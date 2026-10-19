#!/usr/bin/env python3
"""Regenerate every CPU-measurable number the report cites, and gate the report on them.

    python3 -I tools/report_numbers.py --data-dir data --out results/report_numbers.json
    python3 -I tools/report_numbers.py --data-dir data --check research/claims.json   # exit 1 on any mismatch

data/ must hold: train-main-v2.parquet, val-sample.parquet, sample-full.parquet,
augmented-sample-math-agg.parquet (organizer HF datasets; see HANDOFF for sha256).
A report sentence that cites a number not produced here, or produced differently, is not
allowed into the report: --check exits 1 and prints the offending claim.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score as BA
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import LeaveOneGroupOut, StratifiedGroupKFold

DATA_SHA256 = {
    "train-main-v2.parquet": "e18eb44207e7987781ec2ff214793196038442bdc1466fdf5498f3e87ec58285",
    "val-sample.parquet": "3919cb3d951bb360a120be3397e926f48b7819bcd97e12cfee4c01e76618560f",
    "sample-full.parquet": "2989ab6a018f2779a821209f414bd0049c9ef1c2488f589ff2d3bf4ed16942ff",
    "augmented-sample-math-agg.parquet": "b785750259a3f4524cbaf988f51660197cbdfca19d8f45cc35347d4ef29aa4db",
}


def clustered_intervals(y, pred, groups, draws=4000, seed=0):
    """Percentile intervals conditional on fixed OOF predictions; skip one-class draws.

    Sort cluster labels, sample the original number of clusters with replacement
    using numpy.default_rng, concatenate every row in each selected cluster.
    The same draws estimate the paired difference from the always-True rule.
    This is not a bootstrap of the whole training pipeline or an MDE calculation.
    """
    labels = np.unique(groups)
    clusters = [np.flatnonzero(groups == g) for g in labels]
    rng = np.random.default_rng(seed)
    bacc, acc, delta = [], [], []
    for _ in range(draws):
        idx = np.concatenate([clusters[i] for i in rng.integers(len(labels), size=len(labels))])
        yy, pp = y[idx], pred[idx]
        if len(np.unique(yy)) != 2:
            continue
        value = BA(yy, pp)
        bacc.append(value)
        acc.append(accuracy_score(yy, pp))
        delta.append(value - BA(yy, np.ones(len(yy), dtype=int)))
    def ci(values):
        lo, hi = np.quantile(values, [0.025, 0.975], method="linear")
        return {"low": round(float(lo), 4), "high": round(float(hi), 4)}
    return {"draws": draws, "seed": seed, "valid_draws": len(bacc),
            "bacc_ci95": ci(bacc), "acc_ci95": ci(acc), "delta_bacc_ci95": ci(delta),
            "delta_bacc_sd": round(float(np.std(delta, ddof=1)), 4)}


def text_X(s):
    return np.c_[np.log1p(s.str.len()), s.str.count(r"\d")]


def fit(X, y):
    return LogisticRegression(class_weight="balanced", max_iter=2000).fit(X, y)


def concordance(df, key, lab):
    g = df.groupby(key)[lab].agg(["mean", "size"])
    m = g[g["size"] > 1]
    p = df[lab].mean()
    return {"multi": int(len(m)), "concordant": int(((m["mean"] == 0) | (m["mean"] == 1)).sum()),
            "expected_independent": round(float(sum(p ** k + (1 - p) ** k for k in m["size"])), 2)}


def run(d):
    out = {}
    for filename, expected in DATA_SHA256.items():
        with open(os.path.join(d, filename), "rb") as handle:
            actual = hashlib.sha256(handle.read()).hexdigest()
        if actual != expected:
            raise ValueError(f"STOP: {filename} hash {actual} != {expected}")
    t = pd.read_parquet(os.path.join(d, "train-main-v2.parquet"))
    L = t.dropna(subset=["is_robust"]).reset_index(drop=True)
    L["y"] = L.is_robust.astype(int)
    small = ~L.model_id.str.startswith("openai")
    # 1. text control, leave-one-problem-out, trained on all 80 labelled rows, scored on 43 Small rows
    oof = np.zeros(len(L))
    X = text_X(L.problem)
    for tr, te in LeaveOneGroupOut().split(X, groups=L.problem):
        oof[te] = fit(X[tr], L.y[tr]).predict_proba(X[te])[:, 1]
    out["control_lopo_small_bacc"] = round(BA(L.y[small], oof[small] >= 0.5), 4)
    out["small_rows"] = int(small.sum())
    out["small_problems"] = int(L[small].problem.nunique())
    pred = (oof[small] >= 0.5).astype(int)
    yy = L.y[small].to_numpy()
    out["control_lopo_small_acc"] = round(accuracy_score(yy, pred), 4)
    out["always_true_small_acc"] = round(accuracy_score(yy, np.ones(len(yy))), 4)
    out["always_true_small_bacc"] = round(BA(yy, np.ones(len(yy))), 4)
    out["control_small_correct"] = int((yy == pred).sum())
    out["always_true_small_correct"] = int(yy.sum())
    out["control_small_tp"] = int(((yy == 1) & (pred == 1)).sum())
    out["control_small_tn"] = int(((yy == 0) & (pred == 0)).sum())
    out["small_robust_rows"] = int(yy.sum())
    out["small_nonrobust_rows"] = int((1 - yy).sum())
    out["small_bootstrap"] = clustered_intervals(yy, pred, L.problem[small].to_numpy())
    out["control_small_delta_bacc"] = round(out["control_lopo_small_bacc"] - out["always_true_small_bacc"], 4)
    out["train_rows"] = int(len(t))
    out["train_problems"] = int(t.problem.nunique())
    out["train_labelled_rows"] = int(len(L))
    out["train_labelled_problems"] = int(L.problem.nunique())
    out["train_unlabelled_rows"] = int(t.is_robust.isna().sum())
    # 2. same control on the organizer baseline's own rows and CV scheme (141-row agg set)
    a = pd.read_parquet(os.path.join(d, "augmented-sample-math-agg.parquet")).dropna(subset=["model_is_robust"]).reset_index(drop=True)
    Xa, ya, ga = text_X(a.original_problem), a.model_is_robust.astype(int).values, a.problem_id.values
    res, accs = [], []
    for seed in range(10):
        o = np.zeros(len(a))
        for tr, te in StratifiedGroupKFold(5, shuffle=True, random_state=seed).split(Xa, ya, ga):
            o[te] = fit(Xa[tr], ya[tr]).predict_proba(Xa[te])[:, 1]
        res.append(BA(ya, o >= 0.5))
        accs.append(accuracy_score(ya, o >= 0.5))
    out["control_agg_sgkf_bacc_mean"] = round(float(np.mean(res)), 4)
    out["control_agg_sgkf_bacc_min"] = round(float(min(res)), 4)
    out["control_agg_sgkf_bacc_max"] = round(float(max(res)), 4)
    out["agg_rows"] = int(len(a))
    out["agg_problems"] = int(a.problem_id.nunique())
    out["control_agg_sgkf_acc_mean"] = round(float(np.mean(accs)), 4)
    # 3. transfer: trained on train-main-v2 (80), applied to agg (141) and val-sample
    m = fit(X, L.y)
    out["control_transfer_train_to_agg_bacc"] = round(BA(ya, m.predict_proba(Xa)[:, 1] >= 0.5), 4)
    v = pd.read_parquet(os.path.join(d, "val-sample.parquet"))
    out["control_transfer_train_to_val_bacc"] = round(BA(v.model_is_robust.astype(int), m.predict_proba(text_X(v.original_problem))[:, 1] >= 0.5), 4)
    out["control_transfer_train_to_agg_acc"] = round(accuracy_score(ya, m.predict(Xa)), 4)
    out["control_transfer_train_to_val_acc"] = round(accuracy_score(v.model_is_robust.astype(int), m.predict(text_X(v.original_problem))), 4)
    out["val_sample_rows"] = int(len(v))
    vd = v.drop_duplicates(["model_id", "problem_id"])
    out["val_sample_pairs"] = int(len(vd))
    out["conc_val_sample_dedup"] = concordance(vd.assign(y=vd.model_is_robust.astype(int)), "problem_id", "y")
    out["val_oracle_base_accuracy_auc"] = round(roc_auc_score(vd.model_is_robust.astype(int), vd.base_accuracy), 4)
    out["val_nonrobust_base1"] = int(((~vd.model_is_robust) & (vd.base_accuracy == 1)).sum())
    out["val_nonrobust_pairs"] = int((~vd.model_is_robust).sum())
    # 4. cross-model label concordance under several readings
    t["cfg"] = t.model_id.where(~t.model_id.str.startswith("openai"), "gpt-oss")
    out["conc_train_all_configs"] = concordance(L, "problem", "y")
    C = L.assign(cfg=t.loc[t.is_robust.notna(), "cfg"].values).groupby(["problem", "cfg"]).y.mean().round().reset_index()
    out["conc_train_gptoss_collapsed"] = concordance(C, "problem", "y")
    out["conc_train_small_only"] = concordance(L[small], "problem", "y")
    t["y0"] = (t.max_drop <= 0).astype(int)
    out["conc_train_decay0_rule_gptoss_collapsed"] = concordance(t.groupby(["problem", "cfg"]).y0.max().reset_index(), "problem", "y0")
    vv = v.assign(y=v.model_is_robust.astype(int))
    out["conc_val_sample"] = concordance(vv, "problem_id", "y")
    f = pd.read_parquet(os.path.join(d, "sample-full.parquet"))
    md = f.groupby(["model_id", "problem_id"]).absolute_accuracy_decay.max().reset_index(name="max_drop")
    md["y"] = md.max_drop.map(lambda x: 1 if x <= 0.10 else (0 if x >= 0.25 else np.nan))
    out["conc_sample_full_maxdrop_rule"] = concordance(md.dropna(), "problem_id", "y")
    # 5. label construction on the 141-row set: row format vs label, trivial baselines
    fmt = a.permutation_type.astype(str).str.startswith("[")
    out["agg_format_crosstab"] = {"list_rows_robust": int((fmt & (ya == 1)).sum()), "list_rows_nonrobust": int((fmt & (ya == 0)).sum()),
                                  "string_rows_robust": int((~fmt & (ya == 1)).sum()), "string_rows_nonrobust": int((~fmt & (ya == 0)).sum())}
    out["agg_format_flag_bacc"] = round(BA(ya, fmt.astype(int).values), 4)
    out["agg_majority_acc"] = round(float(max(ya.mean(), 1 - ya.mean())), 4)
    # 6. share of max_drop variance explained by problem identity
    def r2(df, g, y):
        mm = df.groupby(g)[y].transform("mean")
        return round(float(1 - ((df[y] - mm) ** 2).sum() / ((df[y] - df[y].mean()) ** 2).sum()), 4)
    tm = t[t.groupby("problem").model_id.transform("size") > 1]
    out["r2_problem_train_multi"] = r2(tm, "problem", "max_drop")
    out["r2_problem_train_multi_rows"] = int(len(tm))
    out["r2_problem_train_multi_problems"] = int(tm.problem.nunique())
    out["r2_problem_train_multi_single_model_problems"] = int((tm.groupby("problem").model_id.nunique() == 1).sum())
    true_multi = t[t.groupby("problem").model_id.transform("nunique") > 1]
    out["r2_problem_train_true_multi"] = r2(true_multi, "problem", "max_drop")
    out["r2_problem_train_true_multi_rows"] = int(len(true_multi))
    out["r2_problem_train_true_multi_problems"] = int(true_multi.problem.nunique())
    st = t[~t.model_id.str.startswith("openai")]
    stm = st[st.groupby("problem").model_id.transform("size") > 1]
    out["r2_problem_small_multi"] = r2(stm, "problem", "max_drop")
    out["r2_problem_small_multi_rows"] = int(len(stm))
    out["r2_problem_small_multi_problems"] = int(stm.problem.nunique())
    out["r2_problem_sample_full"] = r2(md, "problem_id", "max_drop")
    out["r2_problem_sample_full_pairs"] = int(len(md))
    out["sample_full_models"] = int(md.model_id.nunique())
    out["sample_full_problems"] = int(md.problem_id.nunique())
    # 7. concordance without dropping the 0.10-0.25 band (all rows, gpt-oss collapsed, robust iff max_drop <= 0.10)
    t["yb"] = (t.max_drop <= 0.10).astype(int)
    out["conc_train_nogap_p10"] = concordance(t.groupby(["problem", "cfg"]).yb.min().reset_index(), "problem", "yb")
    # 8. The independent v6 leaderboard tool checks all raw snapshot bytes before
    # parsing. Load by absolute path so this also works under Python -I.
    tool_path = Path(__file__).with_name("leaderboard_identifiability.py")
    spec = importlib.util.spec_from_file_location("leaderboard_identifiability", tool_path)
    identifiability = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(identifiability)
    out.update(identifiability.run(Path(d) / "leaderboard/2026-10-19", d)["numbers"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--out")
    ap.add_argument("--check")
    a = ap.parse_args()
    nums = run(a.data_dir)
    if a.out:
        json.dump(nums, open(a.out, "w"), indent=1)
    if not a.check:
        print(json.dumps(nums, indent=1))
        return 0
    claims = json.load(open(a.check))
    bad = []
    for c in claims["claims"]:
        cur = nums
        for k in c["key"].split("."):
            cur = cur.get(k) if isinstance(cur, dict) else None
        if cur != c["value"]:
            bad.append({"claim": c["text"], "key": c["key"], "claimed": c["value"], "regenerated": cur})
    print(json.dumps({"result": "PASS" if not bad else "FAIL", "checked": len(claims["claims"]), "mismatches": bad}, indent=1, ensure_ascii=False))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
