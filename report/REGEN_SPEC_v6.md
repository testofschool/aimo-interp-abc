# Report regeneration specification, declared before v6 build

Content canon: `aimo-interp-report-v5.pdf`, SHA-256 `1ec9bfb0ac7e48c78ef13ae8ee78d9acdce953bd12bac1038a3bee08719194cf`, the five-page public artifact pinned by HANDOFF v6. Its editable companion is the v5 `REPORT_OUTLINE.md` in public commit `9274840b6faacaa7ad0e321172071eedb822d9de`.

Format canon: v5 `create_source.py`, official NeurIPS 2026 author kit SHA-256 `82473931e3ef710fcd3f4a8cd4119b9de32e56825f90f9e5a6d55f2d01b817d9`, embedded `neurips_2026.sty` SHA-256 `c3fc2894e83d2517ca18b66741d6c595986d97957dc08ec08bb2125a7ec4555a`. Preserve the style bytes, preprint option, document class, package/font choices, tabularx column definition, page geometry and body typesetting defaults. No margin, font-size or line-spacing adjustment is authorized to reach the page target.

The v6 change invalidates the v5 description that problem identity is the lead contribution, that the report has four body pages plus references, and that author identity is unconfirmed. The report README, source metadata and manuscript will be revised together. Historical v5 PDF/QA artifacts remain the canon of their own version.

## Intentional text and structure changes

- Replace the title and abstract with a conditional leaderboard-identifiability analysis; retain the training-label audit as supporting evidence.
- Add the hash-pinned leaderboard parsing contract, finite item-grid assumption, fair-coin item null, independent-submission adjustment and across-owner correction, perfect-score caveats, exact power and sample-size planning.
- Distinguish single-owner chance tests from pairwise ranking and non-rejection from evidence of equal methods. State item, submission and owner dependence limitations, and qualify hidden-attempt sensitivity by its null assumptions.
- Condense the prior problem-only-control, sample-transfer, variance and label-concordance material. Attribute prior balance/identity observations to an earlier public report.
- Remove self-limiting front matter and author-confirmation placeholders. Produce named (Jung Min Kang, Independent) and anonymous variants from one manuscript. Submission status is documented outside the scientific front matter.
- Retain owner-bundle private validation and final test as UNMEASURED; describe expected constant/control outcomes as receipt expectations, never new predictions or proofs of balance.
- Replace participant names/handles and participant-handle URLs in report sources with neutral titles and immutable source commit IDs. Precise source URLs remain in research evidence outside the manuscript.
- Rewrite reproduction and AI disclosure around the v6 tools. Include no new model runs or third-party labelled transfer.
- Add the union-bound-within-owner plus Bonferroni-across-owner sensitivity, which preserves the same survivor count without assuming attempt/owner independence for a fixed family of valid single-submission p-values. Explicitly qualify score-adaptive stopping and conditional validity given observed family/counts.
- Restore the two public label-rule lines verbatim from the pinned dataset card, as inherited HANDOFF v5 R1 requires. This replaces the initial v6 threshold paraphrase with the exact inline-code rules and retains the private-label limitation. Threshold values, measurements and formulas do not change. Rebuild both variants and update all PDF/source hashes, rendered-page review and fidelity records after this correction.
- Delimit the owner private-validation paragraph in the editable outline and save its exact existing text in `OWNER_PRIVATE_VAL_UNMEASURED.md`. The renderer strips delimiters and enforces that canonical UNMEASURED fallback when linked receipts do not authorize measured text. This hardens the build boundary without changing the paper's current owner paragraph or blocking the unrelated leaderboard analysis.

## Intentional formatting changes

- Body target grows from four pages to six–eight pages, plus references. Expected total therefore grows from five to seven–nine pages. Page-count growth follows the new scientific content; the underlying style constants stay fixed.
- Remove the v5 centered status block; author blocks differ only by the requested named/anonymous identity. Title wrapping, table allocation, displayed equations and subsection headings follow the new content.
- Add displayed equations and subsection support to the Markdown-to-TeX generator. Equations are manuscript-controlled source; all measured values still pass through the numeric renderer.

## Required comparison before completion

Extract v5 and both v6 PDF texts; classify differences against this list. Check page counts, fonts (Type-3 count zero), embedded-style hash, package/preamble constants, equation/table fit, citation resolution and a rendered contact sheet of every page. Record the final classified diff in `REGEN_FIDELITY_v6.md`. Any unreported text or formatting change must be corrected or explicitly classified with a rationale before DONE.
