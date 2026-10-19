# v6 leaderboard analysis

Run the frozen snapshot and compare all 22 HANDOFF values:

```sh
python3 -I tools/leaderboard_identifiability.py --data-dir data --snapshot-dir data/leaderboard/2026-10-19 --out results/v6/leaderboard_identifiability.json --check research/identifiability_expected_v6.json
```

The derived JSON has flat `numbers` consumed by `tools/report_numbers.py`,
handle-free ranked owner summaries, input hashes, parsing receipts, and power
details. The eight hashed leaderboard pages retain their raw participant handles. The
attached competition metadata is also preserved as hashed comp.json; it is not
an additional leaderboard page and does not enter the owner analysis.
The item denominator is the smallest value jointly compatible with displayed
two-decimal accuracies, coverage, and invalid-item counts. Rounded public scores
alone do not establish that this is the unique true denominator.

Every page is hash-checked before any snapshot calculation. The one registered
conflict, submission 991917, uses the complete coverage-zero set: accuracy 0,
coverage 0, invalid items 21. Coverage-zero rows enter denominator checks but
enter neither the owner family nor an owner's scored-submission count. A
submission scored on both tasks counts once in each track. Repeated score
records are deduplicated.

The primary adjustment is `1 - (1 - p_single)^m`, followed by BH within track;
Bonferroni is also reported. A separate `min(1, m * p_single)` union-bound
adjustment followed by Bonferroni controls a fixed attempt/owner family without
assuming independence among submissions or among owners, conditional on valid
single-submission binomial p-values. For random observed family sizes or
score-adaptive stopping, the guarantee additionally requires p-value validity
conditional on the realized family and counts; otherwise the observed-count
result is descriptive. All calculations count invalid predictions as wrong.

The sustained power thresholds are not an arbitrary finite-sweep result. The
tool exhausts every smaller item count up to a Hoeffding sufficient bound; a
midpoint-threshold test has the requested size and power at every larger count,
and the exact-binomial test is at least as powerful.

For the October 31 rescrape, fetch every nonempty page into a separate date
directory and save an explicit hash manifest with this schema:

```json
{
  "snapshot_label": "2026-10-31",
  "phase_id": 30038,
  "sha256": {
    "lb1.json": "<64-character lowercase SHA256 of exact downloaded bytes>",
    "lb2.json": "<64-character lowercase SHA256 of exact downloaded bytes>"
  }
}
```

The map must contain all contiguous pages from `lb1.json` to `lbN.json`; the
tool rejects missing/extra pages and requires reported count to match unique
submissions. Keep fetch-time and source URL evidence with the new manifest.
The explicit-manifest mode cannot override the frozen October 19 pins.

```sh
python3 -I tools/leaderboard_identifiability.py --data-dir data --snapshot-dir data/leaderboard/2026-10-31 --snapshot-manifest data/leaderboard/2026-10-31/snapshot-manifest.json --out results/v6/leaderboard_identifiability_2026-10-31.json
```

Do not compare the later snapshot with the October 19 expected owner counts.
Apply the separately registered October 31 lead-contribution kill rule and
report both snapshots when the rule permits it.

Regression checks:

```sh
python3 -I tools/test_leaderboard_identifiability.py
```
