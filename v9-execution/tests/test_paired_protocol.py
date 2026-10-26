#!/usr/bin/env python3
"""Synthetic protocol tests; no fixture is an actual competition score."""
from fractions import Fraction
from itertools import product
import importlib.util
import math
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("paired_protocol", HERE / "paired_protocol.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


CONTRACT = {"same_evaluation_items": True, "unweighted_binary_accuracy": True,
            "probe_coverage": 1.0, "control_coverage": 1.0,
            "probe_invalid_predictions": 0, "control_invalid_predictions": 0}


class PairedProtocolTests(unittest.TestCase):
    def test_exact_known_discordance_edges(self):
        self.assertEqual(p.exact_mcnemar_fraction(0, 0), Fraction(1))
        self.assertEqual(p.exact_mcnemar_fraction(0, 3), Fraction(1, 4))
        self.assertEqual(p.exact_mcnemar_fraction(0, 7), Fraction(1, 64))
        self.assertEqual(p.exact_mcnemar_fraction(2, 2), Fraction(1))
        self.assertEqual(p.exact_mcnemar_fraction(1, 7), Fraction(9, 128))

    def test_two_sided_symmetry_and_null_reference(self):
        for b in range(15):
            for c in range(15):
                value = p.exact_mcnemar_fraction(b, c)
                self.assertEqual(value, p.exact_mcnemar_fraction(c, b))
                self.assertLessEqual(value, 1)
                self.assertGreater(value, 0)

    def test_joint_counts_sum_and_difference(self):
        result = p.from_joint_counts(4, 6, 1, 3)
        self.assertEqual((result['n'], result['probe_correct'], result['control_correct']), (14, 10, 5))
        self.assertEqual(result['discordant_items'], 7)
        self.assertFalse(result['equivalence_claim_allowed'])
        self.assertFalse(result['causal_signal_ablation_claim_allowed'])

    def test_same_totals_do_not_identify_pairing(self):
        result = p.from_aggregate_counts(14, 10, 5)
        self.assertEqual(len(result['feasible_tables']), 5)
        self.assertFalse(result['point_pvalue_identified'])
        self.assertEqual(result['pvalue_min_fraction'], '1/16')
        self.assertEqual(result['pvalue_max_fraction'], '1093/4096')
        self.assertEqual(result['decision'], 'NO_FEASIBLE_PAIRING_REJECTS_REFERENCE_NULL')

    def test_aggregate_tables_cover_every_binary_pairing(self):
        # Independent exhaustive sequence oracle, not the overlap-range formula.
        for n in range(1, 5):
            observed = {}
            for states in product(range(4), repeat=n):
                a, b, c, d = (states.count(i) for i in range(4))
                observed.setdefault((a + b, a + c), set()).add((a, b, c, d))
            for (kp, kc), expected in observed.items():
                result = p.from_aggregate_counts(n, kp, kc)
                actual = {tuple(t[k] for k in ('both_correct','probe_only','control_only','both_wrong')) for t in result['feasible_tables']}
                self.assertEqual(actual, expected)

    def test_partial_identification_can_have_robust_rejection(self):
        result = p.from_aggregate_counts(14, 14, 7)
        self.assertEqual(len(result['feasible_tables']), 1)
        self.assertEqual(result['pvalue_max_fraction'], '1/64')
        self.assertTrue(result['reject_for_all_feasible_pairings'])

    def test_partial_identification_can_cross_alpha(self):
        result = p.from_aggregate_counts(14, 10, 4)
        self.assertLessEqual(result['pvalue_min'], .05)
        self.assertGreater(result['pvalue_max'], .05)
        self.assertEqual(result['decision'], 'DECISION_DEPENDS_ON_UNOBSERVED_PAIRING')

    def test_equal_total_counts_are_not_equivalence(self):
        result = p.analyze(14, 7, 7)
        self.assertEqual(result['primary']['pvalue_min'], 1)
        self.assertEqual(result['primary']['pvalue_max'], 1)
        self.assertFalse(result['primary']['equivalence_claim_allowed'])
        self.assertEqual(result['secondary']['status'], 'UNMEASURED')

    def test_binary_predictions_with_totals_recover_joint_counts(self):
        probe = {str(i): i < 10 for i in range(14)}
        control = {str(i): i < 4 or i == 10 for i in range(14)}
        result = p.from_binary_predictions(probe, control, 10, 5, validated_contract=CONTRACT)
        self.assertEqual(result['table'], {'both_correct': 4, 'probe_only': 6, 'control_only': 1, 'both_wrong': 3})

    def test_binary_prediction_alignment_or_invalid_fails(self):
        with self.assertRaises(ValueError): p.from_binary_predictions({'a': True}, {'b': True}, 1, 1, validated_contract=CONTRACT)
        with self.assertRaises(ValueError): p.from_binary_predictions({'a': None}, {'a': True}, 1, 1, validated_contract=CONTRACT)
        with self.assertRaises(ValueError): p.from_binary_predictions({'a': True}, {'a': False}, 0, 0, validated_contract=CONTRACT)
        with self.assertRaises(ValueError): p.from_binary_predictions({'a': True}, {'a': True}, 1, 0, validated_contract=CONTRACT)

    def test_binary_prediction_contract_cannot_be_assumed(self):
        with self.assertRaises(ValueError): p.from_binary_predictions({'a': True}, {'a': True}, 1, 1)
        for key, value in [("same_evaluation_items", False), ("unweighted_binary_accuracy", False),
                           ("probe_coverage", .9), ("control_coverage", True),
                           ("probe_invalid_predictions", 1), ("control_invalid_predictions", False)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                contract = dict(CONTRACT);contract[key] = value
                p.from_binary_predictions({'a': True}, {'a': True}, 1, 1, validated_contract=contract)

    def test_invalid_counts_and_alpha_fail(self):
        for args in [(0,0,0), (14,15,7), (14,-1,7), (14,True,7), (14,7.0,7)]:
            with self.subTest(args=args), self.assertRaises(ValueError): p.from_aggregate_counts(*args)
        for alpha in (0, 1, float('nan'), True):
            with self.subTest(alpha=alpha), self.assertRaises(ValueError): p.from_joint_counts(1,1,1,1,alpha)

    def test_exact_power_threshold_all_discordant_one_direction(self):
        self.assertEqual(p.paired_power(5, 1, 0), 0)
        self.assertEqual(p.paired_power(6, 1, 0), 1)
        result = p.first_n_for_power(1, 0, max_n=10)
        self.assertEqual(result['first_n'], 6)

    def test_power_mixture_matches_direct_multinomial_enumeration(self):
        for n in (6, 7):
            pa, pb, pc = .5, .3, .2  # concordant, probe-only, control-only
            expected = 0
            for states in product(range(3), repeat=n):
                m = states.count(1) + states.count(2)
                reject = m >= 6 and (states.count(1) == 0 or states.count(2) == 0)
                if reject:
                    expected += math.prod((pa,pb,pc)[s] for s in states)
            self.assertAlmostEqual(p.paired_power(n, pb, pc), expected, places=13)

    def test_null_model_power_is_size_bounded_not_eighty_percent(self):
        self.assertLessEqual(p.paired_power(50, .25, .25), .05 + 1e-12)
        self.assertIsNone(p.first_n_for_power(.25, .25)['first_n'])

    def test_power_symmetry_and_probability_edges(self):
        self.assertAlmostEqual(p.paired_power(25, .4, .1), p.paired_power(25, .1, .4), places=13)
        self.assertEqual(p.paired_power(14, 0, 0), 0)
        with self.assertRaises(ValueError): p.paired_power(14, .8, .3)
        with self.assertRaises(ValueError): p.paired_power(14, float('nan'), 0)
        with self.assertRaises(ValueError): p.first_n_for_power(.3, .1, max_n=2001)

    def test_joint_must_match_validated_score_totals(self):
        with self.assertRaises(ValueError):
            p.analyze(14, 10, 5, {'both_correct': 4, 'probe_only': 5, 'control_only': 1, 'both_wrong': 4})

    def test_search_limit_is_censored_not_impossible(self):
        result = p.first_n_for_power(.2, .1, max_n=5)
        self.assertEqual(result['status'], 'RIGHT_CENSORED_NO_CROSSING_WITHIN_SEARCH')
        self.assertIsNone(result['first_n'])


if __name__ == '__main__': unittest.main()
