#!/usr/bin/env python3
"""Synthetic rendering-gate regression tests; no owner/service observations."""
from contextlib import redirect_stdout
from datetime import datetime, timezone
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("report_renderer", ROOT / "tools/render_report.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


class OwnerPrivateRenderingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="aimo-synthetic-render-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "report").mkdir()
        (self.root / "research").mkdir()
        self.outline = self.root / "report/REPORT_OUTLINE.md"
        self.numbers = self.root / "numbers.json"
        self.output = self.root / "output.md"
        self.fallback = self.root / "report/OWNER_PRIVATE_VAL_UNMEASURED.md"
        self.fallback.write_bytes((ROOT / "report/OWNER_PRIVATE_VAL_UNMEASURED.md").read_bytes())
        self.fallback_text = self.fallback.read_text().strip()
        self.numbers.write_text(json.dumps({"public_count": 61, "owner_score": 0.5}))
        (self.root / "research/claims.json").write_text(json.dumps({"claims": [
            {"key": "public_count", "value": 61}, {"key": "owner_score", "value": 0.5}]}))
        self.receipts = self.root / "absent-owner-receipts.json"
        self.now = datetime(2026, 10, 22, tzinfo=timezone.utc)

    def document(self, candidate="Injected private accuracy 0.9 must not survive without receipts."):
        self.outline.write_text("# Synthetic report\n\n## 2. Public analysis\n\nPublic owners: {{public_count}}.\n\n"
                                "## 4. Supporting controls\n\nPublic support stays unchanged.\n\n"
                                + renderer.OWNER_BEGIN + "\n" + candidate + "\n" + renderer.OWNER_END
                                + "\n\nUnrelated public limitation stays unchanged.\n\n## 5. Limitations\n\nPublic end.\n")

    def render(self):
        captured = io.StringIO()
        with redirect_stdout(captured):
            exit_code = renderer.main(str(self.outline), str(self.numbers), str(self.output),
                                      owner_receipts=self.receipts, owner_now=self.now)
        return exit_code, json.loads(captured.getvalue())

    def valid_synthetic_receipts(self):
        fixture = json.loads((ROOT / "tests/fx_match.json").read_text())
        for index, row in enumerate(fixture["receipts"]):
            row.update(submission_id=str(9000 + index), screenshot="synthetic-evidence.txt")
        (self.root / "synthetic-evidence.txt").write_text("SYNTHETIC TEST EVIDENCE; no service screenshot")
        self.receipts = self.root / "synthetic-owner-receipts.json"
        self.receipts.write_text(json.dumps(fixture))

    def test_missing_receipts_replace_only_owner_block(self):
        self.document()
        code, result = self.render()
        self.assertEqual(code, 0)
        text = self.output.read_text()
        self.assertIn(self.fallback_text, text)
        self.assertNotIn("Injected private accuracy", text)
        self.assertNotIn("OWNER_PRIVATE_VALIDATION", text)
        for expected in ["Public owners: 61.", "Public support stays unchanged.",
                         "Unrelated public limitation stays unchanged.", "Public end."]:
            self.assertIn(expected, text)
        self.assertEqual(result["owner_private_validation"]["rendered_variant"], "canonical_unmeasured")

    def test_expired_deadline_keeps_missing_receipts_unmeasured(self):
        self.document()
        self.now = datetime(2026, 11, 1, 11, 55, tzinfo=timezone.utc)
        code, result = self.render()
        self.assertEqual(code, 0)
        self.assertTrue(result["owner_private_validation"]["render_gate_expired"])
        self.assertEqual(result["owner_private_validation"]["measurement_status"], "UNMEASURED")
        self.assertNotIn("Injected private accuracy", self.output.read_text())

    def test_valid_strict_receipts_allow_registered_candidate(self):
        self.valid_synthetic_receipts()
        self.document("Recorded owner accuracy: {{owner_score}}.")
        code, result = self.render()
        self.assertEqual(code, 0)
        self.assertIn("Recorded owner accuracy: 0.5.", self.output.read_text())
        self.assertNotIn(self.fallback_text, self.output.read_text())
        self.assertEqual(result["owner_private_validation"]["rendered_variant"], "recorded_owner_scores")
        self.assertFalse(result["owner_private_validation"]["per_problem_balance_inference_allowed"])

    def test_guarded_candidate_still_requires_numeric_registry(self):
        self.valid_synthetic_receipts()
        for candidate in ["Owner accuracy 0.9.", "Owner accuracy {{unknown_score}}."]:
            with self.subTest(candidate=candidate):
                self.document(candidate)
                code, result = self.render()
                self.assertEqual(code, 1)
                self.assertEqual(result["result"], "FAIL")
                self.assertTrue(result["errors"])

    def test_structure_errors_are_explicit(self):
        self.document()
        original = self.outline.read_text()
        mutations = [original.replace(renderer.OWNER_BEGIN, ""),
                     original.replace(renderer.OWNER_END, ""),
                     original.replace(renderer.OWNER_BEGIN, renderer.OWNER_BEGIN * 2),
                     original.replace("## 4. Supporting controls", "## 3. Supporting controls"),
                     original.replace(renderer.OWNER_BEGIN, "TEMP").replace(renderer.OWNER_END, renderer.OWNER_BEGIN).replace("TEMP", renderer.OWNER_END)]
        for source in mutations:
            with self.subTest(source=source):
                self.outline.write_text(source)
                code, result = self.render()
                self.assertEqual(code, 1)
                self.assertIn("configuration error", result["errors"][0])
        self.outline.write_text(original)
        self.fallback.unlink()
        code, result = self.render()
        self.assertEqual(code, 1)
        self.assertIn("fallback is missing", result["errors"][0])

    def test_historical_v5_outline_stays_markerless(self):
        self.outline = self.outline.with_name("PREREGISTERED_OUTLINE_v5.md")
        self.outline.write_text("Historical public owners: {{public_count}}.\n")
        code, result = self.render()
        self.assertEqual(code, 0)
        self.assertEqual(self.output.read_text(), "Historical public owners: 61.\n")
        self.assertNotIn("owner_private_validation", result)

    def test_fallback_tampering_cannot_license_measured_claims(self):
        self.document()
        self.fallback.write_text("Owner private accuracy is 1.0 (fabricated synthetic injection).\n")
        code, result = self.render()
        self.assertEqual(code, 1)
        self.assertIn("fallback hash mismatch", result["errors"][0])
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(OwnerPrivateRenderingTests)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    print(json.dumps({"result": "PASS" if result.wasSuccessful() else "FAIL",
                      "scope": "SYNTHETIC renderer cases only; no owner or service measurements",
                      "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
                      "details": stream.getvalue()}, indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)
