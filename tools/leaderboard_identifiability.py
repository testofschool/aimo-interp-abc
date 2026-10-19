#!/usr/bin/env python3
"""Hash-pinned, owner-selection-adjusted audit of the public validation board.

Only the raw input JSON contains participant handles. Derived output identifies
owners by rank within track. A visible submission counts once in each task on
which it was scored; repeated score records do not create extra trials.

    python3 -I tools/leaderboard_identifiability.py --out results/v6/leaderboard_identifiability.json --check research/identifiability_expected_v6.json

The default snapshot is the pre-registered 2026-10-19 snapshot (retrieved just
after midnight KST on October 20). All eight hashes are checked before parsing.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re
import sys

import pandas as pd
from scipy.stats import binom

SNAPSHOT_SHA256 = {
    "lb1.json": "fc7338524b81410324f3e3588aee42ff8a0bb67e5b3ad36b24a6903986d066c2",
    "lb2.json": "7fcb939214bfb1e673975cf1f3f9de100a074ba5c459da067af90ccc2ef1a4cd",
    "lb3.json": "ac33b9f4cd4e1e626f19a71b397d5a1a8a756f3fd78ef37e91c7477568a705df",
    "lb4.json": "22331c134be761029c5adefe18a08620f5a8ee84c70a6e4ca205779307abdc1e",
    "lb5.json": "89822694e89aaa4c5743ee2a84113b97386dbfa9a2ae13dc090a72df35b382a4",
    "lb6.json": "cc94df6dcee715c110332b8df677e917151501cbeb76fec21cdcd4448c34043e",
    "lb7.json": "e909516e2644adca80b744d2a10a88b788fbf6b7bce2a96be8e3e921d8765464",
    "lb8.json": "fa507d52739648f820ecb253f6ab1c5f1f6d08a2415d609628d2ad61fb1bea9f",
}
TRAIN_SHA256 = "e18eb44207e7987781ec2ff214793196038442bdc1466fdf5498f3e87ec58285"
TASKS = {36237: "Main", 36241: "Small"}
ALPHA = 0.05
TARGET = 0.8
NULL_ACCURACY = 0.5


def checked_bytes(path, expected):
    raw = Path(path).read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected:
        raise ValueError(f"STOP: {path} hash {actual} != {expected}")
    return raw


def parse_snapshot(pages):
    """Return one row per unique submission/task after score deduplication."""
    submissions = {}
    duplicate_submissions = 0
    reported_counts = set()
    for page in pages:
        if page["id"] != 30038:
            raise ValueError("STOP: unexpected leaderboard phase")
        reported_counts.add(page["count"])
        for sub in page["submissions"]:
            sid = sub["id"]
            if sid in submissions:
                if submissions[sid] != sub:
                    raise ValueError(f"STOP: inconsistent repeated submission {sid}")
                duplicate_submissions += 1
            else:
                submissions[sid] = sub
    if reported_counts != {len(submissions)}:
        raise ValueError("STOP: pagination count does not match unique submissions")
    rows, repeated_scores, dual_tasks, conflicts = [], 0, 0, []
    for sid, sub in submissions.items():
        by_task = defaultdict(lambda: defaultdict(set))
        seen = set()
        for score in sub["scores"]:
            token = (score["task_id"], score["column_key"], float(score["score"]))
            if token in seen:
                repeated_scores += 1
                continue
            seen.add(token)
            task, column, value = token
            if task not in TASKS:
                raise ValueError(f"STOP: unknown task {task}")
            by_task[task][column].add(value)
        dual_tasks += len(by_task) > 1
        for task, columns in by_task.items():
            required = {"accuracy", "coverage", "invalid_predictions"}
            if not required.issubset(columns):
                raise ValueError(f"STOP: incomplete scores on submission {sid}")
            conflicting = any(len(columns[key]) != 1 for key in required)
            if conflicting:
                # The sole registered ambiguity has two complete score sets.
                # Keep the failed (coverage-zero) set, including its invalid count.
                expected = {"accuracy": {0.0, 0.52}, "coverage": {0.0, 1.0},
                            "invalid_predictions": {0.0, 21.0}}
                if sid != 991917 or task != 36237 or any(columns[k] != v for k, v in expected.items()):
                    raise ValueError(f"STOP: unregistered conflicting score sets on {sid}")
                values = {"accuracy": 0.0, "coverage": 0.0, "invalid_predictions": 21.0}
                conflicts.append({"submission_id": sid, "track": TASKS[task],
                                  "resolution": "coverage-zero score set"})
            else:
                values = {key: next(iter(columns[key])) for key in required}
            rows.append({"submission_id": sid, "owner": sub["owner"], "track": TASKS[task],
                         **values, "queue": sub.get("queue_name", "")})
    return rows, {"unique_submissions": len(submissions),
                  "duplicate_submission_records": duplicate_submissions,
                  "repeated_score_records_removed": repeated_scores,
                  "submissions_scored_on_both_tasks": dual_tasks,
                  "submission_task_rows": len(rows), "conflicts": conflicts}


def integer_from_display(value, n):
    fits = [k for k in range(n + 1) if abs(round(k / n, 2) - value) < 1e-9]
    if len(fits) != 1:
        raise ValueError(f"STOP: displayed fraction {value} is ambiguous at N={n}")
    return fits[0]


def smallest_denominator(rows, maximum=299):
    """Fit all rounded accuracies, coverage and integral invalid-item counts."""
    for n in range(1, maximum + 1):
        fits = True
        for row in rows:
            invalid = row["invalid_predictions"]
            if not invalid.is_integer() or not 0 <= invalid <= n:
                fits = False
                break
            if abs(round((n - int(invalid)) / n, 2) - row["coverage"]) > 1e-9:
                fits = False
                break
            candidates = [k for k in range(n - int(invalid) + 1)
                          if abs(round(k / n, 2) - row["accuracy"]) < 1e-9]
            if len(candidates) != 1:
                fits = False
                break
        if fits:
            return n
    raise ValueError("STOP: no denominator fits rounded accuracy, coverage and invalid counts")


def critical_correct(n):
    """Smallest k such that P_0(X >= k) <= alpha; n+1 means never reject."""
    k = int(binom.isf(ALPHA, n, NULL_ACCURACY)) + 1
    while k > 0 and binom.sf(k - 2, n, NULL_ACCURACY) <= ALPHA:
        k -= 1
    while binom.sf(k - 1, n, NULL_ACCURACY) > ALPHA:
        k += 1
    return k


def exact_power(n, p):
    return float(binom.sf(critical_correct(n) - 1, n, p))


def power_numbers():
    nums = {"power_alpha": ALPHA, "power_fdr_q": ALPHA, "power_target": TARGET,
            "power_null_accuracy": NULL_ACCURACY}
    detail = {}
    for suffix, p in (("acc060", 0.60), ("acc065", 0.65)):
        # Hoeffding guarantees size <= alpha and power >= target for the midpoint
        # threshold at every n >= bound. The exact binomial test is at least as
        # powerful. Scan all smaller n, so sustained is certified beyond a sweep.
        bound = math.ceil(2 * max(math.log(1 / ALPHA), math.log(1 / (1 - TARGET)))
                          / (p - NULL_ACCURACY) ** 2)
        values = [(n, exact_power(n, p)) for n in range(1, bound + 1)]
        first = next(n for n, power in values if power >= TARGET)
        sustained = max(n for n, power in values if power < TARGET) + 1
        nums[f"power_alternative_{suffix}"] = p
        nums[f"power_n80_first_{suffix}"] = first
        nums[f"power_n80_sustained_{suffix}"] = sustained
        nums[f"power_sustained_certification_{suffix}"] = bound
        for n in (14, 21):
            nums[f"power_at_{n}_{suffix}"] = round(exact_power(n, p), 2)
        detail[suffix] = {"true_accuracy": p, "first_n": first, "sustained_n": sustained,
                          "power_at_first": exact_power(first, p),
                          "power_at_sustained": exact_power(sustained, p),
                          "all_larger_n_certified_by_hoeffding_from": bound}
    return nums, detail


def summarize_track(rows):
    n = smallest_denominator(rows)
    scored = [row for row in rows if row["coverage"] > 0]
    owners = defaultdict(list)
    for row in scored:
        owners[row["owner"]].append(row)
    ranking = []
    for own_rows in owners.values():
        best = max(integer_from_display(row["accuracy"], n) for row in own_rows)
        p = float(binom.sf(best - 1, n, NULL_ACCURACY))
        m = len(own_rows)
        padj = -math.expm1(m * math.log1p(-p)) if p < 1 else 1.0
        ranking.append({"visible_scored_submissions": m, "best_correct": best,
                        "p_single": p, "p_adjusted": padj,
                        "p_union_bound": min(1.0, m * p),
                        "perfect_organizer_rerun_submissions": sum(
                            integer_from_display(r["accuracy"], n) == n and
                            "aimo_organizer_rerun" in r["queue"] for r in own_rows)})
    # No handle enters the exported ranking or tie breaker.
    ranking.sort(key=lambda row: (row["p_adjusted"], -row["best_correct"], row["visible_scored_submissions"]))
    M = len(ranking)
    qs = [min(1.0, row["p_adjusted"] * M / i) for i, row in enumerate(ranking, 1)]
    for i in range(M - 2, -1, -1):
        qs[i] = min(qs[i], qs[i + 1])
    for i, (row, q) in enumerate(zip(ranking, qs), 1):
        row.update({"owner_rank": i, "bh_q": q, "bh_significant": q <= ALPHA,
                    "bonferroni_significant": row["p_adjusted"] <= ALPHA / M,
                    "union_bonferroni_significant": row["p_union_bound"] <= ALPHA / M})
    bh = sum(row["bh_significant"] for row in ranking)
    if not ranking:
        raise ValueError("STOP: track has no coverage-positive owners")
    next_row = ranking[bh] if bh < M else None
    nums = {"items": n, "owners_scored": M, "scored_submissions": len(scored),
            "submission_task_rows": len(rows), "coverage_zero_rows": len(rows) - len(scored),
            "bh_survivors": bh,
            "bonferroni_survivors": sum(row["bonferroni_significant"] for row in ranking),
            "union_bonferroni_survivors": sum(row["union_bonferroni_significant"] for row in ranking),
            "owners_single_draw_significant": sum(row["p_single"] <= ALPHA for row in ranking),
            "perfect_owners": sum(row["best_correct"] == n for row in ranking),
            "perfect_scored_submissions": sum(integer_from_display(r["accuracy"], n) == n for r in scored),
            "perfect_organizer_rerun_submissions": sum(row["perfect_organizer_rerun_submissions"] for row in ranking),
            "next_padj": round(next_row["p_adjusted"], 4) if next_row else None,
            "next_best_correct": next_row["best_correct"] if next_row else None,
            "next_submissions": next_row["visible_scored_submissions"] if next_row else None,
            "next_rank": bh + 1 if next_row else None,
            "critical_correct": critical_correct(n),
            "actual_alpha": round(float(binom.sf(critical_correct(n) - 1, n, NULL_ACCURACY)), 4),
            "accuracy_half_scored_submissions": sum(r["accuracy"] == .5 for r in scored)}
    return nums, {"numbers": nums, "owners_by_adjusted_p": ranking,
                  "scored_submissions_per_owner_histogram": dict(sorted(Counter(len(x) for x in owners.values()).items())),
                  "denominator_rule": "smallest jointly fitting rounded accuracy, coverage and invalid-count denominator; invalid items count wrong"}


def snapshot_hashes(snapshot_dir, snapshot_manifest=None):
    """Future snapshots require explicit pins; the original pins cannot change."""
    if snapshot_manifest is None:
        return "2026-10-19", SNAPSHOT_SHA256
    manifest = json.loads(Path(snapshot_manifest).read_text())
    label = manifest["snapshot_label"]
    if (label == "2026-10-19" or
            Path(snapshot_dir).resolve() == Path("data/leaderboard/2026-10-19").resolve()):
        raise ValueError("STOP: explicit manifest cannot override the frozen 2026-10-19 snapshot")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", label) or manifest["phase_id"] != 30038:
        raise ValueError("STOP: future snapshot needs ISO date label and phase_id 30038")
    hashes = manifest["sha256"]
    names = [f"lb{i}.json" for i in range(1, len(hashes) + 1)]
    if not hashes or set(hashes) != set(names):
        raise ValueError("STOP: future snapshot pins must list contiguous pages lb1.json..lbN.json")
    if any(not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value) for value in hashes.values()):
        raise ValueError("STOP: invalid future snapshot SHA256")
    if set(path.name for path in Path(snapshot_dir).glob("lb*.json")) != set(names):
        raise ValueError("STOP: future snapshot page files differ from the explicit manifest")
    return label, {name: hashes[name] for name in names}


def run(snapshot_dir="data/leaderboard/2026-10-19", data_dir="data", snapshot_manifest=None):
    # Verify every input before parsing or calculating any derived value.
    label, hashes = snapshot_hashes(snapshot_dir, snapshot_manifest)
    raw = {name: checked_bytes(Path(snapshot_dir) / name, expected)
           for name, expected in hashes.items()}
    train_path = Path(data_dir) / "train-main-v2.parquet"
    checked_bytes(train_path, TRAIN_SHA256)
    rows, parsing = parse_snapshot([json.loads(page) for page in raw.values()])
    nums, power = power_numbers()
    nums.update({"lb_unique_submissions": parsing["unique_submissions"],
                 "lb_submission_task_rows": parsing["submission_task_rows"],
                 "lb_dual_task_submissions": parsing["submissions_scored_on_both_tasks"],
                 "lb_repeated_score_records_removed": parsing["repeated_score_records_removed"],
                 "lb_conflicting_submissions": len(parsing["conflicts"])})
    tracks = {}
    for track in ("Small", "Main"):
        track_nums, tracks[track] = summarize_track([row for row in rows if row["track"] == track])
        nums.update({f"lb_{track.lower()}_{key}": value for key, value in track_nums.items()})
    train = pd.read_parquet(train_path).dropna(subset=["is_robust"])
    small = train[~train.model_id.str.startswith("openai")]
    problem = small.groupby("problem").agg(models=("model_id", "nunique"), labels=("is_robust", "nunique"))
    multi = problem[problem.models > 1]
    nums.update({"train_small_rows": int(len(small)), "train_small_problems": int(len(problem)),
                 "train_small_multi_model_problems": int(len(multi)),
                 "train_small_mixed": int((multi.labels > 1).sum())})
    return {"schema_version": 1, "snapshot_label": label, "numbers": nums, "tracks": tracks, "parsing": parsing,
            "power": power, "input_sha256": {**hashes, "train-main-v2.parquet": TRAIN_SHA256},
            "assumptions": ["fair independent item null with success probability 0.5",
                            "independent submissions within each owner for Sidak selection adjustment",
                            "only visible coverage-positive submissions counted per owner",
                            "BH and Bonferroni applied separately within each track",
                            "union-bound plus Bonferroni sensitivity needs no submission or owner independence; item-binomial null remains"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot-dir", default="data/leaderboard/2026-10-19")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--snapshot-manifest", help="explicit future snapshot date/phase/SHA256 manifest; cannot override frozen snapshot")
    parser.add_argument("--out")
    parser.add_argument("--check")
    args = parser.parse_args()
    try:
        result = run(args.snapshot_dir, args.data_dir, args.snapshot_manifest)
    except (ValueError, OSError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if args.out:
        dest = Path(args.out)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(result, indent=2) + "\n")
    if args.check:
        expected = json.loads(Path(args.check).read_text())["expected"]
        mismatches = [{"key": key, "expected": value, "observed": result["numbers"].get(key)}
                      for key, value in expected.items() if result["numbers"].get(key) != value]
        print(json.dumps({"result": "FAIL" if mismatches else "PASS", "checked": len(expected),
                          "mismatches": mismatches}, indent=2))
        return bool(mismatches)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
