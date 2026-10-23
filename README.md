# AIMO-Interp: validation leaderboard identifiability

G-AUTHOR 직접 확인을 기록하고 AI Use Statement에 검토 완료·책임 문구를 반영했다. 현재 상태는 `report/G_AUTHOR_v8.1.md`, `AUTHOR_APPROVAL_INTEGRATION_2026-10-24.md`, `results/v8.1/BUILD.json`을 따른다. T2는 외부 원인으로 blocked이며 상금 게이트는 실제 접수번호·점수가 없어 15/17이다.

October 24 gate update: supplied v2.2 and the handoff are preserved with their exact hashes under `research/gate_v2_2/source/`. The active gate is the separately identified `2.2+local.1` hardening. Its nine test groups (31 cases) pass on macOS; the original supplied gate passes 3/9 groups (17/31 cases). These are protocol checks, not submission receipts. See `GATE_V2_2_VALIDATION.md` and `research/gate_v2_2/OPERATIONS.md`; the actual report remains 15/17 and fallback has not run operationally.

The locally prepared v8.1 report asks what can be resolved from a small public validation leaderboard.
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

Read `report/REPORT_DRAFT.md`, both v8 PDF variants under `report/`,
`EXECUTION_REPORT_v8.1.md`, and `PUBLICATION.md`. v8 corrects the BH wording,
removes queue discussion, leads with conditional non-rejection counts and an
independent-item planning rule, and reduces redundant hedging. The existing 150
claims, frozen data and bundles are unchanged; two complementary owner counts
are derived from existing values. The current normal prize gate is 15/17: genuine owner
submission IDs and scores are still absent. Publication and submission are pending.
The published v6 report and v5-v7 artifacts remain historical evidence.
Two frozen owner bundle scores and final-test
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
Both variants are retained while venue anonymity instructions remain unverified.
The current public invitation is readable, but does not settle an anonymity policy.
This repository's publication is not an OpenReview receipt.

The October 24 live Submission invitation configures November 6 at 21:59 KST
(expiration 22:29), requires leaderboard submission IDs and offers only CC BY-SA
4.0. This supersedes the October 20 portal configuration preserved in historical
receipts. Fresh field/enum constraints are under `research/v8_1_sources/`. The new required
submission track is Small models track. The revised reciprocal-reviewer obligation
is three reviews. Website/announcements give November 6 at 20:59 KST, one hour
earlier than the portal; the existing decision uses the portal deadline. The page
cap remains unconfirmed. Organizer context, proposal citation and the independent-item
design target are recorded in the v8.1 report; the frozen snapshot predates the
October 21 removals, without identifying affected owners.
The author directly confirmed review of the named variant and AI-assisted work on October 24; the disclosure now records completed review and responsibility. The alternative changes the author
block and PDF author metadata; the repository URL still reveals the author, so it
must not be described as fully double-blind anonymized.

The owner uploads the unchanged Small bundles listed in `OWNER_CHECKLIST_v6.md`,
records native receipts and screenshots, reviews current Discord instructions,
nominates final-test submissions, and performs the final OpenReview submission.
Two aggregate scores can check receipt expectations; they cannot establish
per-problem label balance. Missing evidence never becomes a zero or a passed gate.

The earlier v6 workflow recorded an October 31 rescrape scheduled for 20:00
Asia/Seoul. This v8 run did not verify or modify that schedule; the future rescrape
has not been executed as part of this run. The registered kill rule and immutable future-snapshot invocation
are in `HANDOFF_v6.md` and `research/identifiability_usage_v6.md`. Method reopening
remains CLOSED. AI assistance and all statistical assumptions are disclosed in
the report. Current release receipts supersede historical v5 state statements.

The historical v6 completion audit is in `COMPLETION_AUDIT_v6.md`. It records corrected snapshot membership, verbatim label rules and the protected owner-result rendering block. `EXECUTION_REPORT_v8.md` is historical. `AUTHOR_APPROVAL_INTEGRATION_2026-10-24.md` records the latest author confirmation, checks and remaining account/receipt work. Required owner evidence and the actual October 31 rescrape are still pending.
