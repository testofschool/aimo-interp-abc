#!/usr/bin/env python3
"""Regression checks for the v6 parsing choices and exact-binomial power."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("identifiability", Path(__file__).with_name("leaderboard_identifiability.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def score(task, key, value):
    return {"task_id": task, "column_key": key, "score": str(value)}


def scores(task, accuracy, coverage, invalid):
    return [score(task, key, value) for key, value in
            (("accuracy", accuracy), ("coverage", coverage), ("invalid_predictions", invalid))]


def sub(sid, task_scores):
    return {"id": sid, "owner": f"private-test-owner-{sid}", "scores": task_scores}


class IdentifiabilityTests(unittest.TestCase):
    def parse(self, submissions):
        return audit.parse_snapshot([{"id": 30038, "count": len(submissions), "submissions": submissions}])

    def test_duplicate_scores_and_dual_task_do_not_inflate_trials(self):
        original = scores(36241, .64, 1, 0)
        rows, receipt = self.parse([sub(1, original + original + scores(36237, .52, 1, 0))])
        self.assertEqual(len(rows), 2)
        self.assertEqual(receipt["repeated_score_records_removed"], 3)
        self.assertEqual(receipt["submissions_scored_on_both_tasks"], 1)

    def test_registered_conflict_uses_entire_coverage_zero_set(self):
        rows, receipt = self.parse([sub(991917, scores(36237, 0, 0, 21) + scores(36237, .52, 1, 0))])
        self.assertEqual((rows[0]["accuracy"], rows[0]["coverage"], rows[0]["invalid_predictions"]), (0, 0, 21))
        self.assertEqual(len(receipt["conflicts"]), 1)
        with self.assertRaisesRegex(ValueError, "unregistered conflicting"):
            self.parse([sub(2, scores(36237, 0, 0, 21) + scores(36237, .52, 1, 0))])

    def test_denominator_jointly_uses_invalid_items_and_coverage(self):
        rows, _ = self.parse([sub(1, scores(36241, .64, 1, 0)), sub(2, scores(36241, .43, .5, 7))])
        self.assertEqual(audit.smallest_denominator(rows), 14)
        self.assertEqual(audit.integer_from_display(rows[1]["accuracy"], 14), 6)

    def test_coverage_zero_is_excluded_from_owner_and_trial_counts(self):
        rows, _ = self.parse([sub(1, scores(36241, .64, 1, 0)), sub(2, scores(36241, 0, 0, 14))])
        numbers, summary = audit.summarize_track(rows)
        self.assertEqual(numbers["owners_scored"], 1)
        self.assertEqual(numbers["scored_submissions"], 1)
        self.assertEqual(summary["owners_by_adjusted_p"][0]["visible_scored_submissions"], 1)
        self.assertNotIn("private-test-owner", str(summary))

    def test_exact_power_has_discrete_dips_and_certified_sustained_threshold(self):
        numbers, _ = audit.power_numbers()
        self.assertEqual([numbers[f"power_n80_{kind}_{effect}"] for effect in ("acc060", "acc065")
                          for kind in ("first", "sustained")], [158, 169, 69, 76])
        self.assertLess(audit.exact_power(168, .60), .8)
        self.assertLess(audit.exact_power(75, .65), .8)

    def test_hash_mismatch_fails_before_parsing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lb1.json"
            path.write_text("not JSON")
            with self.assertRaisesRegex(ValueError, "STOP:.*hash"):
                audit.checked_bytes(path, audit.SNAPSHOT_SHA256["lb1.json"])

    def test_future_manifest_is_explicit_and_cannot_override_frozen_pins(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "lb1.json").write_text("{}")
            path = root / "manifest.json"
            manifest = {"snapshot_label": "2026-10-31", "phase_id": 30038,
                        "sha256": {"lb1.json": "a" * 64}}
            path.write_text(json.dumps(manifest))
            self.assertEqual(audit.snapshot_hashes(root, path), ("2026-10-31", manifest["sha256"]))
            manifest["snapshot_label"] = "2026-10-19"
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "cannot override"):
                audit.snapshot_hashes(root, path)


if __name__ == "__main__":
    unittest.main()
