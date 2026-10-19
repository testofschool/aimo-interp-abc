# v6 requirement-by-requirement completion audit

Full goal remains **INCOMPLETE**. Local executable checks pass after the corrections below; T6 refresh is pending and T4/T5 remain required work. A future schedule is not execution evidence.

| Requirement | State | Evidence |
|---|---|---|
| I0 — Initial public HEAD and v5 PDF/bundle/train hashes matched before execution | PASS | results/v6/input_checks.json; research/v6_sources/input-integrity.json |
| I1 — All38 package manifest hashes checked | PASS | research/v6_sources/input-integrity.json |
| T1.1 — Every attached snapshot JSON copied and individually hashed in data manifest | PASS | results/v6/snapshot_completeness.json:9/9 including comp.json; comp metadata is not ninth numeric page |
| T1.2 — Frozen snapshot hash checks precede computation; smallest compatible denominators; invalid/dedup/dual/conflict/coverage rules | PASS | tools/leaderboard_identifiability.py; tools/test_leaderboard_identifiability.py; results/v6/leaderboard_identifiability.json |
| T1.3 — All20 required numerical expectations plus2 Bonferroni values registered and checked | PASS | results/v6/identifiability_validation.json:22/22 MATCH; research/claims.json; results/report_numbers.json |
| T1.4 — Optional transfer only after license check, from fetched pinned bytes, no raw redistribution | PASS_OPTIONAL | research/v6_sources/source_audit.json; OPTIONAL_TRANSFER.md; results/v6/optional_transfer_validation.json:10/10 MATCH; raw data omitted |
| T1.5 — Current scientific report omits participant handles | PASS | Both TeX/Markdown and extracted current PDF texts checked; hashed raw snapshot retained |
| T2.1 — Specified scientific narrative, power, label audit, calibration/dependence/hidden-attempt/final-test limitations and AI disclosure | PASS | report/REPORT_DRAFT.md; report/REGEN_FIDELITY_v6.md; results/v6/statistical_review.json |
| T2.2 — Official NeurIPS template,6-8bodypages plusreferences | PASS | report/render_qa_v6.json; unchanged official style and base preamble;8body+1references |
| T2.3 — Prior v5 lead-contribution sentence removed | PASS | report/REPORT_DRAFT.md and extracted final PDF text |
| T2.4 — Measured decimals/percentages use checked numeric keys; sourced literals remain declared | PASS | tools/render_report.py; report/ALLOWED_LITERALS.txt; V2 public stdout |
| T2.5 — Submission front-matter gate exits0 on final sources | PASS | V6 public stdout; both TeX sources and Markdown CLEAN |
| T2.6 — Named Jung Min Kang Independent and anonymous variants from one scientific body | PASS | report/source_provenance.json; report/regen_source_checks_v6.json |
| T2.7 — TAE citation is optional | NOT_REQUIRED | Not used; no claim added |
| L5.R1 — Inherited v5 requires public label rule verbatim | PASS | Pinned dataset card26-29; exact two rules restored in report/REPORT_DRAFT.md; sourced0.10/0.25 literals |
| L5.V — Original13-claim/17-placeholder and frozen12 v5 checks retained | PASS | tools/reproduce_report.py; latest public CPU receipt |
| T3.1 — Two supplied gates, PREREG and five fixture inputs installed byte-identically | PASS | results/v6/gate_fixture_receipts.json; original package hashes |
| T3.2 — V5 identifiability and V6 text/source regeneration integrated | PASS | tools/reproduce_report.py; latest public CPU receipt |
| T3.3 — Synthetic fixture exits0,0,1,1,1 and mismatch REFUTED_OR_PARTIAL | PASS_SYNTHETIC_ONLY | results/v6/gate_fixture_receipts.json; no fixture promoted to live receipt |
| T3.4 — 7/14 expectations described as receipt expectations, not novel predictions or balance proof | PASS | report section4; research/GATES_v6.md; fixed supplied PREREG retained as evidence |
| T3.5 — Missing/invalid receipts replace only owner private-result block with protected UNMEASURED fallback; deadline never invents results | PASS | tools/render_report.py scoped rendering; report/OWNER_PRIVATE_VAL_UNMEASURED.md; new scoped rendering regression receipt |
| T4.1 — Felix uploads both unchanged Small bundles and supplies real scores/screenshots | OWNER_REQUIRED | No results/v6/codabench_receipts.json exists; user-designated owner action; Codex clicks prohibited |
| T4.2 — Felix records exact Discord announcements and current nomination/report/anonymity instructions | OWNER_REQUIRED | No research/discord_2026-10.md exists; explicit owner track |
| T5 — October31 complete rescrape and novelty/kill-rule decision | DATE_REQUIRED | TodayOctober20KST; scheduled20:00KSTOct31 via aimo-v6-leaderboard-rescrape; future snapshot absent; not complete |
| T6.1 — Commit with specified author and public push/readback | PUBLIC_REFRESH_PENDING | PUBLICATION.md and latest final public HEAD receipt; author felix <gangjeongmin23@gmail.com> |
| T6.2 — Fresh anonymous clone,newvenv,fresh pinned data,V1-V6 pass | PUBLIC_REFRESH_PENDING | Latest results/v6/publication receipt and per-check stdout/stderr |
| T6.3 — Both public PDFs render,page counts/hashes/Type3 recorded | PUBLIC_REFRESH_PENDING | PUBLICATION.md; report/render_qa_v6.json; public readback PDF rendering logs |
| T6.4 — No OpenReview submission by Codex | PASS_BOUNDARY | Owner checklist; no submission receipt; explicit owner-only final click |
| D1 — Every preregistered input/value expected-observed-MATCH table | PASS | EXECUTION_REPORT_v6.md; initial38+input checks+22identifiability+10optional |
| D2 — Build-input changes file-by-file including manifest,reproduce and requirements byte deltas | PASS | BUILD_INPUT_CHANGES_v6.md; results/v6/build_input_changes.json; requirements unchanged |
| D3 — Final clean sources,PDF page counts/hashes/Type3 zero | PASS | Latest QA and public stdout |
| D4 — Public HEAD and fresh-clone V1-V6 stdout retained | PUBLIC_REFRESH_PENDING | PUBLICATION.md; latest public/final readback receipts |
| D5 — Unrun work and reasons reported | PASS | EXECUTION_REPORT_v6.md; owner/future actions remain explicitly incomplete |
| P — No paidGPU/newlanguage-model inference/method reopen/service clicks/messages/unlicensed raw label redistribution | PASS_BOUNDARY | Recorded CPU commands only; V4 CLOSEDexpectedexit1; unchanged bundles; source/license/provenance ledgers |

Corrections found during this completion audit: copied and hashed omitted comp.json; restored exact inherited label rules; connected receipt evidence to scoped rendering with a protected UNMEASURED fallback; aligned usage documentation with the fixed-family/adaptive-stopping limitation already stated in the paper.

No additional model/GPU work was introduced. The owner designated account uploads, Discord record and final submission remain outside Codex action authority. October31 has not arrived. These facts prevent a full completion claim.
