# AIMO-Interp report v8.1

`REPORT_OUTLINE.md` is the editable manuscript with numeric placeholders.
`REPORT_DRAFT.md` is its gated rendering against `results/report_numbers.json`
and the measured-value registry in `research/claims.json`. Measured values must
come through registered keys. `ALLOWED_LITERALS.txt` covers fixed public-label
thresholds, protocol constants and bibliographic identifiers.

`create_source.py` builds both `main.tex` (Jung Min Kang, Independent) and
`main-anonymous.tex` from that same rendered content. The only scientific-source
differences between variants are author identity and PDF author metadata. Both
embed unchanged official `neurips_2026.sty` bytes from the hash-pinned author kit.
The preprint option, font/package choices, page geometry and body typesetting
defaults are preserved from v5. The two variants remain available while the
venue's anonymity policy is unresolved. The v8 PDFs are locally prepared, with a
separate unnumbered AI Use Statement on page 8 before references on page 9.
The statement describes review responsibility without claiming unverified
completed human review. Actual author review and the form's matching completed
review confirmation remain necessary before submission.

The v6 lead is a conditional, selection-adjusted analysis of the public
private-validation leaderboard and an exact power calculation. The paper
explicitly states the independent fair-coin item null, finite score-grid model,
submission-selection assumptions, dependence sensitivities and distinction
between chance testing and pairwise ranking. The public training-label/control
audit is supporting material. Private-validation results for our frozen bundles
and their final-test performance remain UNMEASURED without linked owner
receipts; matching expected constant/control scores would not establish
per-problem balance.

The editable outline marks the owner private-validation paragraph with one
`BEGIN_OWNER_PRIVATE_VALIDATION` / `END_OWNER_PRIVATE_VALIDATION` pair. The
renderer removes those markers and enforces
`OWNER_PRIVATE_VAL_UNMEASURED.md` as the canonical paragraph whenever linked
receipts do not authorize measured text. This guard applies after the deadline
as well; a deadline does not create measurements. It changes only that paragraph
and leaves the independent leaderboard analysis available.

To regenerate source from the repository root:

```sh
python3 -I tools/render_report.py report/REPORT_OUTLINE.md results/report_numbers.json report/REPORT_DRAFT.md
python3 -I report/create_source.py
python3 -I tools/submission_text_gate.py report/main.tex report/main-anonymous.tex report/REPORT_DRAFT.md
```

For a conventional PDF build, run twice for each variant from `report/`, using a
separate output directory per variant and `-no-shell-escape -halt-on-error
-interaction=nonstopmode`. There is no bibliography backend. The delivered build
uses the LaTeX-production skill's compiler/QA workflow; its execution receipt,
page counts, PDF/source hashes and Type-3 font checks accompany the publication
record. A successful compile is distinct from inspecting every rendered page.

`REGEN_SPEC_v8.1.md` predeclares the October 24 text edits against saved v8 canon;
`REGEN_FIDELITY_v8.1.md` records their final check. `REGEN_SPEC_v8.md` predeclares the text edits against the hash-verified v7
PDFs and unchanged generation specification. `REGEN_FIDELITY_v8.md` records the
source/PDF text and formatting comparison. Historical v5-v7 PDFs and QA files
remain evidence. Both v8 variants retain nine pages, the original font and margin
settings, and the unchanged AI disclosure. The two variants differ in author block
and PDF author metadata; the shared repository URL reveals identity.

The supplied `tools/openreview_payload_gate.py` is preserved byte-for-byte.
Its historical v7 four-fixture replay results remain preserved evidence. Both v8
PDFs fail the current form check only for missing genuine leaderboard submission IDs. This is a limited structural check: it does
not verify completed human review, reviewer commitments, authenticated account
access, invitation freshness, or all nested author/reviewer constraints.
`tools/openreview_submission_preflight.py` adds stricter local validation and
keeps the current artifact blocked while IDs and author attestations remain absent.
The prepared payload is `plans/payload_v8.json`; its abstract comes directly from
the gated manuscript and exact confirmation strings come from the live invitation.
The strings are prepared text rather than completed author attestations. Licence
is recorded separately as note metadata in `plans/note_metadata_v8.json`.

Raw source URLs and immutable revisions for earlier public participant reports
are kept in the research evidence manifest. The manuscript uses neutral report
titles and commit identifiers, without participant handles in visible text or
source URLs. It attributes prior label/balance observations and does not claim
those observations as a new contribution. The publication archive records what
was executed; it is not an OpenReview submission receipt.

The October 24 supplied `tools/prize_rubric_gate.py`, updated byte-for-byte, has
15/17 checks passing for both current PDFs, with 40 main-text negations. Missing owner ID/score checks block
push and submission. The protected UNMEASURED paragraph and pending-receipts
sentence remain until verified native evidence supports replacement.
