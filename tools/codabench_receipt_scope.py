#!/usr/bin/env python3
"""Conservatively inspect owner receipt scope without blocking unrelated report work.

The supplied prereg_codabench_gate.py and PREREG_v6.json remain frozen. Their
matching/mismatching verdict text is diagnostic input, never report prose:
two aggregate control scores cannot establish per-problem label balance.
This wrapper checks structure and supporting screenshot files, then permits
only the recorded bundle scores. It does not authenticate an external service.
Missing/invalid receipts remain UNMEASURED after the rendering gate expires.
"""
import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DEADLINE = datetime(2026, 11, 1, 11, 55, tzinfo=timezone.utc)


def timestamp(value):
    value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if value.utcoffset() is None:
        raise ValueError("timezone is required")
    return value


def inspect(prereg_path, receipts_path, now):
    base = {
        "scope": "owner bundle private-validation statements only; other report sections proceed",
        "measurement_status": "UNMEASURED",
        "render_gate_deadline_utc": DEADLINE.isoformat(),
        "render_gate_expired": now >= DEADLINE,
        "render_gate_active": now < DEADLINE,
        "measured_score_statements_allowed": False,
        "per_problem_balance_inference_allowed": False,
        "rows": [], "errors": [],
    }
    try:
        pre = json.loads(prereg_path.read_text())
        registered = timestamp(pre["registered_at"])
        rec = json.loads(receipts_path.read_text())
        rows = rec["receipts"]
        if not isinstance(rows, list):
            raise ValueError("receipts must be a list")
        predictions = {p["bundle"]: p for p in pre["predictions"]}
        if len(rows) != len(predictions):
            base["errors"].append("exactly one receipt is required for each expected bundle")
        bundles, submission_ids = set(), set()
        for row in rows:
            bundle = row["bundle"]
            if bundle not in predictions or bundle in bundles:
                raise ValueError("unknown or duplicate receipt bundle")
            bundles.add(bundle)
            prediction = predictions[bundle]
            submission_id = str(row.get("submission_id", ""))
            if not submission_id.isdigit() or submission_id in submission_ids:
                raise ValueError("distinct numeric submission IDs are required")
            submission_ids.add(submission_id)
            when = timestamp(row["submitted_at"])
            if not registered < when <= now:
                raise ValueError("receipt time must follow registration and not be in the future")
            accuracy = row["accuracy"]
            if isinstance(accuracy, bool) or not isinstance(accuracy, (int, float)) or not math.isfinite(accuracy) or not 0 <= accuracy <= 1:
                raise ValueError("accuracy must be a finite number in [0, 1]")
            n = prediction["n_items"]
            correct = round(accuracy * n)
            if round(correct / n, 2) != round(accuracy, 2):
                raise ValueError("accuracy does not fit the registered item count at displayed precision")
            screenshot = receipts_path.parent / row.get("screenshot", "")
            if not row.get("screenshot") or not screenshot.is_file():
                raise ValueError("a supporting screenshot file is required for each owner receipt")
        if bundles != set(predictions):
            base["errors"].append("one or more expected bundles have no receipt")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        base["errors"].append(str(error))
    if base["errors"]:
        return base
    result = subprocess.run([sys.executable, "-I", str(ROOT / "tools/prereg_codabench_gate.py"),
                             str(prereg_path), str(receipts_path)], text=True, capture_output=True)
    try:
        diagnostic = json.loads(result.stdout)
    except ValueError:
        diagnostic = {"result": "UNREADABLE_OUTPUT"}
    base["frozen_gate_exit"] = result.returncode
    base["frozen_gate_result"] = diagnostic.get("result")
    if result.returncode != 0 or result.stderr or diagnostic.get("result") != "JUDGED":
        base["errors"].append("frozen receipt gate did not judge the receipts")
        return base
    base.update({"measurement_status": "RECORDED_OWNER_RECEIPTS",
                 "render_gate_active": False, "measured_score_statements_allowed": True,
                 "rows": diagnostic["rows"],
                 "interpretation": "Recorded scores only. Neither matching nor mismatching aggregate scores establish the per-problem composition; external authenticity requires owner evidence review."})
    return base


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prereg", type=Path, default=ROOT / "research/PREREG_v6.json")
    parser.add_argument("--receipts", type=Path, default=ROOT / "results/v6/codabench_receipts.json")
    parser.add_argument("--now", help="explicit ISO timestamp for synthetic boundary tests")
    args = parser.parse_args()
    now = timestamp(args.now) if args.now else datetime.now(timezone.utc)
    print(json.dumps(inspect(args.prereg, args.receipts, now), indent=2))
    return 0  # A missing owner receipt never fails unrelated CPU/report gates.


if __name__ == "__main__":
    sys.exit(main())
