# v7 regeneration specification (declared before the build)

Content canon: the v6 named PDF at public HEAD
`a429a9e71b65e804481394f8b3a5f6799a9a6987`, SHA-256
`6114f15549c07c12efce021a6521d0d72d20c53adc46079d3a4bba9558eef9ef`,
and its anonymous companion, SHA-256
`f1d2a4df94c1669c6f0e2e3dc67c7dda6324b51b8ccc83b28a95a77d79d88ebb`.
Both have nine pages. The corresponding outline, generated Markdown, TeX,
generator and provenance are preserved outside the checkout in
`v7-execution/canon-v6/` before editing.

Format canon: the current `report/create_source.py`, the pinned official
NeurIPS author kit and unchanged embedded style. Preserve preprint mode,
packages, fonts, geometry, table/equation layout and existing body wording.

Intentional changes:

- Replace the inline AI assistance disclosure with one separate unnumbered
  `AI Use Statement`, after the final main-text paragraph and before references.
- Disclose Ideation, Coding, Analysis and Writing, Claude and Codex, and the
  distinction between preserved source observations and AI-assisted derived
  computations. Do not claim that the human author has completed review without
  direct attestation. State the author's review obligation and responsibility.
  The final submission still requires actual author review and the matching
  completed-review confirmation required by the live form.
- Add only the special unnumbered-heading case to the existing TeX generator.
- Render named and anonymous v7 PDFs. Any added space, page reflow or reference
  page shift must follow from the new statement, with no font/margin compression.
- Update current version pointers and metadata; preserve v6 PDFs and evidence.
- Use a derived form payload whose abstract matches the gated report exactly;
  preserve the originally supplied payload as a fixture.

No measured value, registered key, source input, frozen bundle or owner-result
paragraph changes. Without native Codabench receipts, private results remain
UNMEASURED and no submission-pending sentence is added. Prior publication and
owner/future-date evidence remain historical; local v7 checks do not imply a
public release, an account submission, human review or a policy ruling.

Before completion, compare TeX preambles/style bytes, all non-disclosure body
text, numeric tokens, pages, fonts and extracted PDF text against v6; inspect all
rendered pages and record every intentional difference in REGEN_FIDELITY_v7.md.
