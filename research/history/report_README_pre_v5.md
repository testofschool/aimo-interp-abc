Current v4 status: the method track is folded and owner O2 has not selected
whether to keep the report. This historical pre-J0 draft is preserved unchanged.
See `../EXECUTION_REPORT_v4.md`; no v4 report/PDF has been produced.

# Working report, not a completed submission

This PDF is the **pre-J0 working snapshot** saved at source commit `b990b4d`.
Afterward the owner corrected E2 to train49/evaluate43 and authorized one J0.
Current job measurements, billing and status supersede the draft's earlier
UNRUN/approval-pending statements; see `../EXECUTION_REPORT.md` and `../RUN_STATUS.json`.
The saved source/PDF hashes still identify that historical draft, not a final paper.

`../output/pdf/aimo-control-first-working-draft.pdf` is a five-page working draft:
four body pages and one references page. It records observed control/data audits,
an unselected guarded derivative's host checks, and explicit UNRUN/HOLD challenger
status. It is not the final approximately nine-page report, a private-test result,
a white-box effect claim, or a submitted OpenReview paper. Author/team designation
and final competition format remain pending.

`main.tex` is standalone: it embeds unchanged official `neurips_2026.sty` bytes
using `filecontents*`, then uses the `preprint` option. Source URL and archive/style,
content and source hashes are in `source_provenance.json`. The official author kit
is stored under `research/live_audit/`. No main-track acceptance or anonymity rule
has been imposed on the competition writeup merely by using this layout.

`DRAFT_CONTENT.md` is the editable content source. Run `python3 report/create_source.py`
from the repository root after an intentional content edit. The small converter
supports the current document's paragraphs, headings, tables, links and source
index. It keeps long hash/path strings breakable and builds an inline bibliography.
`main.tex` can also be opened directly in the Codex LaTeX editor for a live preview.

For an independent standard TeX rebuild, run these from `report/`:

```sh
mkdir -p build/local
pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode -output-directory=build/local main.tex
pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode -output-directory=build/local main.tex
pdffonts build/local/main.pdf
pdftoppm -png -r 110 build/local/main.pdf build/local/page
```

There is no external bibliography backend. The observed build used the installed
arxiv-latex-production builder, two pdfTeX passes, automated references/font/key
checks, then visual inspection of all five rendered pages. The first render
clipped the long train hash; line breaks fixed it, and every page was reinspected.
The latest draft has no Type-3 fonts or unresolved citations/references. Exact
commands, final PDF hash, source hash and visual-review scope are preserved in
`render_qa.json`; `pdffonts.txt` stores the font listing. A successful build is
distinct from author approval and submission readiness.
