#!/usr/bin/env python3
"""Create a standalone draft using unchanged official NeurIPS 2026 style bytes.

The deliberately small Markdown subset matches DRAFT_CONTENT.md. This produces
source, never scientific observations or submission receipts.
"""
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
KIT_SHA = "82473931e3ef710fcd3f4a8cd4119b9de32e56825f90f9e5a6d55f2d01b817d9"
URL = "https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip"


def plain(value):
    chars = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
             "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
             "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
             "′": r"\ensuremath{^{\prime}}", "–": "--", "—": "---",
             "‘": "`", "’": "'", "“": "``", "”": "''", "×": r"\ensuremath{\times}",
             "≤": r"\ensuremath{\leq}", "≥": r"\ensuremath{\geq}"}
    return "".join(chars.get(c, c) for c in value)


def text(value):
    pattern = re.compile(r"\[(S\d+[^\]]*)\]")
    output, end = [], 0
    for match in pattern.finditer(value):
        output.append(plain(value[end:match.start()]))
        keys = []
        reference_part = match.group(1).split(";", 1)[0]
        for first, last in re.findall(r"S(\d+)(?:[–-]S?(\d+))?", reference_part):
            keys.extend(f"S{i}" for i in range(int(first), int(last or first) + 1))
        output.append(r"\citep{" + ",".join(dict.fromkeys(keys)) + "}")
        end = match.end()
    output.append(plain(value[end:]))
    return "".join(output)


def code(value):
    if re.fullmatch(r"[0-9a-f]{40,64}", value):
        return r"\texttt{" + r"\allowbreak{}".join(value[i:i+8] for i in range(0, len(value), 8)) + "}"
    value = plain(value).replace("/", r"/\allowbreak ").replace(",", r",\allowbreak ")
    value = value.replace(r"\_", r"\_\allowbreak ")
    return r"\texttt{" + value + "}"


def inline(value):
    pattern = re.compile(r"`([^`]+)`|\[([^\]]+)\]\((https?://[^)]+)\)|\*\*(.+?)\*\*|(?<!\*)\*([^*]+)\*(?!\*)")
    output, end = [], 0
    for match in pattern.finditer(value):
        output.append(text(value[end:match.start()]))
        if match.group(1) is not None:
            output.append(code(match.group(1)))
        elif match.group(2) is not None:
            output.append(r"\href{" + match.group(3).replace("#", r"\#") + "}{" + text(match.group(2)) + "}")
        elif match.group(4) is not None:
            output.append(r"\textbf{" + inline(match.group(4)) + "}")
        else:
            output.append(r"\emph{" + inline(match.group(5)) + "}")
        end = match.end()
    output.append(text(value[end:]))
    return "".join(output)


def body(markdown):
    lines = markdown.splitlines()
    output, i, abstract, references, started_bib, tables = [], 0, False, False, False, 0
    # Title and status are typeset separately; body derives only from gated draft.
    i = next(n for n, line in enumerate(lines) if line == "## Abstract")
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("## "):
            if abstract:
                output.append(r"\end{abstract}")
                abstract = False
            heading = line[3:]
            if heading == "Abstract":
                output.append(r"\begin{abstract}")
                abstract = True
            elif heading == "Source index":
                references = True
            else:
                output.append(r"\section{" + inline(re.sub(r"^\d+\.\s*", "", heading)) + "}")
            i += 1
            continue
        if references:
            match = re.match(r"- \*\*(S\d+):\*\* (.*)", line)
            if match:
                if not started_bib:
                    output.extend([r"\clearpage", r"\begin{thebibliography}{15}", r"\small\raggedright"])
                    started_bib = True
                output.append(r"\bibitem{" + match.group(1) + "} " + inline(match.group(2)))
            i += 1
            continue
        if line.startswith("|"):
            table = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                    table.append(cells)
                i += 1
            tables += 1
            caption = {
                1: "Observed drop variance grouped by problem; an in-sample description.",
                2: "Observed label agreement; Bernoulli reference is not a significance test.",
                3: "Problem-grouped public Small evaluation; no private competition scores.",
                4: "Public sample transfer with different models and label conventions.",
            }[tables]
            output.extend([r"\begin{table}[htbp]", r"\caption{" + caption + "}",
                           r"\label{tab:" + str(tables) + "}", r"\small",
                           r"\begin{tabularx}{\linewidth}{@{}" + "Y" * len(table[0]) + "@{}}", r"\toprule"])
            for number, cells in enumerate(table):
                output.append(" & ".join((r"\textbf{" + inline(c) + "}" if number == 0 else inline(c)) for c in cells) + r" \\")
                if number == 0:
                    output.append(r"\midrule")
            output.extend([r"\bottomrule", r"\end{tabularx}", r"\end{table}"])
            continue
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("## ") and not lines[i].lstrip().startswith("|"):
            paragraph.append(lines[i].strip())
            i += 1
        output.append(inline(" ".join(paragraph)) + "\n")
    if abstract:
        output.append(r"\end{abstract}")
    if started_bib:
        output.append(r"\end{thebibliography}")
    return "\n\n".join(output)


def main():
    kit = ROOT / "research/live_audit/neurips2026_author_kit.zip"
    if hashlib.sha256(kit.read_bytes()).hexdigest() != KIT_SHA:
        raise SystemExit("STOP: official author-kit bytes changed")
    with zipfile.ZipFile(kit) as archive:
        style = archive.read("neurips_2026.sty")
    if b"\r" in style:
        raise SystemExit("STOP: review line ending normalization before embedding official style")
    content = (HERE / "REPORT_DRAFT.md").read_text()
    prefix = r"""% Standalone working draft; official style embedded unchanged for single-file preview.
\begin{filecontents*}[overwrite]{neurips_2026.sty}
""" + style.decode() + r"""\end{filecontents*}
\documentclass{article}
\usepackage[preprint]{neurips_2026}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb,booktabs,tabularx,array,textcomp}
\usepackage[hidelinks]{hyperref}
\setcitestyle{numbers,square,comma}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\hypersetup{pdftitle={Problem-only controls for robustness prediction in AIMO-Interp},pdfauthor={Author confirmation pending},pdfsubject={Technical draft; private evaluation unmeasured; not submitted}}
\title{Problem-only controls for robustness prediction\\in AIMO-Interp}
\author{Author and team designation pending owner confirmation\\Technical draft}
\begin{document}
\maketitle
\begin{center}
\textbf{Working draft. Not submitted.}\\
\small Public-data CPU audit. Private validation and test: UNMEASURED.\\
Author review and final portal instructions pending; official NeurIPS preprint style.
\end{center}
"""
    source = prefix + body(content) + "\n\\end{document}\n"
    if "\r" in source:
        raise SystemExit("source has CRLF")
    (HERE / "main.tex").write_text(source)
    provenance = {"status": "WORKING_DRAFT_NOT_SUBMITTED", "author_kit_url": URL,
                  "author_kit_sha256": KIT_SHA, "style_sha256": hashlib.sha256(style).hexdigest(),
                  "style_embedded_unmodified": True, "style_option": "preprint",
                  "content_sha256": hashlib.sha256(content.encode()).hexdigest(),
                  "source_sha256": hashlib.sha256(source.encode()).hexdigest()}
    provenance["content_path"] = "report/REPORT_DRAFT.md"
    provenance["content_source"] = "Gated REPORT_OUTLINE.md rendered with results/report_numbers.json"
    (HERE / "source_provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(json.dumps(provenance, indent=2))


if __name__ == "__main__":
    main()
