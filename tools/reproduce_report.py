#!/usr/bin/env python3
"""Run preregistered and final CPU gates; a CLOSED V4/exit 1 is expected.

Run after tools/fetch_data.py. No GPU, credentials, uploads or paid jobs.
The rendered draft must match tracked bytes; this script never rewrites it.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "r2_problem_train_multi": 0.7822,
    "r2_problem_train_multi_rows": 76,
    "r2_problem_sample_full": 0.1813,
    "conc_train_small_only.concordant": 11,
    "conc_train_small_only.multi": 11,
    "conc_train_small_only.expected_independent": 4.89,
    "conc_train_nogap_p10.concordant": 10,
    "conc_train_nogap_p10.multi": 15,
    "conc_train_nogap_p10.expected_independent": 3.59,
    "control_lopo_small_bacc": 0.6855,
    "agg_format_flag_bacc": 1.0,
    "agg_majority_acc": 0.7447,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--receipt", type=Path, default=Path("results/reproduction/receipt.json"))
    args = ap.parse_args()
    receipt = {"scope": "CPU gates only; remote clone provenance recorded separately", "checks": []}
    with tempfile.TemporaryDirectory(prefix="aimo-report-") as temp:
        tmp = Path(temp)
        def run(name, argv, expected_exit=0, fields=None):
            result = subprocess.run([sys.executable, "-I", *argv], cwd=ROOT, text=True, capture_output=True)
            parsed = json.loads(result.stdout)
            ok = result.returncode == expected_exit and not result.stderr
            if fields:
                ok = ok and all(parsed.get(k) == v for k, v in fields.items())
            entry = {"name": name, "argv": [sys.executable, "-I", *argv], "exit_code": result.returncode,
                     "expected_exit": expected_exit, "stdout": result.stdout, "stderr": result.stderr, "passed": ok}
            receipt["checks"].append(entry)
            print(name + " actual exit " + str(result.returncode))
            print(result.stdout, end="")
            if not ok:
                raise RuntimeError(name + " failed; STOP")
            return parsed
        run("V1_original", ["tools/report_numbers.py", "--data-dir", "data", "--check", "research/preregistered_v5_claims.json"],
            fields={"result": "PASS", "checked": 13})
        run("V2_original", ["tools/render_report.py", "report/PREREGISTERED_OUTLINE_v5.md", "results/report_numbers.json", str(tmp / "original.md")],
            fields={"result": "PASS", "placeholders": 17})
        run("V1_final", ["tools/report_numbers.py", "--data-dir", "data", "--out", str(tmp / "numbers.json"), "--check", "research/claims.json"],
            fields={"result": "PASS", "checked": len(json.loads((ROOT / "research/claims.json").read_text())["claims"])})
        nums = json.loads((tmp / "numbers.json").read_text())
        if nums != json.loads((ROOT / "results/report_numbers.json").read_text()):
            raise RuntimeError("tracked numbers differ from regeneration; STOP")
        for key, value in EXPECTED.items():
            actual = nums
            for bit in key.split("."):
                actual = actual[bit]
            if actual != value:
                raise RuntimeError("V3 mismatch: " + key)
        receipt["checks"].append({"name": "V3", "checked": len(EXPECTED), "passed": True})
        print("V3 PASS: " + str(len(EXPECTED)) + " registered values")
        run("V2_final", ["tools/render_report.py", "report/REPORT_OUTLINE.md", str(tmp / "numbers.json"), str(tmp / "final.md")],
            fields={"result": "PASS"})
        draft = (ROOT / "report/REPORT_DRAFT.md").read_bytes()
        if (tmp / "final.md").read_bytes() != draft:
            raise RuntimeError("tracked draft differs from gated rendering; STOP")
        receipt["draft_sha256"] = hashlib.sha256(draft).hexdigest()
        run("V4", ["tools/reopen_gate.py"], expected_exit=1, fields={"result": "CLOSED"})
    receipt["result"] = "PASS"
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    print("ALL_CPU_GATES_PASS; V4_CLOSED_EXPECTED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
