#!/usr/bin/env python3
"""prereg_codabench_gate.py — judge the owner's Codabench receipts against values registered BEFORE upload.

Usage: python3 -I tools/prereg_codabench_gate.py research/PREREG_v6.json results/v6/codabench_receipts.json
Exit 0 = every receipt matches its registered bundle hash and the verdict is computed (prints which report
         sentence variant is licensed) · 1 = missing receipt, hash mismatch, or registration dated after a receipt
         (blocks rendering section 4 private-val claims) · 2 = unreadable input.
Receipt row: {"bundle": "...zip", "sha256": "...", "track": "Small", "submission_id": "...",
              "status": "Finished", "accuracy": 0.5, "submitted_at": "ISO+tz"}
Stdlib only.
"""
import json, sys
from datetime import datetime

def dt(s): return datetime.fromisoformat(s.replace("Z", "+00:00"))

def main(a):
    if len(a) != 2:
        print("usage: prereg_codabench_gate.py PREREG.json RECEIPTS.json", file=sys.stderr); return 2
    try:
        pre = json.load(open(a[0], encoding="utf-8")); rec = json.load(open(a[1], encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(json.dumps({"result": "UNREADABLE", "error": str(e)})); return 2
    errs, rows = [], {r["bundle"]: r for r in rec.get("receipts", [])}
    reg_at = dt(pre["registered_at"])
    out = []
    for p in pre["predictions"]:
        r = rows.get(p["bundle"])
        if r is None:
            errs.append(f"missing receipt for {p['bundle']}"); continue
        if r.get("sha256") != p["sha256"]:
            errs.append(f"{p['bundle']}: sha256 {r.get('sha256')} != registered {p['sha256']}")
        if r.get("track") != p["track"]:
            errs.append(f"{p['bundle']}: track {r.get('track')} != {p['track']}")
        if r.get("status") != "Finished":
            errs.append(f"{p['bundle']}: status {r.get('status')} (need Finished)")
        if dt(r["submitted_at"]) <= reg_at:
            errs.append(f"{p['bundle']}: submitted {r['submitted_at']} not after registration {pre['registered_at']}")
        n = p["n_items"]; k = round(float(r.get("accuracy", -1)) * n)
        match = round(k / n, 2) == round(float(r.get("accuracy", -1)), 2) and k == p["expected_k"]
        out.append({"bundle": p["bundle"], "expected": f"{p['expected_k']}/{n}", "observed": f"{k}/{n}", "match": match})
    if errs:
        print(json.dumps({"result": "BLOCKED", "errors": errs}, indent=1)); return 1
    allm = all(o["match"] for o in out)
    print(json.dumps({"result": "JUDGED", "verdict": pre["if_all_match"] if allm else pre["if_any_mismatch"],
                      "rows": out}, indent=1, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
