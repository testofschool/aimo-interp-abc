"""Source-selection tests with explicit synthetic scope modules, no private data."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


class OfficialReceiptRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("renderer_for_official_tests", ROOT / "tools/render_report.py")
        cls.renderer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.renderer)

    def prepare(self, temporary_root):
        (temporary_root / "report").mkdir()
        (temporary_root / "tools").mkdir()
        shutil.copyfile(ROOT / "report/OWNER_PRIVATE_VAL_UNMEASURED.md",
                        temporary_root / "report/OWNER_PRIVATE_VAL_UNMEASURED.md")
        return temporary_root / "report/fixture.md"

    def stub(self, temporary_root, name, *, allowed, source):
        state = {
            "measured_score_statements_allowed": allowed,
            "measurement_status": "SYNTHETIC_ALLOWED" if allowed else "SYNTHETIC_MISSING",
            "source": source,
            "native_owner_receipt_verified": allowed,
            "errors": [] if allowed else ["synthetic invalid receipt source"],
        }
        (temporary_root / "tools" / (name + ".py")).write_text(
            "def inspect(*args, **kwargs):\n    return " + repr(state) + "\n")

    @staticmethod
    def template(key, section="Appendix A — reference observations", extra=""):
        return ("## " + section + "\n\n" + extra + "\n" +
                "<!-- BEGIN_OWNER_PRIVATE_VALIDATION -->\n" +
                "Authored observation {{" + key + "}}.\n" +
                "<!-- END_OWNER_PRIVATE_VALIDATION -->\n\n## References\n")

    def test_explicit_official_placeholder_selects_official_source(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            outline = self.prepare(temporary_root)
            self.stub(temporary_root, "official_receipt_numbers", allowed=True, source="SYNTHETIC_OFFICIAL")
            text = self.template("official_trained_probe_k")
            with patch.object(self.renderer, "ROOT", temporary_root):
                rendered, state = self.renderer.owner_private_validation(text, outline)
            self.assertIn("Authored observation", rendered)
            self.assertEqual(state["source"], "SYNTHETIC_OFFICIAL")
            self.assertEqual(state["rendered_variant"], "recorded_owner_scores")

    def test_invalid_official_source_raises_instead_of_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            outline = self.prepare(temporary_root)
            self.stub(temporary_root, "official_receipt_numbers", allowed=False, source="SYNTHETIC_OFFICIAL")
            with patch.object(self.renderer, "ROOT", temporary_root), self.assertRaises(ValueError):
                self.renderer.owner_private_validation(self.template("official_trained_probe_k"), outline)

    def test_unknown_official_prefix_still_selects_official_source(self):
        # Key registration is checked later by main(); an unknown official key
        # must not select the historical owner/UNMEASURED branch first.
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            outline = self.prepare(temporary_root)
            self.stub(temporary_root, "official_receipt_numbers", allowed=True, source="SYNTHETIC_OFFICIAL")
            with patch.object(self.renderer, "ROOT", temporary_root):
                rendered, state = self.renderer.owner_private_validation(
                    self.template("official_misspelled_namespace_k"), outline)
            self.assertEqual(state["source"], "SYNTHETIC_OFFICIAL")
            self.assertIn("{{official_misspelled_namespace_k}}", rendered)

    def test_official_placeholder_without_markers_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            outline = self.prepare(temporary_root)
            self.stub(temporary_root, "official_receipt_numbers", allowed=True, source="SYNTHETIC_OFFICIAL")
            text = "## Appendix A\n\nOfficial result {{official_trained_probe_k}}.\n"
            with patch.object(self.renderer, "ROOT", temporary_root), self.assertRaises(ValueError):
                self.renderer.owner_private_validation(text, outline)

    def test_missing_official_source_raises_instead_of_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            outline = self.prepare(temporary_root)
            with patch.object(self.renderer, "ROOT", temporary_root), self.assertRaises((OSError, ValueError)):
                self.renderer.owner_private_validation(self.template("official_trained_probe_k"), outline)

    def test_official_block_must_be_in_appendix_a(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            outline = self.prepare(temporary_root)
            self.stub(temporary_root, "official_receipt_numbers", allowed=True, source="SYNTHETIC_OFFICIAL")
            with patch.object(self.renderer, "ROOT", temporary_root), self.assertRaises(ValueError):
                self.renderer.owner_private_validation(self.template("official_trained_probe_k", section="4. Old owner results"), outline)

    def test_queue_only_outline_retains_its_queue_source(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            outline = self.prepare(temporary_root)
            self.stub(temporary_root, "queue_receipt_scope_v83", allowed=True, source="SYNTHETIC_QUEUE")
            with patch.object(self.renderer, "ROOT", temporary_root):
                _, state = self.renderer.owner_private_validation(self.template("queue_always_true_k"), outline)
            self.assertEqual(state["source"], "SYNTHETIC_QUEUE")

    def test_bad_queue_source_still_blocks_queue_rendering(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            outline = self.prepare(temporary_root)
            self.stub(temporary_root, "queue_receipt_scope_v83", allowed=False, source="SYNTHETIC_QUEUE")
            with patch.object(self.renderer, "ROOT", temporary_root), self.assertRaises(ValueError):
                self.renderer.owner_private_validation(self.template("queue_always_true_k"), outline)

    def test_mixed_official_and_queue_require_both_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            outline = self.prepare(temporary_root)
            self.stub(temporary_root, "official_receipt_numbers", allowed=True, source="SYNTHETIC_OFFICIAL")
            self.stub(temporary_root, "queue_receipt_scope_v83", allowed=False, source="SYNTHETIC_QUEUE")
            mixed = self.template("official_trained_probe_k", extra="Historical {{queue_always_true_k}}")
            with patch.object(self.renderer, "ROOT", temporary_root), self.assertRaises(ValueError):
                self.renderer.owner_private_validation(mixed, outline)

    def test_mixed_valid_sources_preserve_official_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            outline = self.prepare(temporary_root)
            self.stub(temporary_root, "official_receipt_numbers", allowed=True, source="SYNTHETIC_OFFICIAL")
            self.stub(temporary_root, "queue_receipt_scope_v83", allowed=True, source="SYNTHETIC_QUEUE")
            mixed = self.template("official_probe_control_exact_p", extra="Historical {{queue_always_true_k}}")
            with patch.object(self.renderer, "ROOT", temporary_root):
                rendered, state = self.renderer.owner_private_validation(mixed, outline)
            self.assertIn("Historical {{queue_always_true_k}}", rendered)
            self.assertEqual(state["source"], "SYNTHETIC_OFFICIAL")


if __name__ == "__main__":
    unittest.main()
