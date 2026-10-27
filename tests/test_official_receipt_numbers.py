"""Aggregate-only validation tests; mutations are never competition receipts."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replace_at(record, path, value):
    target = record
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value


class OfficialReceiptNumbersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module("official_receipt_numbers_tested", ROOT / "tools/official_receipt_numbers.py")
        cls.protocol = load_module("paired_protocol_for_official_tests", ROOT / "v9-execution/paired_protocol.py")
        scores = json.loads((ROOT / "v9-execution/SCORES.json").read_text())
        native = json.loads((ROOT / "v9-execution/NATIVE_OUTPUT_CHECK.json").read_text())
        ablation = json.loads((ROOT / "v9-execution/ABLATION.json").read_text())
        cls.previous_relative = native["input_receipts_snapshots"]["v9-execution/SCORES.json"]["snapshot"]
        previous = json.loads((ROOT / cls.previous_relative).read_text())
        cls.base = (scores, native, ablation, previous)

    def validate(self, records=None):
        return self.module.validate_records(*(records or copy.deepcopy(self.base)), self.protocol)

    def reject_changes(self, changes):
        records = copy.deepcopy(self.base)
        for record_index, path, value in changes:
            replace_at(records[record_index], path, value)
        with self.assertRaises(ValueError):
            self.validate(records)

    def test_current_aggregate_receipts_produce_33_numbers(self):
        numbers = self.validate()
        self.assertEqual(len(numbers), 33)
        self.assertEqual(numbers["official_probe_control_exact_p"], 1)
        self.assertIsNone(numbers["official_probe_control_n80"])

    def test_native_api_score_mismatch_is_rejected(self):
        self.reject_changes([(0, ["runs", 2, "native_receipt", "scores", 0, "score"], "0.6000000000")])

    def test_previous_receipt_cannot_be_reassociated_with_another_owner(self):
        self.reject_changes([(3, ["runs", 2, "native_receipt", "owner"], "another-owner")])

    def test_wrong_task_or_phase_is_rejected(self):
        for path, value in [(["task_id"], 36237), (["phase_id"], 1), (["competition_id"], 1)]:
            with self.subTest(path=path):
                self.reject_changes([(0, path, value)])
        self.reject_changes([(1, ["runs", 2, "native_small_task"], 36237)])

    def test_wrong_bundle_association_is_rejected(self):
        self.reject_changes([(0, ["runs", 1, "sha256"], "0" * 64)])
        self.reject_changes([(1, ["runs", 1, "zips", "submitted-bundle.zip", "sha256"], "0" * 64)])

    def test_archive_integrity_failure_is_rejected(self):
        for key in ["crc_ok", "unique_safe_paths"]:
            with self.subTest(key=key):
                self.reject_changes([(1, ["runs", 2, "zips", "prediction_result.zip", key], False)])

    def test_missing_count_or_binary_validity_proof_is_rejected(self):
        changes = [
            (["prediction_rows"], 13),
            (["unique_ids"], 13),
            (["all_prediction_rows_valid_binary"], False),
            (["summary_cases"], 15),
            (["summary_invalid_predictions"], 1),
            (["summary_timeouts"], 1),
            (["summary_skipped"], 1),
            (["native_scoring_json_matches_api"], False),
            (["N"], 15),
            (["k"], 8),
        ]
        for suffix, value in changes:
            with self.subTest(suffix=suffix):
                self.reject_changes([(1, ["runs", 2] + suffix, value)])

    def test_unweighted_binary_contract_is_required(self):
        self.reject_changes([(1, ["scorer_contract", "unweighted_binary_accuracy"], False)])
        self.reject_changes([(1, ["same_real_item_id_sets_all_three"], False)])
        self.reject_changes([(2, ["validated_score_contract", "unweighted_binary_accuracy"], False)])

    def test_stored_correct_total_cannot_override_native_proof(self):
        self.reject_changes([(0, ["runs", 2, "k"], 8)])
        self.reject_changes([(0, ["runs", 2, "N"], 16)])

    def test_joint_table_margins_must_match_native_totals(self):
        self.reject_changes([(2, ["primary", "table", "both_correct"], 2),
                             (2, ["primary", "table", "probe_only"], 5)])

    def test_discordance_total_must_match_the_joint_table(self):
        self.reject_changes([(2, ["primary", "discordant_items"], 6)])

    def test_exact_p_is_recomputed_instead_of_trusting_reported_significance(self):
        self.reject_changes([(2, ["primary", "pvalue"], 0.04),
                             (2, ["primary", "pvalue_fraction"], "1/25"),
                             (2, ["primary", "reject_reference_null"], True),
                             (2, ["pvalue"], 0.04)])

    def test_zero_directional_effect_does_not_get_a_fabricated_n80(self):
        self.reject_changes([(2, ["N80"], 76),
                             (2, ["secondary_paired_n80", "first_n"], 76),
                             (2, ["secondary_paired_n80", "status"], "HYPOTHETICAL_MODEL_FIRST_CROSSING")])

    def test_exact_finish_time_is_not_inferred_from_an_observation(self):
        fake = "2026-10-27T18:44:15.357184+09:00"
        self.reject_changes([(0, ["runs", 2, "finished_time_KST"], fake)])
        self.reject_changes([(0, ["runs", 2, "finished_time_KST"], fake),
                             (1, ["runs", 2, "native_exact_finished_time"], fake)])

    def test_preregistration_cannot_be_backdated_by_a_status_label(self):
        future = "2026-10-28T01:03:42+09:00"
        self.reject_changes([(1, ["prereg_chronology", "prereg_commit_time_KST"], future),
                             (2, ["prereg_chronology", "prereg_commit_time_KST"], future)])

    def test_nonsignificance_cannot_be_promoted_to_equivalence(self):
        self.reject_changes([(2, ["reporting", "black_box_sufficiency_claim_allowed"], True)])
        self.reject_changes([(2, ["primary", "equivalence_claim_allowed"], True)])

    def copy_reproduction_inputs(self, temporary_root):
        paths = set(self.module.SOURCE_SHA256)
        paths.update(item["snapshot"] for item in self.base[1]["input_receipts_snapshots"].values())
        for relative in paths:
            destination = temporary_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)

    def test_loader_accepts_pinned_aggregate_only_reproduction(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            self.copy_reproduction_inputs(temporary_root)
            state = self.module.inspect(root=temporary_root)
            self.assertTrue(state["measured_score_statements_allowed"], state["errors"])
            self.assertEqual(len(self.module.numbers(state)), 33)

    def test_loader_rejects_changed_source_bytes_even_when_json_is_equivalent(self):
        # Appending whitespace preserves JSON semantics but breaks the source pin.
        for relative in ["v9-execution/SCORES.json", "v9-execution/NATIVE_OUTPUT_CHECK.json", "v9-execution/ABLATION.json"]:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                temporary_root = Path(directory)
                self.copy_reproduction_inputs(temporary_root)
                path = temporary_root / relative
                path.write_bytes(path.read_bytes() + b"\n")
                state = self.module.inspect(root=temporary_root)
                self.assertFalse(state["measured_score_statements_allowed"])
                self.assertTrue(state["errors"])
                with self.assertRaises(ValueError):
                    self.module.numbers(state)


if __name__ == "__main__":
    unittest.main()
