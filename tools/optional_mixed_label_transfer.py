import sys, json, hashlib, collections
import numpy as np, pandas as pd
TOOLS, SELF, PARQ, OUT = sys.argv[1:5]
sys.path.insert(0, TOOLS)  # our own code: reuse text_X, fit, clustered_intervals verbatim
from report_numbers import text_X, fit, clustered_intervals
from sklearn.metrics import balanced_accuracy_score as BA, accuracy_score
from sklearn.model_selection import LeaveOneGroupOut

def evaluate(df, name):
    df = df.reset_index(drop=True)
    y = df.y.to_numpy(); g = df.gid.to_numpy()
    X = text_X(df.problem)
    oof = np.zeros(len(df))
    for tr, te in LeaveOneGroupOut().split(X, groups=g):
        if len(np.unique(y[tr])) < 2: oof[te] = y[tr][0]; continue
        oof[te] = fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]
    pred = (oof >= 0.5).astype(int)
    per = df.groupby('gid').y.agg(['sum', 'size'])
    mixed = per[(per['sum'] > 0) & (per['sum'] < per['size'])]
    multi = per[per['size'] > 1]
    balanced = per[2 * per['sum'] == per['size']]
    # per-problem majority oracle (in-sample, best possible problem-only predictor for accuracy)
    maj = (2 * per['sum'] >= per['size']).astype(int)  # tie -> 1
    opred = df.gid.map(maj).to_numpy()
    oracle_correct = int((per[['sum']].values.ravel().clip(0) * 0 + np.maximum(per['sum'], per['size'] - per['sum'])).sum())
    bal_rows = df.gid.isin(balanced.index).to_numpy()
    r = dict(
        set=name, rows=len(df), problems=int(df.gid.nunique()), models=int(df.model_id.nunique()),
        robust=int(y.sum()), nonrobust=int((1 - y).sum()),
        problems_with_gt1_label=int(len(multi)), problems_mixed_labels=int(len(mixed)),
        problems_exactly_balanced=int(len(balanced)), rows_in_exactly_balanced=int(bal_rows.sum()),
        size_dist=dict(collections.Counter(per['size'].tolist())),
        control_lopo_bacc=round(BA(y, pred), 4), control_lopo_acc=round(accuracy_score(y, pred), 4),
        control_correct=int((y == pred).sum()),
        always_true_acc=round(float(y.mean()), 4),
        bootstrap=clustered_intervals(y, pred, g, draws=4000, seed=0),
        oracle_majority_acc=round(oracle_correct / len(df), 4), oracle_correct=oracle_correct,
        oracle_majority_bacc=round(BA(y, opred), 4),
        oracle_acc_on_exactly_balanced_rows=(round(accuracy_score(y[bal_rows], opred[bal_rows]), 6) if bal_rows.any() else None),
        oracle_acc_on_exactly_balanced_rows_tie0=(round(accuracy_score(y[bal_rows], 1 - opred[bal_rows]), 6) if bal_rows.any() else None),
        control_acc_on_exactly_balanced_rows=(round(accuracy_score(y[bal_rows], pred[bal_rows]), 6) if bal_rows.any() else None),
    )
    return r

out = {}
s = pd.DataFrame([json.loads(l) for l in open(SELF)])
s = s[s.is_robust.notna()].copy(); s['y'] = s.is_robust.astype(int); s['gid'] = s.problem_id
out['self_labels_all'] = evaluate(s, 'self_labels labelled (incl base_zero)')
out['self_labels_nobase0'] = evaluate(s[~s.base_zero.astype(bool)], 'self_labels labelled, base_zero excluded')
t = pd.read_parquet(PARQ)
SMALL = ("Qwen/Qwen3.5-4B", "Skywork/Skywork-OR1-Math-7B", "allenai/Olmo-3-7B-Think", "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B")
o = t[t.model_id.isin(SMALL) & t.is_robust.notna()].copy()
o['gid'] = o.problem.map(lambda p: hashlib.sha256(p.strip().encode()).hexdigest()[:16])
n_before = len(o)
o = o.drop_duplicates(['model_id', 'gid'], keep='first')
o['y'] = o.is_robust.astype(int)
out['official_small_dedup'] = evaluate(o, f'train-main-v2 small-model labelled, dedup (model,problem): {n_before}->{len(o)}')
o3 = o[o.model_id != 'allenai/Olmo-3-7B-Think']
out['official_small_3models_noOlmo'] = evaluate(o3, 'train-main-v2 labelled, the 3 self-label models (Olmo excluded) -- reconstruction of byeolki 34 rows')
ov = len(set(o.gid) & set(s.gid)); out['official_vs_self_problem_overlap'] = ov
json.dump(out, open(OUT, 'w'), indent=1, default=str)
for k, v in out.items(): print(k, v)
