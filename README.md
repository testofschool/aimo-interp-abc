# AIMO-Interp: validation leaderboard identifiability

The v6 report asks what can be resolved from a small public validation leaderboard.
On the pinned October 19 snapshot (retrieved October 20, 2026 KST), owner-selection
adjustment followed by Benjamini–Hochberg leaves 2 of 61 Small owners and 1 of 41
Main owners significant under an independent fair-coin item null. All survivors
have perfect scores. This is a conditional above-chance audit, not a pairwise
ranking test. The smallest denominators jointly compatible with the displayed
scores, coverage and invalid counts are 14 and 21; rounded scores alone do not
prove the true number of evaluation items.

For a one-sided exact binomial test at alpha 0.05, 80% power at true accuracy 0.60
first occurs at 158 items and is sustained from 169; at accuracy 0.65 the counts
are 69 and 76. These are single fixed predictor calculations, without leaderboard
selection or multiple-owner correction. The report keeps those limits explicit.

Public anonymous fresh-clone V1–V6 passed at scientific commit `524cc98816b2cd31bafd7c4e4e25f66a093e2cf5`;
see `PUBLICATION.md` and `results/v6/publication/`.

Read `report/REPORT_DRAFT.md`, the named and anonymous v6 PDFs under `report/`,
`EXECUTION_REPORT_v6.md`, and `PUBLICATION.md`. The v5 report and its execution
receipts remain historical evidence. Two frozen owner bundle scores and final-test
performance remain **UNMEASURED**. No GPU/model generation run was launched.

## Reproduce

Use Python 3.12 or newer (this release is verified on Python 3.13):

```sh
git clone https://github.com/testofschool/aimo-interp-abc.git
cd aimo-interp-abc
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements-local.txt
.venv/bin/python -I tools/fetch_data.py --output-dir data
.venv/bin/python -I tools/reproduce_report.py
.venv/bin/python -I tests/test_v6_gates.py
.venv/bin/python -I tools/test_leaderboard_identifiability.py
```

V1 checks the original and expanded numeric registry; V2 renders the original
and final outlines; V3 preserves the v5 reference values. V4 is expected to return
`CLOSED` with exit 1. V5 recomputes 22 frozen v6 values from hash-checked inputs.
V6 checks report front matter in both source variants and Markdown. A separate
owner-evidence check retains UNMEASURED when receipts are missing, allowing
unrelated analysis and report work to complete. Synthetic fixtures are not service
results. See `research/GATES_v6.md` for scope and the supplied gate's limitations.

Dataset IDs, immutable revisions, hashes and license boundaries are in
`data/manifest.json`. Parquet files are fetched locally and not redistributed.
Pinned public leaderboard JSON is included; participant handles remain in the
raw snapshot, while derived result tables use within-track owner ranks.
Every reported numeric key is regenerated and checked against `research/claims.json`.
A hash mismatch stops before computation.

## Report builds and remaining owner work

```sh
.venv/bin/python -I tools/render_report.py report/REPORT_OUTLINE.md results/report_numbers.json report/REPORT_DRAFT.md
.venv/bin/python -I report/create_source.py
```

`report/create_source.py` produces named and anonymous NeurIPS sources from the
same gated body. See `report/README.md` for build and font/render verification.
Both variants are retained while the actual OpenReview invitation's anonymity
policy is unavailable. This repository's publication is not an OpenReview receipt.

An October 20 public portal recheck found an unresolved report-deadline conflict:
the Submission invitation currently configures November 1 at 17:00 KST, while the
official website says November 15. See `research/v6_sources/PORTAL_CHECK_2026-10-20.md`
and `OWNER_CHECKLIST_v6.md`. PDF anonymity remains unverified; both variants stay.

The owner uploads the unchanged Small bundles listed in `OWNER_CHECKLIST_v6.md`,
records native receipts and screenshots, reads current Discord instructions,
nominates final-test submissions, and performs the final OpenReview submission.
Two aggregate scores can check receipt expectations; they cannot establish
per-problem label balance. Missing evidence never becomes a zero or a passed gate.

The October 31 rescrape is scheduled for 20:00 Asia/Seoul in the current Codex chat.
It has not run. The registered kill rule and immutable future-snapshot invocation
are in `HANDOFF_v6.md` and `research/identifiability_usage_v6.md`. Method reopening
remains CLOSED. AI assistance and all statistical assumptions are disclosed in
the report. Current release receipts supersede historical v5 state statements.

The full completion audit is in `COMPLETION_AUDIT_v6.md`. It records corrected snapshot membership, verbatim label rules and the protected owner-result rendering block; required owner evidence and the actual October 31 rescrape are still pending.
