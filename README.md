# AIMO-Interp: problem-only controls and public-label audit

The v5 technical draft is public: five NeurIPS-format pages, 87 checked
numeric values and 89 rendered placeholders. It is not submitted. Public-data
control balanced accuracy is 0.6855 and plain accuracy is 0.7674; private-validation
and final-test performance are UNMEASURED. The method track remains folded and
the reopen gate is CLOSED. No new GPU jobs or spend are authorized by this packet.

Read `report/REPORT_DRAFT.md`, `report/aimo-interp-report-v5.pdf`,
`report/CLAIMS_TABLE.md`, and `EXECUTION_REPORT_v5.md` for results and limitations.
The inherited pre-v5 README is preserved at `research/history/README_pre_v5.md`.

## Reproduce the CPU report

Use Python 3.12 and the pinned local dependencies:

```sh
git clone https://github.com/testofschool/aimo-interp-abc.git
cd aimo-interp-abc
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements-local.txt
.venv/bin/python -I tools/fetch_data.py --output-dir data
.venv/bin/python -I tools/reproduce_report.py
```

The fetcher fixes all four HF revisions and checks exact file sizes and hashes.
Any existing mismatch stops without replacement. Parquet files are excluded from
the prepared public export because redistribution permission is unresolved.
`data/manifest.json` records IDs, paths, revisions, hashes and source evidence.

The reproduction runner checks the original V1 (13 claims), original V2 (17
placeholders), final V1 (87 claims), final V2 (89 placeholders), V3's registered
values and V4. V4 must return CLOSED / exit 1; that is the expected operational
stop, not a failed report check. It also compares regenerated JSON and rendered
Markdown with the tracked bytes. It does not launch a job or contact Codabench.

The expanded numeric script preserves the original claim values and adds plain
accuracy, checkpoint/cohort sensitivities and a fully specified problem bootstrap.
The old unscripted power-note interval is historical, not the current estimate.

## Report source and PDF

```sh
.venv/bin/python -I tools/render_report.py report/REPORT_OUTLINE.md results/report_numbers.json report/REPORT_DRAFT.md
.venv/bin/python -I report/create_source.py
```

`report/main.tex` embeds the unchanged official NeurIPS style and uses an inline
bibliography. See `report/README.md` for the PDF build. Final source compiled with
both the desktop compiler and pdfTeX; all five page renders were inspected. The
PDF hash and font/key/reference checks are in `report/render_qa_v5.json`.

## Owner submission artifacts and remaining work

| Bundle | SHA256 | Status |
|---|---|---|
| `bundles/solution-text-length-control-small.zip` | `30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd` | Original frozen control, unchanged |
| `bundles/solution-always-true-small.zip` | `4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a` | Built with the pinned official builder |

The owner confirmed account `testofschool` and no submission yet. `kangmin` rows
are not used as evidence. Host-only checks do not establish private scores or
GPU-image parity. See `OWNER_CHECKLIST_v5.md`; uploads and OpenReview submission
remain owner actions. Public publication and anonymous fresh-clone reproduction
passed on 2026-10-20 KST at commit `6fef8753b2e21b0c53098e77fdbc6e72ad4d4251`.
See `PUBLICATION.md` and `results/v5/publication/` for public HEAD, V1-V4 outputs,
data downloads, bundle rebuild and identical TeX source. Subsequent publication
receipt/documentation commits preserve the tested scientific bytes. The report
PDF retains its prepublication snapshot statements; this README records the
current release state.

## Evidence boundaries

Problem R-squared is a descriptive in-sample decomposition. Agreement with a
Bernoulli reference is not a significance test. Public sample configurations
are not scored competition inputs; some underlying checkpoints overlap.
Organizer baseline metrics use different protocols, so there is no matched
superiority claim. Related work is cited explicitly. Unexecuted methods and
unsupported inherited external screening numbers are not experimental results.

AI assistance is disclosed in the report. Current rules and provenance are
summarized in `research/v5_sources/AUTHORITY_LEDGER.md`; the private raw-source
cache is not included in the export. These are documentary verifications, not
independent reruns of competitors' experiments. Historical records retain their
original timestamps and statements and are superseded by the v5 execution report.
