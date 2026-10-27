#!/usr/bin/env python3
"""Missing metrics cannot impersonate the explicitly unavailable paired N80."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('report_numbers', Path(__file__).resolve().parents[1] / 'tools/report_numbers.py')
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)


class ClaimCheckTests(unittest.TestCase):
    def claim(self, key, value):
        return [{'text': 'registered measurement state', 'key': key, 'value': value}]

    def test_explicit_unavailable_measurement_is_valid(self):
        self.assertEqual(report.claim_mismatches({'N80': None}, self.claim('N80', None)), [])

    def test_missing_measurement_is_not_an_explicit_null(self):
        bad = report.claim_mismatches({}, self.claim('N80', None))
        self.assertEqual(len(bad), 1)
        self.assertTrue(bad[0]['missing_key'])

    def test_missing_nested_measurement_is_rejected(self):
        bad = report.claim_mismatches({'power': {}}, self.claim('power.N80', None))
        self.assertTrue(bad[0]['missing_key'])

    def test_numeric_mismatch_still_rejected(self):
        self.assertEqual(len(report.claim_mismatches({'p': 1}, self.claim('p', 0.01))), 1)


if __name__ == '__main__':
    unittest.main()
