# Independent v8.3 fidelity and anonymous PDF review

Verdict: **PASS for local T1 anonymous-artifact QA**. There are no unreported semantic or formatting changes left in the checked artifact. This is not human G-LOOK, a verified mirror, or an external submission receipt.

Content canon: approvedv8.1 at144ce58, paired with its matching outline/draft/generator/style and stored under v8-execution/v8.3-preflight/canon. The independent canon audit verifies those bytes against144ce58. Format canon is present: official embedded NeurIPS2026style, preprint option, T1encoding, original font/margin/table defaults. It was preserved rather than recovered or improvised.

Reviewed anonymous PDF SHA-256: `2edf06ab6764af045e470acdc77f115700d9cf85303a11d174c80e273c182e51`. Generated source SHA-256: `31f8ceb94cb94edec4f31712a0b8db49bf828b9afd3e82e8537dc680da604aeb`. Mechanical checks: **27/27 PASS**. Visual review: **all10pages PASS**, inspected individually from the actual110dpi PNG render.

| Axis | Observed difference | Classification | Verification |
| --- | --- | --- | --- |
| Abstract | E4 JSON-derived queue observations, singular ID clauses, CPU-reproduction clause, and moved removal citation | Reported intentional E4/citation/lexical deltas | Entire expected paragraph matches; no extra change |
| Main §§1,3 | None | Preserved | Word-for-word equality |
| Main §2 | Snapshot country phrase becomesKST | Reported intentional E12 | Only this replacement differs; §2.3 is not shortened |
| Old §4 → AppendixA | Section move plus removal of planned/pending statements and E4 result block | Reported intentional E11/E4 | Every remaining paragraph and table byte-identical |
| Old §5 → Limitations | Move to excluded section, E4 result/status replacement | Reported intentional E11/E4 | Calibration/dependence/size paragraphs unchanged; final-test absence retained |
| AI Use Statement | Move earlier with Limitations | Reported intentional E11 | Statement word-for-word unchanged; human new-PDF review still pending |
| References | Move before appendices; S13 adds explicit handoff provenance for24Octqueue notice | Reported intentional E11/reference delta | All other bibliography content unchanged |
| Old §6 → AppendixB | Section move | Reported intentional E11 | Raw named source content word-for-word unchanged |
| Anonymous variant | Author block/metadata, two self-repository URLs, searchable self-source commit mask | Reported intentional E12 and predeclared privacy normalization | These are the only variant differences after excluding common embedded style |
| All six tables | None to contents or numerical keys | Preserved | Six Markdown table blocks byte-identical; unchanged captions/style |
| Scientific registry | Twelve source-backed queue keys appended | Reported intentional E4 | All original152fullclaimrecords identical;164total |
| Format | Old9totalpages →10; mainbody7→5; excluded sections reflow and appendices | Reported intentional E11 | Mainbody ends page5; Limitations/AI page6; References7; AppendixA8–9; B9–10 |
| Font/layout | No font, margin, style-option or table-default changes | Preserved | Both generated-source preambles match canon; Type3=0 |

The complete pdftotext line diff is `pdftotext_v8.1_to_v8.3_anonymous.diff`. Line-level reflow from changed pages is expected; the section-aware checks exhaustively compare the underlying text and moved blocks so reflow does not hide an unreported wording change.

Anonymity: case-insensitive identity-token counts are **text0, metadata0, linkURI0**; the searchable self-source identifier is also absent. PDF Author is exactly `Anonymous Author(s)`. All7link targets were read through the PDF annotation objects. The visible specified anonymous mirror URL occurs twice. This verifies anonymized artifact text/metadata/targets; it does not claim the mirror currently exists or has a scrubbed README. G-MIRROR remains pending.

Visual observations: title, all equations, six tables, references, appendix headings and footer boundaries are fully visible. No overlap, clipped lines/cells, missing glyph/tofu, split table, orphan heading or unexpected blank page was found. AppendixB starts near the bottom of page9 with a substantive initial paragraph and continues on10; it is not an orphan heading. Page5's remaining white space follows the declared boundary before excluded sections.

The artifact truthfully retains no final-test outcomes, final-test UNMEASURED status in AppendixA, paired-data requirements, declared binomial/selection assumptions and the distinction between queue results and the leaderboard. Public receipt observations/user-supplied mapping are not represented as recovered native-owner logs.

The installed v3 gate hash is unchanged at152e2a488eb0c3cdeadbe4195bb09ac90acab464df4326a612098dc63f5c7630. No old32086990gate was executed by this audit. No report/generator/numeric source was edited. Only QA outputs were written.

**Unreported differences remaining:0. G-LOOK:pending human confirmation of the actual anonymous PDF. T3/T4:not performed by this audit.**
