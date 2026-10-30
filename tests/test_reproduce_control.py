"""Control provenance failures and numerical/packaging reproduction checks."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("reproduce_control", ROOT / "tools/reproduce_control.py")
control = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(control)
TRAIN = ROOT / "data/train-main-v2.parquet"
BUNDLE = ROOT / "bundles/solution-text-length-control-small.zip"


class ReproductionTests(unittest.TestCase):
    def test_feature_recipe_preserves_unicode_digits(self):
        x = control.features(["a١2", "abc"])
        np.testing.assert_allclose(x, [[np.log1p(3), 2], [np.log1p(3), 0]], rtol=0, atol=1e-15)

    def test_training_selector_excludes_nulls_without_hardcoded_cohort_size(self):
        table = pd.DataFrame({"problem": ["a", "b", "c", "d"],
                              "model_id": ["small", "openai/gpt-oss-120b", "small", "small"],
                              "is_robust": [True, False, None, True]})
        with patch.object(control.pd, "read_parquet", return_value=table):
            full, labelled = control.training_table(b"stub parquet")
        self.assertEqual(len(full), 4)
        self.assertEqual(len(labelled), 3)
        self.assertEqual(labelled.problem.tolist(), ["a", "b", "d"])
        self.assertIn("openai/gpt-oss-120b", labelled.model_id.tolist())

    def test_nonbinary_or_missing_training_schema_is_rejected(self):
        for table in (pd.DataFrame({"problem": ["a"]}),
                      pd.DataFrame({"problem": ["a"], "model_id": ["small"], "is_robust": ["yes"]})):
            with self.subTest(columns=table.columns.tolist()):
                with patch.object(control.pd, "read_parquet", return_value=table):
                    with self.assertRaises(ValueError):
                        control.training_table(b"stub")

    def test_corrupted_hash_fails_before_any_pickle_load(self):
        with tempfile.TemporaryDirectory() as directory:
            bad = Path(directory) / "train-main-v2.parquet"
            bad.write_bytes(b"corrupted")
            with patch.object(control.joblib, "load", side_effect=AssertionError("pickle must not load")) as load:
                with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                    control.reproduce(bad, BUNDLE)
            load.assert_not_called()

    def test_changed_estimator_is_detected_by_actual_parameters(self):
        problems = ["1", "22", "abc", "1234", "abcdef", "12345678"]
        model = control.estimator().fit(control.features(problems), [0, 1, 0, 1, 0, 1])
        changed = copy.deepcopy(model)
        changed.intercept_[0] += 0.01
        with self.assertRaisesRegex(ValueError, "intercept_max_abs_difference"):
            control.compare_models(model, changed, problems)

    def test_model_class_order_and_parameter_mismatches_are_rejected(self):
        problems = ["1", "22", "abc", "1234"]
        model = control.estimator().fit(control.features(problems), [0, 1, 0, 1])
        changed = copy.deepcopy(model)
        changed.classes_ = changed.classes_[::-1]
        with self.assertRaisesRegex(ValueError, "class order"):
            control.compare_models(model, changed, problems)
        changed = copy.deepcopy(model)
        changed.C = 2.0
        with self.assertRaisesRegex(ValueError, "parameter mismatch"):
            control.compare_models(model, changed, problems)

    def test_packaging_is_order_independent_with_fixed_metadata(self):
        payloads = {"solution.py": b"public code", "small.txt": b"", "artifacts/text_length.joblib": b"artifact"}
        first = control.deterministic_zip(payloads)
        second = control.deterministic_zip(dict(reversed(list(payloads.items()))))
        self.assertEqual(first, second)
        with zipfile.ZipFile(io.BytesIO(first)) as archive:
            self.assertEqual(archive.namelist(), sorted(payloads))
            for info in archive.infolist():
                self.assertEqual(info.date_time, (2020, 1, 1, 0, 0, 0))
                self.assertEqual(info.create_system, 3)
                self.assertEqual(info.external_attr, 2175008768)
                self.assertEqual(archive.read(info), payloads[info.filename])

    def test_unexpected_bundle_member_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unexpected Small bundle members"):
            control.deterministic_zip({"../../outside": b"bad"})

    def test_cli_outputs_cannot_overwrite_inputs(self):
        before = BUNDLE.read_bytes()
        with patch.object(control, "reproduce", side_effect=AssertionError("must stop before fit")) as fit:
            with patch("sys.stdout", new_callable=io.StringIO) as output:
                code = control.main(["--out", str(BUNDLE)])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output.getvalue())["status"], "FAIL")
        self.assertEqual(BUNDLE.read_bytes(), before)
        fit.assert_not_called()

    @unittest.skipUnless(TRAIN.exists(), "pinned public parquet must be obtained separately")
    def test_tampered_bundle_fails_before_pickle_load(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / "changed.zip"
            bundle.write_bytes(BUNDLE.read_bytes() + b"tampered")
            with patch.object(control.joblib, "load", side_effect=AssertionError("untrusted pickle")) as load:
                with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                    control.reproduce(TRAIN, bundle)
            load.assert_not_called()

    @unittest.skipUnless(TRAIN.exists(), "pinned public parquet must be obtained separately")
    def test_actual_refit_and_packaging_with_separate_cohort_scopes(self):
        train_before, bundle_before = TRAIN.read_bytes(), BUNDLE.read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            with patch("subprocess.run", side_effect=AssertionError("no external process")), \
                    patch("urllib.request.urlopen", side_effect=AssertionError("no network")):
                result = control.reproduce(TRAIN, BUNDLE, target / "refit.joblib", target / "repacked.zip")
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["rows"], {"public_total": 94, "labelled_fit": 80, "unlabelled_excluded": 14,
                                               "fit_distinct_problems": 33, "small_labelled": 43, "small_distinct_problems": 22})
            self.assertEqual(result["parity"]["prediction_rows"], 94)
            self.assertTrue(result["parity"]["threshold_prediction_equal"])
            self.assertTrue(result["packaging"]["identical_to_submitted_zip"])
            self.assertEqual((target / "repacked.zip").read_bytes(), bundle_before)
            self.assertTrue((target / "refit.joblib").is_file())
        self.assertEqual(TRAIN.read_bytes(), train_before)
        self.assertEqual(BUNDLE.read_bytes(), bundle_before)


if __name__ == "__main__":
    unittest.main()
