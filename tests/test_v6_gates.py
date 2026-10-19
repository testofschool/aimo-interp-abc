#!/usr/bin/env python3
"""Synthetic tests only; these fixtures are never Codabench observations."""
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("receipt_scope", ROOT / "tools/codabench_receipt_scope.py")
scope = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scope)


class GateTests(unittest.TestCase):
    def test_supplied_synthetic_fixture_contract(self):
        for name, expected_exit in [("match", 0), ("mismatch", 0), ("badsha", 1), ("early", 1), ("missing", 1)]:
            with self.subTest(fixture=name):
                result = subprocess.run([sys.executable, "-I", str(ROOT / "tools/prereg_codabench_gate.py"),
                                         str(ROOT / "research/PREREG_v6.json"), str(ROOT / f"tests/fx_{name}.json")],
                                        text=True, capture_output=True)
                self.assertEqual(result.returncode, expected_exit)
                self.assertFalse(result.stderr)
                if name == "mismatch":
                    self.assertTrue(json.loads(result.stdout)["verdict"].startswith("REFUTED_OR_PARTIAL:"))

    def test_deadline_does_not_create_measurements(self):
        for now, active in [("2026-11-01T11:54:59Z", True), ("2026-11-01T11:55:00Z", False)]:
            with self.subTest(now=now), tempfile.TemporaryDirectory() as temp:
                result = scope.inspect(ROOT / "research/PREREG_v6.json", Path(temp) / "missing.json", scope.timestamp(now))
                self.assertEqual(result["measurement_status"], "UNMEASURED")
                self.assertEqual(result["render_gate_active"], active)
                self.assertFalse(result["measured_score_statements_allowed"])
                self.assertFalse(result["per_problem_balance_inference_allowed"])

    def test_matching_scores_never_license_per_problem_inference(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            fixture = json.loads((ROOT / "tests/fx_match.json").read_text())
            for number, row in enumerate(fixture["receipts"]):
                row["submission_id"] = str(100 + number)
                row["screenshot"] = "synthetic-screenshot.txt"
            (temp / "synthetic-screenshot.txt").write_text("SYNTHETIC TEST EVIDENCE; not a service screenshot")
            receipts = temp / "synthetic-receipts.json"
            receipts.write_text(json.dumps(fixture))
            result = scope.inspect(ROOT / "research/PREREG_v6.json", receipts, scope.timestamp("2026-10-22T00:00:00Z"))
            self.assertEqual(result["measurement_status"], "RECORDED_OWNER_RECEIPTS")
            self.assertTrue(result["measured_score_statements_allowed"])
            self.assertFalse(result["per_problem_balance_inference_allowed"])
            self.assertNotIn("verdict", result)

    def test_weak_receipts_are_unmeasured(self):
        changes = [lambda rows: rows.append(rows[0].copy()),
                   lambda rows: rows[0].update(accuracy=1.5),
                   lambda rows: rows[0].update(accuracy=float("nan")),
                   lambda rows: rows[0].update(accuracy=0.51),
                   lambda rows: rows[0].update(submitted_at="2026-10-21T10:00:00"),
                   lambda rows: rows[0].update(submission_id=""),
                   lambda rows: rows[0].update(screenshot="absent.png")]
        for change in changes:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temp:
                temp = Path(temp)
                fixture = json.loads((ROOT / "tests/fx_match.json").read_text())
                for number, row in enumerate(fixture["receipts"]):
                    row.update(submission_id=str(100 + number), screenshot="synthetic.txt")
                (temp / "synthetic.txt").write_text("SYNTHETIC")
                change(fixture["receipts"])
                receipts = temp / "synthetic.json"
                receipts.write_text(json.dumps(fixture))
                result = scope.inspect(ROOT / "research/PREREG_v6.json", receipts, scope.timestamp("2026-10-22T00:00:00Z"))
                self.assertEqual(result["measurement_status"], "UNMEASURED")
                self.assertFalse(result["measured_score_statements_allowed"])

    def test_text_gate_checks_both_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            sources = [Path(temp) / "main.tex", Path(temp) / "draft.md"]
            for path in sources:
                path.write_text("Final source")
            command = [sys.executable, "-I", str(ROOT / "tools/submission_text_gate.py"), *map(str, sources)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            sources[1].write_text("Working draft")
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)


if __name__ == "__main__":
    unittest.main()
