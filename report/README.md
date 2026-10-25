# AIMO-Interp report v8.3

The submission artifact is `aimo-interp-report-v8.3-anonymous.pdf`. The named variant is retained for later public/camera-ready use. Both have 10 total pages: main body 1–5, Limitations and AI Use Statement 6, References 7, and appendices 8–10. The exact supplied v3 normal gate returns PASS 19/19 on the anonymous PDF. The named PDF returns 18/19 because ANONYMIZED is intentionally false. Both have zero Type3 fonts.

Current hashes and receipts are in `../results/v8.3/BUILD.json` and `../EXECUTION_REPORT_v8.3_T1.md`. `G_LOOK_v8.3.md` records the pending new-PDF review. Existing v8.1 author approval is preserved; v8.3 approval has not been recorded. T3 and T4 are unrun.

`REPORT_OUTLINE.md` is the editable source and `REPORT_DRAFT.md` the gated rendering. `report_numbers.py` verifies 164 claims: all previous 152 records and pre-existing values remain unchanged, with 12 queue-derived keys added. Supplied receipts are hash-checked under `../research/v8_3_sources/queue/`, with copies in `v8-execution/queue/`. They are public API views with the direct user/handoff bundle association; native owner logs have not been recovered. Final-test performance remains unmeasured. No paired-owner or per-problem-balance inference is drawn.

The frozen official Codabench numeric-ID guard, PREREG, and canonical UNMEASURED file remain unchanged. A distinct queue branch validates the new sources. Missing or tampered queue receipts stop the entire new render before emitting results in the abstract or Limitations.

E11 moves the old supporting analysis and Tables 4–6 to Appendix A, and old reproduction text to Appendix B. Main sections 1–3 and all six table contents are preserved; no §2.3 shortening was needed. E4 updates baseline observations with individual submission-ID labels and the fair-coin comparison. E12 removes the location identifier, anonymizes self-URLs and the self-source commit hash, and moves the abstract removal citation. Intentional changes and text/format checks are recorded in `REGEN_SPEC_v8.3.md` and `REGEN_FIDELITY_v8.3.md`.

`create_source.py` preserves the official NeurIPS 2026 style bytes, preprint option, fonts, margins, and captions. It adds section boundaries and anonymous redactions. The specified mirror URL is not proof that the mirror exists; G-MIRROR remains pending after T3. No mirror operation was performed.

Reproduce sources from the repository root:

```sh
.venv/bin/python -I tools/report_numbers.py --out results/report_numbers.json --check research/claims.json
.venv/bin/python -I tools/render_report.py report/REPORT_OUTLINE.md results/report_numbers.json report/REPORT_DRAFT.md
.venv/bin/python -I report/create_source.py
.venv/bin/python -I tools/submission_text_gate.py report/main.tex report/main-anonymous.tex report/REPORT_DRAFT.md
```

The LaTeX builder used pdflatex reruns with inline bibliography and `-no-shell-escape`. Logs and page images are under `report/build/v8.3`; machine checks are under `results/v8.3`. Full render review is separate from compilation and gate PASS.

`../results/v8.3/gate_controls/GATE_DIFF.md` compares exact v3 (`152e2a48…`) with the old gate (`32086990…`) without executing the old gate. v3 adds body/anonymity checks but does not retain every prior fallback protection. This run uses normal mode only. Historical v8.1 PDFs, approval, and v2.2 results remain preserved evidence.

`plans/payload_v8.json` is historical preparation, not a current upload instruction. Current intake requires an anonymized main body of at most five pages, one OpenReview note per first author, and later changes as revisions of that same note ID. Schema acceptance of queue UUIDs is distinct from organizer acceptance. No OpenReview authentication, upload, creation, or revision occurred in T1.
