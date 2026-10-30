#!/usr/bin/env python3
"""Recover the supplied control recipe; preserve all supplied artifacts."""
import hashlib
import json
import math
import re
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parents[1]
TRAIN_SHA = "e18eb44207e7987781ec2ff214793196038442bdc1466fdf5498f3e87ec58285"


def features(problems):
    return np.asarray([[math.log1p(len(p)), len(re.findall(r"\d", p))] for p in problems])


def estimator():
    return LogisticRegression(class_weight="balanced", max_iter=2000)


def main():
    assert sklearn.__version__ == "1.8.0" and joblib.__version__ == "1.5.3"
    source = ROOT / "data/train-main-v2.parquet"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == TRAIN_SHA
    table = pd.read_parquet(source).dropna(subset=["is_robust"]).copy()
    pid = {p: f"p{i:03d}" for i, p in enumerate(sorted(table.problem.unique()))}
    table["problem_id"] = table.problem.map(pid)
    small = table[table.model_id != "openai/gpt-oss-120b"].copy()
    out = ROOT / "results/control_reproduction"
    out.mkdir(parents=True, exist_ok=True)
    rows, folds = [], []
    for problem_id in sorted(small.problem_id.unique()):
        fit = table[table.problem_id != problem_id]
        test = small[small.problem_id == problem_id]
        model = estimator().fit(features(fit.problem), fit.is_robust.astype(int))
        scores = model.predict_proba(features(test.problem))[:, 1]
        folds.append({"heldout_problem": problem_id,
                      "fit_problem_ids": sorted(fit.problem_id.unique()),
                      "fit_rows": len(fit), "evaluation_rows": len(test)})
        for row, score in zip(test.itertuples(), scores):
            rows.append({"problem_id": row.problem_id, "model_id": row.model_id,
                         "reasoning_effort": row.reasoning_effort,
                         "label": int(row.is_robust), "score": float(score)})
    reproduced = pd.DataFrame(rows)
    reproduced.to_csv(out / "oof.csv", index=False)
    keys = ["problem_id", "model_id", "reasoning_effort"]
    supplied = pd.read_csv(ROOT / "controls/text_length.csv")
    joined = supplied.merge(reproduced, on=keys, validate="one_to_one", suffixes=("_supplied", "_reproduced"))
    delta = float(abs(joined.score_supplied - joined.score_reproduced).max())
    assert len(joined) == 43 and delta < 1e-10
    assert (joined.label_supplied == joined.label_reproduced).all()
    model = estimator().fit(features(table.problem), table.is_robust.astype(int))
    artifact = {"model": model, "features": "log1p(len(problem)), count(digits)",
                "trained_on": "aimo-interp/train-main-v2 labelled rows (80)",
                "sha_train": "e18eb442"}
    joblib.dump(artifact, out / "text_length.joblib")
    supplied_model = joblib.load(ROOT / "bundles/text-length-control-src/artifacts/text_length.joblib")["model"]
    coeff_delta = float(abs(model.coef_ - supplied_model.coef_).max())
    assert coeff_delta < 1e-10
    assert np.array_equal(model.predict(features(table.problem)), supplied_model.predict(features(table.problem)))
    summary = {"status": "PASS", "train_sha256": TRAIN_SHA,
               "training_cohort": "all 80 labelled rows, excluding every held-out problem across all models",
               "evaluation_rows": 43, "evaluation_problems": 22,
               "oof_max_abs_difference": delta, "refit_coefficient_max_abs_difference": coeff_delta,
               "sklearn": sklearn.__version__, "joblib": joblib.__version__,
               "numpy": np.__version__, "pandas": pd.__version__,
               "note": "Recovered recipe matches supplied scores numerically; supplied artifacts unchanged."}
    (out / "fold_manifest.json").write_text(json.dumps({"estimator": estimator().get_params(), "folds": folds}, indent=2) + "\n")
    (out / "reproduction.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
