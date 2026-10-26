#!/usr/bin/env python3
"""Pre-score paired comparison helpers; no network, model execution, or score fetching.

The exact conditional reference is the two-sided Binomial(b+c, 1/2) test on
correctness discordances. Aggregate totals only identify a set of joint tables.
Power is a finite-sum calculation under an explicitly supplied iid joint model,
not a guarantee for correlated problem/model instances or a test of equivalence.
"""
import argparse
from fractions import Fraction
from functools import lru_cache
import json
import math
from pathlib import Path


SOURCES = [
    "https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html",
    "https://www.statsmodels.org/stable/_modules/statsmodels/stats/contingency_tables.html#mcnemar",
    "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html",
]


def _integer(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(name + " must be a nonnegative integer")
    return value


def _probability(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(name + " must be finite numeric data in [0, 1]")
    return float(value)


def _alpha(value):
    number = _probability(value, "alpha")
    if not 0 < number < 1:
        raise ValueError("alpha must be strictly between zero and one")
    return Fraction(str(number))


def exact_mcnemar_fraction(probe_only, control_only):
    """Exact arithmetic for the symmetric two-sided conditional p-value."""
    b = _integer(probe_only, "probe_only")
    c = _integer(control_only, "control_only")
    m = b + c
    if not m:
        return Fraction(1)
    lower = sum(math.comb(m, j) for j in range(min(b, c) + 1))
    return min(Fraction(1), Fraction(2 * lower, 2 ** m))


def from_joint_counts(both_correct, probe_only, control_only, both_wrong, alpha=0.05):
    counts = [_integer(v, name) for name, v in zip(
        ("both_correct", "probe_only", "control_only", "both_wrong"),
        (both_correct, probe_only, control_only, both_wrong))]
    a, b, c, d = counts
    n = sum(counts)
    if not n:
        raise ValueError("at least one common scored item is required")
    exact = exact_mcnemar_fraction(b, c)
    return {
        "mode": "PAIRED_EXACT_CONDITIONAL_MCNEMAR",
        "table": {"both_correct": a, "probe_only": b, "control_only": c, "both_wrong": d},
        "n": n, "probe_correct": a + b, "control_correct": a + c,
        "accuracy_difference_probe_minus_control": (b - c) / n,
        "discordant_items": b + c, "pvalue": float(exact),
        "pvalue_fraction": str(exact), "alpha": float(_alpha(alpha)),
        "reject_reference_null": exact <= _alpha(alpha),
        "independence_status": "CONDITIONAL_REFERENCE_ASSUMPTION_NOT_PROVEN",
        "equivalence_claim_allowed": False,
        "causal_signal_ablation_claim_allowed": False,
    }


def from_aggregate_counts(n, probe_correct, control_correct, alpha=0.05):
    """Enumerate all binary pairings consistent with the two supplied totals.

    Bounds are sharp within this unconstrained same-n binary-pairing set. They
    are not an independent/unpaired two-sample binomial test. Worst-case p is
    conservative when the unknown actual joint table is one of the candidates
    and the conditional McNemar reference assumptions hold for it.
    """
    n = _integer(n, "n")
    kp = _integer(probe_correct, "probe_correct")
    kc = _integer(control_correct, "control_correct")
    if not n or kp > n or kc > n:
        raise ValueError("counts must lie within a positive common n")
    level = _alpha(alpha)
    tables = []
    for a in range(max(0, kp + kc - n), min(kp, kc) + 1):
        b, c = kp - a, kc - a
        p = exact_mcnemar_fraction(b, c)
        tables.append({"both_correct": a, "probe_only": b, "control_only": c,
                       "both_wrong": n - a - b - c,
                       "pvalue": float(p), "pvalue_fraction": str(p)})
    values = [Fraction(row["pvalue_fraction"]) for row in tables]
    lo, hi = min(values), max(values)
    if hi <= level:
        decision = "ALL_FEASIBLE_PAIRINGS_REJECT_REFERENCE_NULL"
    elif lo > level:
        decision = "NO_FEASIBLE_PAIRING_REJECTS_REFERENCE_NULL"
    else:
        decision = "DECISION_DEPENDS_ON_UNOBSERVED_PAIRING"
    return {
        "mode": "AGGREGATE_PARTIAL_IDENTIFICATION_NOT_UNPAIRED_TEST",
        "n": n, "probe_correct": kp, "control_correct": kc,
        "accuracy_difference_probe_minus_control": (kp - kc) / n,
        "feasible_tables": tables,
        "pvalue_min": float(lo), "pvalue_max": float(hi),
        "pvalue_min_fraction": str(lo), "pvalue_max_fraction": str(hi),
        "point_pvalue_identified": lo == hi,
        "point_pvalue": float(lo) if lo == hi else None,
        "worst_case_reference_pvalue": float(hi),
        "reject_for_all_feasible_pairings": hi <= level,
        "alpha": float(level), "decision": decision,
        "bounds_scope": "all common-n binary pairings consistent with observed totals",
        "independence_status": "CONDITIONAL_REFERENCE_ASSUMPTION_NOT_PROVEN",
        "secondary_paired_n80": "UNMEASURED_WITHOUT_JOINT_DISCORDANCE_INFORMATION",
        "equivalence_claim_allowed": False,
        "causal_signal_ablation_claim_allowed": False,
    }


def from_binary_predictions(probe, control, probe_correct, control_correct, alpha=0.05, *, validated_contract=None):
    """Recover discordance totals without private labels, under a strict contract.

    Both maps must contain the same nonempty stable item IDs, one valid binary
    prediction per item, full coverage, zero invalid predictions, and unweighted
    accuracy against the same binary labels. The caller must establish that
    contract from native artifacts; this function does not authenticate it.
    Predictions alone, without the two correct-count totals, are insufficient.
    """
    required_contract = {"same_evaluation_items": True, "unweighted_binary_accuracy": True}
    if not isinstance(validated_contract, dict) or any(validated_contract.get(k) is not v for k, v in required_contract.items()):
        raise ValueError("same-item unweighted binary score contract must be separately validated")
    for key in ("probe_coverage", "control_coverage"):
        if _probability(validated_contract.get(key), key) != 1.0:
            raise ValueError("complete coverage is required")
    for key in ("probe_invalid_predictions", "control_invalid_predictions"):
        if _integer(validated_contract.get(key), key) != 0:
            raise ValueError("zero invalid predictions are required")
    if not isinstance(probe, dict) or not isinstance(control, dict) or not probe or set(probe) != set(control):
        raise ValueError("nonempty prediction maps must have identical stable item IDs")
    for values in (probe, control):
        if any(not isinstance(k, str) or not k for k in values):
            raise ValueError("stable item IDs must be nonempty strings")
        if any(type(v) is not bool for v in values.values()):
            raise ValueError("every prediction must be a valid bool; invalid/missing predictions need another path")
    n = len(probe)
    kp = _integer(probe_correct, "probe_correct")
    kc = _integer(control_correct, "control_correct")
    if kp > n or kc > n:
        raise ValueError("correct-count totals exceed the common items")
    m = sum(probe[key] != control[key] for key in probe)
    delta = kp - kc
    if (m + delta) % 2 or abs(delta) > m:
        raise ValueError("prediction disagreement and correct totals are incompatible")
    b, c = (m + delta) // 2, (m - delta) // 2
    a, d = kp - b, n - (kp - b) - m
    if min(a, b, c, d) < 0:
        raise ValueError("prediction disagreement and correct totals have no feasible joint table")
    result = from_joint_counts(a, b, c, d, alpha)
    result["pairing_source"] = "stable-item binary predictions plus two validated score totals"
    result["native_artifact_contract"] = "REQUIRES_SEPARATE_SOURCE_REVIEW"
    return result


def _binomial_probabilities(n, p):
    """Stable finite PMF, propagating from its mode rather than an underflowing tail."""
    if p == 0:
        return [1.0] + [0.0] * n
    if p == 1:
        return [0.0] * n + [1.0]
    mode = min(n, int((n + 1) * p))
    probs = [0.0] * (n + 1)
    probs[mode] = math.exp(math.lgamma(n + 1) - math.lgamma(mode + 1) - math.lgamma(n - mode + 1)
                           + mode * math.log(p) + (n - mode) * math.log1p(-p))
    for k in range(mode, 0, -1):
        probs[k - 1] = probs[k] * k / (n - k + 1) * (1 - p) / p
    for k in range(mode, n):
        probs[k + 1] = probs[k] * (n - k) / (k + 1) * p / (1 - p)
    normalizer = math.fsum(probs)
    return [v / normalizer for v in probs]


@lru_cache(maxsize=8192)
def _lower_rejection_cutoff(m, alpha_fraction):
    cutoff, lower, mass = -1, 0, 1
    for k in range(m // 2 + 1):
        lower += mass
        if Fraction(2 * lower, 2 ** m) <= alpha_fraction:
            cutoff = k
        else:
            break
        mass = mass * (m - k) // (k + 1)
    return cutoff


@lru_cache(maxsize=8192)
def _conditional_rejection_probability(m, direction_probability, alpha_fraction):
    cutoff = _lower_rejection_cutoff(m, alpha_fraction)
    if cutoff < 0:
        return 0.0
    pmf = _binomial_probabilities(m, direction_probability)
    return math.fsum(pmf[:cutoff + 1]) + math.fsum(pmf[m - cutoff:])


def paired_power(n, probe_only_probability, control_only_probability, alpha=0.05):
    """Finite exact-model power sum; probabilities evaluated numerically.

    M ~ Binomial(n,q), then B | M ~ Binomial(M, p10/q), q=p10+p01.
    The two-sided exact conditional rejection region is fixed by alpha.
    This requires an explicitly hypothesized iid joint correctness model.
    """
    n = _integer(n, "n")
    p10 = _probability(probe_only_probability, "probe_only_probability")
    p01 = _probability(control_only_probability, "control_only_probability")
    if p10 + p01 > 1 + 1e-12:
        raise ValueError("joint discordance probabilities sum to more than one")
    level = _alpha(alpha)
    q = min(1.0, p10 + p01)
    if not q or not n:
        return 0.0
    direction = p10 / q
    pmf = _binomial_probabilities(n, q)
    return math.fsum(pmf[m] * _conditional_rejection_probability(m, direction, level) for m in range(n + 1))


def first_n_for_power(probe_only_probability, control_only_probability, target=0.8, alpha=0.05, max_n=2000):
    """Bounded first crossing only; no monotonic/sustained-threshold assertion."""
    p10 = _probability(probe_only_probability, "probe_only_probability")
    p01 = _probability(control_only_probability, "control_only_probability")
    target = _probability(target, "target")
    level = _alpha(alpha)
    max_n = _integer(max_n, "max_n")
    if not 0 < target <= 1 or not 1 <= max_n <= 2000:
        raise ValueError("target must be positive and max_n must be in [1,2000]")
    if p10 + p01 > 1 + 1e-12:
        raise ValueError("joint discordance probabilities sum to more than one")
    if p10 == p01 and target > float(level):
        return {"status": "NO_NONZERO_DIRECTIONAL_EFFECT_IN_SPECIFIED_MODEL", "first_n": None,
                "max_n": max_n, "target": target, "model": {"p10": p10, "p01": p01},
                "scope": "equal discordance probabilities are the reference null; not proof of actual equivalence"}
    for n in range(1, max_n + 1):
        power = paired_power(n, p10, p01, alpha)
        if power >= target:
            return {"status": "HYPOTHETICAL_MODEL_FIRST_CROSSING", "first_n": n,
                    "power_at_first_n": power, "max_n": max_n, "target": target,
                    "model": {"p10": p10, "p01": p01},
                    "scope": "iid joint model; plug-in/sensitivity planning only, not sustained power or generalization evidence"}
    return {"status": "RIGHT_CENSORED_NO_CROSSING_WITHIN_SEARCH", "first_n": None,
            "max_n": max_n, "target": target, "model": {"p10": p10, "p01": p01},
            "scope": "no assertion beyond search limit; not equivalence"}


def analyze(n, probe_correct, control_correct, joint=None, alpha=0.05, power_max_n=2000):
    aggregate = from_aggregate_counts(n, probe_correct, control_correct, alpha)
    if joint is None:
        primary = aggregate
        secondary = {"status": "UNMEASURED", "reason": "paired discordance probabilities are not identified by two aggregate scores"}
    else:
        if not isinstance(joint, dict) or set(joint) != {"both_correct", "probe_only", "control_only", "both_wrong"}:
            raise ValueError("joint must contain exactly the four paired correctness counts")
        primary = from_joint_counts(**joint, alpha=alpha)
        if (primary["n"], primary["probe_correct"], primary["control_correct"]) != (n, probe_correct, control_correct):
            raise ValueError("joint table disagrees with validated score totals")
        secondary = first_n_for_power(joint["probe_only"] / n, joint["control_only"] / n, alpha=alpha, max_n=power_max_n)
        secondary["status_qualification"] = "EXPLORATORY_OBSERVED_JOINT_PLUG_IN_NOT_CONFIRMED_SAMPLE_REQUIREMENT"
    return {"primary": primary, "secondary": secondary, "sources": SOURCES,
            "claim_scope": "conditional paired reference only; no equivalence, black-box sufficiency, causal signal ablation, or final-test claims"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON of validated n/probe_correct/control_correct and optional joint counts")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text())
        result = analyze(**data)
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({"result": "UNUSABLE", "error": str(error)}))
        return 2
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
