# v5 technical draft

`REPORT_OUTLINE.md` is the editable manuscript with numeric placeholders.
`REPORT_DRAFT.md` is its gated rendering. The renderer also requires each key's
registered value in `../research/claims.json`. `ALLOWED_LITERALS.txt` lists sourced
external results, public label thresholds and fixed protocol literals.

`main.tex` is generated from the rendered draft; it embeds unchanged official
`neurips_2026.sty` bytes from the hash-pinned author kit. The prior pre-J0 content
in `DRAFT_CONTENT.md` is historical and no longer the active source.

The delivered `aimo-interp-report-v5.pdf` has five pages: body pages 1-4 and
references page 5. All five final page images were visually checked. There are
no Type-3 fonts, unresolved references, or broken citation markers. All 35 body
decimal tokens checked by the PDF battery are present. Exact PDF/source hashes
are in `render_qa_v5.json`; author-kit/style hashes are in `source_provenance.json`.
PDF binary reproducibility is not claimed because build timestamps can differ.

For a conventional build from the repository root:

```sh
mkdir -p report/build/rebuild
cd report
pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode -output-directory=build/rebuild main.tex
pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode -output-directory=build/rebuild main.tex
pdffonts build/rebuild/main.pdf
pdftoppm -png -r 110 build/rebuild/main.pdf build/rebuild/page
```

There is no external bibliography backend. Compilation is distinct from visual
inspection and submission readiness. Author details/review, native Codabench
results, final portal instructions and the OpenReview receipt remain pending.
Public-remote reproduction passed on 2026-10-20 KST; see `../PUBLICATION.md` and
`../results/v5/publication/`. The scientific manuscript/PDF and their prepublication
QA snapshot remain unchanged. The report includes the evaluation limitation and
peer review commitment checklist. Existing historical PDF/QA files were preserved.
