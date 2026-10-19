# Regen fidelity report — v6

Content canon: the public v5 PDF at commit `9274840b6faacaa7ad0e321172071eedb822d9de`, SHA-256 `1ec9bfb0ac7e48c78ef13ae8ee78d9acdce953bd12bac1038a3bee08719194cf`. It is the artifact explicitly pinned by HANDOFF v6, rather than a historical generator chosen by recency.

Format canon: that commit's `report/create_source.py` and the unchanged official NeurIPS author kit/style, paired with the PDF. The intentional differences were declared in `REGEN_SPEC_v6.md` before source generation and PDF compilation. The final manuscript has eight body pages plus one references page in both variants, within the declared six–eight body-page target.

## Final artifacts and checks

| Artifact | Pages | SHA-256 | Type-3 fonts |
|---|---:|---|---:|
| v5 content canon | 5 | `1ec9bfb0ac7e48c78ef13ae8ee78d9acdce953bd12bac1038a3bee08719194cf` | 0 |
| v6 named | 9 | `0cd3fdf4dd40b39a80b5244fc7d8131f2956c278d1944c6951eebe2e0290600f` | 0 |
| v6 anonymous | 9 | `64007f693861ccf0151e42e0805fccc65a638036ec26b76a7a440a7f5c13c112` | 0 |

Named source SHA-256: `211bf3f17a03d093e3d472f27baac8e2a712fa408dcb1e5836a01f438c2507e9`.

Anonymous source SHA-256: `513c75c8ee6a1605ee111f35ec5a936897cfb9a619327a1d85d5ca86ddb7e20e`.

The embedded official style is byte-identical across v5 and both v6 sources, SHA-256 `c3fc2894e83d2517ca18b66741d6c595986d97957dc08ec08bb2125a7ec4555a`. The document class, preprint option, font/package declarations, citation style and tabularx column definition are unchanged. No custom margin, font-size or line-spacing override was added. All three PDFs retain the letter page size, 612 × 792 points. The original roman/monospaced fonts remain; additional embedded Type-1 Computer Modern math fonts serve the new equations.

The numeric renderer passes with 136 placeholders. The submission-text gate reports CLEAN on both TeX variants and rendered Markdown. Named and anonymous scientific TeX bodies are byte-identical. Their complete source diff consists of the author block and PDF author metadata. The named affiliation uses a second line, so removing it in the anonymous version shifts some paragraph/page boundaries; this is an intentional identity-layout consequence, and both still have eight body pages plus references. Neither variant has participant handles in manuscript text or URLs.

## Exhaustive difference classification

The complete extracted-text diffs against v5 are retained as `qa_v6_fidelity/v5-to-named-text.diff` and `qa_v6_fidelity/v5-to-anonymous-text.diff`, alongside all extracted texts and PDF/font metadata. The named diff was read in full, including the reordered supporting tables and removed v5 passages. The anonymous scientific source body is identical; its identity/layout diff is separately retained. Every changed passage maps to the following declared changes.

