#!/usr/bin/env python3
"""Reopen gate for the method track (folded 2026-10-19 after three sweep rounds).

    python3 -I tools/reopen_gate.py --labels LABELS.csv --official data/train-main-v2.parquet

Exit 0 only if a NEW paid method job is justified, i.e. LABELS.csv (self-made robustness labels) has
  (1) all four exact Small checkpoints: Qwen/Qwen3.5-4B, Skywork/Skywork-OR1-Math-7B,
      allenai/Olmo-3-7B-Think, deepseek-ai/DeepSeek-R1-0528-Qwen3-8B;
  (2) min samples per condition (column n_samples) >= 48;
  (3) >= 150 labelled (problem, model) rows;
  (4) on the rows that overlap the official labelled Small rows, agreement with the official is_robust >= 0.80
      on >= 10 overlapping rows.
Otherwise exit 1: do not start any paid method job; the text-control entry and the report stand.
Without --labels the gate always exits 1 (the current state).
LABELS.csv columns: problem, model_id, n_samples, is_robust (0/1).
"""
import argparse
import json
import sys

import pandas as pd

TARGETS = {"Qwen/Qwen3.5-4B", "Skywork/Skywork-OR1-Math-7B", "allenai/Olmo-3-7B-Think",
           "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels")
    ap.add_argument("--official", default="data/train-main-v2.parquet")
    a = ap.parse_args()
    if not a.labels:
        print(json.dumps({"result": "CLOSED", "reason": "no self-made labels supplied; method track stays folded"}))
        return 1
    lab = pd.read_csv(a.labels)
    off = pd.read_parquet(a.official).dropna(subset=["is_robust"])
    off = off[off.model_id.isin(TARGETS)]
    checks = {
        "all_four_checkpoints": TARGETS.issubset(set(lab.model_id)),
        "min_samples_ge_48": bool(lab.n_samples.min() >= 48),
        "rows_ge_150": bool(len(lab) >= 150),
    }
    m = lab.merge(off[["problem", "model_id", "is_robust"]], on=["problem", "model_id"], suffixes=("", "_official"))
    agree = float((m.is_robust.astype(int) == m.is_robust_official.astype(int)).mean()) if len(m) else 0.0
    checks["official_overlap_ge_10"] = bool(len(m) >= 10)
    checks["agreement_ge_0.80"] = bool(agree >= 0.80)
    ok = all(checks.values())
    print(json.dumps({"result": "OPEN" if ok else "CLOSED", "checks": checks, "overlap_rows": int(len(m)),
                      "agreement": round(agree, 4)}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
