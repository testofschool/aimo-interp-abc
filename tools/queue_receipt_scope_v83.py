#!/usr/bin/env python3
"""Read the user's hash-verified v8.3 public queue receipts without inventing ownership.

The bundle-to-UUID association is supplied by the user's bundle and handoff.
The saved public API view corroborates status/scores/time, not native ownership,
ZIP bytes uploaded on M5, Codabench user identity, or final-test performance.
The frozen Codabench numeric-ID guard and its preregistration remain unchanged.
"""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = {
    "solution-always-true-small.zip": {
        "prefix": "queue_always_true", "file": "receipt_always_robust.json",
        "sha256": "b05a6f4e29e6c29730a7afff5e371ddc6c36d3acc202a0c4fc4ad5d87e5d7878",
        "uuid": "bde5e370-4dba-4f19-8291-4a998bfecdcd",
        "zip_sha256": "4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a",
    },
    "solution-text-length-control-small.zip": {
        "prefix": "queue_text_length_control", "file": "receipt_length_digit.json",
        "sha256": "0dda2ed544e1ac6c27ab83d528136aa73acde5658dcc7ca2e0dfb28e04d41cd8",
        "uuid": "0c736e59-8248-4dee-8e4f-2df037c552d7",
        "zip_sha256": "30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd",
    },
}
KST = timezone(timedelta(hours=9))


def timestamp(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.utcoffset() is None:
        raise ValueError("receipt timestamp must include a timezone")
    return result


def inspect(*, receipts_dir=None, bundle_root=None, prereg_path=None, now=None):
    receipts_dir = ROOT / "research/v8_3_sources/queue" if receipts_dir is None else Path(receipts_dir)
    bundle_root = ROOT / "bundles" if bundle_root is None else Path(bundle_root)
    prereg_path = ROOT / "research/PREREG_v6.json" if prereg_path is None else Path(prereg_path)
    now = datetime.now(timezone.utc) if now is None else now
    result = {"measurement_status": "UNMEASURED", "measured_score_statements_allowed": False,
              "source": "USER_SUPPLIED_PUBLIC_TEMPORARY_QUEUE_RECEIPTS",
              "association_basis": "DIRECT_USER_SUPPLIED_BUNDLE_AND_HANDOFF",
              "native_owner_receipt_verified": False, "on_codabench_leaderboard": False,
              "final_test_status": "UNMEASURED", "per_problem_balance_inference_allowed": False,
              "pairwise_ranking_inference_allowed": False, "rows": [], "errors": []}
    try:
        if now.utcoffset() is None:
            raise ValueError("evaluation time requires a timezone")
        pre = json.loads(prereg_path.read_text())
        registered = timestamp(pre["registered_at"])
        expected = {x["bundle"]: x for x in pre["predictions"]}
        if set(expected) != set(RECEIPTS):
            raise ValueError("exactly the two registered frozen bundles are required")
        for bundle, spec in RECEIPTS.items():
            contract = expected[bundle]
            if contract["track"] != "Small" or contract["n_items"] != 14 or contract["sha256"] != spec["zip_sha256"]:
                raise ValueError("frozen Small bundle contract mismatch")
            zip_bytes = (bundle_root / bundle).read_bytes()
            if hashlib.sha256(zip_bytes).hexdigest() != spec["zip_sha256"]:
                raise ValueError("frozen ZIP hash mismatch: " + bundle)
            raw = (receipts_dir / spec["file"]).read_bytes()
            if hashlib.sha256(raw).hexdigest() != spec["sha256"]:
                raise ValueError("supplied receipt SHA256SUMS mismatch: " + spec["file"])
            row = json.loads(raw)
            if row["id"] != spec["uuid"] or row["task"] != "small" or row["status"] != "Finished":
                raise ValueError("queue UUID/task/terminal status mismatch")
            if row.get("_provenance", {}).get("source") != "public GET https://codabench-queue.josefkuchar.com/ui-api/submissions/" + spec["uuid"]:
                raise ValueError("public queue provenance URL mismatch")
            accuracy = row["scores"]["accuracy"]
            if isinstance(accuracy, bool) or not isinstance(accuracy, (int, float)) or not math.isfinite(accuracy) or not 0 <= accuracy <= 1:
                raise ValueError("accuracy must be finite numeric data in [0,1]")
            n = contract["n_items"]
            k = round(accuracy * n)
            if abs(accuracy * n - k) >= 1e-9:
                raise ValueError("accuracy does not fit the registered 14-item contract")
            if k > 11:
                raise ValueError("registered E1 stop threshold exceeded; do not resubmit")
            created = timestamp(row["created_at"])
            if not registered < created <= now:
                raise ValueError("receipt must postdate registration and not be in the future")
            result["rows"].append({"bundle": bundle, "prefix": spec["prefix"], "submission_id": row["id"],
                "k": k, "n": n, "accuracy": accuracy,
                "created_at_kst": created.astimezone(KST).strftime("%Y-%m-%d %H:%M:%S"),
                "faircoin_one_sided_p": sum(math.comb(n, j) for j in range(k, n + 1)) / 2**n,
                "receipt_sha256": spec["sha256"], "zip_sha256": spec["zip_sha256"], "zip_bytes": len(zip_bytes)})
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        result["errors"].append(str(error))
        return result
    result["measurement_status"] = "RECORDED_TEMPORARY_QUEUE_PUBLIC_RECEIPTS"
    result["measured_score_statements_allowed"] = True
    return result


def numbers(state):
    if not state["measured_score_statements_allowed"] or state["errors"]:
        raise ValueError("verified supplied queue receipts are required: " + "; ".join(state["errors"]))
    out = {}
    for row in state["rows"]:
        for key in ("k", "n", "accuracy", "submission_id", "created_at_kst", "faircoin_one_sided_p"):
            out[row["prefix"] + "_" + key] = row[key]
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipts-dir", type=Path)
    args = parser.parse_args()
    state = inspect(receipts_dir=args.receipts_dir)
    print(json.dumps(state, indent=2))
    return 0 if state["measured_score_statements_allowed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