| Axis | Observed difference | Classification | Rationale/action |
|---|---|---|---|
| Text: title/abstract | Problem-only-control lead replaced by conditional leaderboard identifiability, selected-owner results and exact power | Reported intentional change | v6 lead contribution; original label-identity observation is attributed to prior work |
| Text: task/scope | Task and checkpoint/source descriptions shortened; interpretation of public balance statements made explicit | Reported intentional change | State the evaluation question and distinguish organizer wording from a prior author's stronger report |
| Text: new analysis | Snapshot/parser contract, integer score-grid model, binomial item null, owner selection adjustment, BH, Bonferroni and union-bound sensitivity added | Reported intentional change | Reproducible v6 analysis; fixed-family/conditional-validity and adaptive-stopping qualifications included |
| Text: new planning | Exact current-grid power, first crossings, sustained thresholds and evaluation recommendations added | Reported intentional change | Actionable sample-size analysis; single-method power is explicitly separate from ranking power |
| Text: support | v5 variance/concordance/control results moved to section 4; tables retain the same registered measurements | Reported intentional change | Preserve evidence while condensing it beneath the new lead |
| Text: removed support detail | Prior sample-transfer table, checkpoint list, contextual probe scores, detailed sample-format counts, grouped sample CV, outcome-metadata AUROC and unexecuted external-attempt discussion removed or shortened | Reported intentional change | Condensed v5 support; removed material remains in v5 and the numeric reproduction ledger, and is not converted into a new claim |
| Text: owner evaluation | Owner-bundle private results remain UNMEASURED; receipt expectations are distinguished from predictions and balance proofs | Reported intentional change | No linked owner receipts; two matching aggregate scores could not establish per-problem balance |
| Text: limitations | Dependence directions, hidden-attempt scope, fixed/adaptive attempt counts, calibration, final-test uncertainty and non-rejection/ranking distinctions expanded | Reported intentional change | State practical limits alongside the new statistics |
| Text: front matter/status | Self-limiting status block and author-confirmation placeholders removed; named/anonymous identities supplied | Reported intentional change | Explicit v6 requirement; submission status remains in external execution/publication records |
| Text: references | Participant handles and handle-bearing URLs replaced by neutral titles plus immutable commit pointers; leaderboard/BH references added; unused proposal/portal citations removed | Reported intentional change | Handle-free scientific report with exact source provenance outside the manuscript |
| Text: reproduction/disclosure | v6 tools, dual-source generation, gate fixture scope and current AI assistance replace v5 completion/checklist prose | Reported intentional change | The report describes the artifacts and evidence delivered in this version |
| Formatting: pages | Four body pages plus references become eight body pages plus references | Reported intentional change | Declared content growth; no style compression or expansion |
| Formatting: structure | Four tables become six; zero displayed equations become four; zero subsections become nine | Reported intentional change | New methods/power material and clearer navigation |
| Formatting: reflow | Tables, paragraph/page breaks, reference labels and cross-reference placement change with the new structure | Reported intentional change | Natural reflow under identical style constants; tables/equations fit and citations resolve |
| Formatting: font resources | Math font resources added; all fonts remain embedded Type 1, with no Type 3 | Reported intentional change | Equations require math glyphs; roman/monospaced font choices and body defaults are preserved |
| Formatting: links | External source hyperlinks decrease from nine to six | Reported intentional change | Handle-bearing participant links are moved to research provenance; bibliography still contains nine entries |
| Variants | Named author/affiliation and PDF author metadata become anonymous; scientific source body is unchanged | Reported intentional change | Requested dual artifacts while venue anonymity policy is unresolved |

## Now-false statement scan and visual review

The change invalidates v5's lead-contribution framing, its five-page artifact description and its unconfirmed-author description. Those active manuscript/source/README statements were revised together. Historical v5 artifacts retain their own descriptions. The obsolete “explicit reproduction and sensitivity ledger” lead-contribution sentence is absent. Banned front-matter strings and the known participant handles are absent from final scientific sources and extracted PDF texts. No owner-private measurement was promoted from UNMEASURED.

All eighteen pages in the final named/anonymous contact sheets were inspected. No missing glyph, clipped equation/table, split table, orphan heading or broken citation marker was observed. The anonymous variant's shorter author block causes ordinary reflow, rather than a change to scientific content. Detailed build diagnostics and rendered pages are in `qa_v6_named/` and `qa_v6_anonymous/`; `regen_source_checks_v6.json` records the source, font, page and hash comparisons.

Unreported remaining: **0**. Pages: **9 / 9**, each **8 body + 1 references**. Fidelity verdict: **DONE**. This verdict concerns faithful, declared regeneration and visual quality; statistical assumptions, owner receipts and external publication/submission status remain governed by their separate evidence records.
