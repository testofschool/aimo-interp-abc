#!/usr/bin/env python3
"""v9_lead_gate.py — add-on to prize_rubric_gate.py v3 for the v9 lead (D-020).

Runs on the anonymous v9 PDF (or its `pdftotext -layout` text). It checks only the main body
(everything before the first "Limitations" / "AI Use Statement" heading), because that is what
the 5-page rule and the judges read first. Gate v3 must ALSO pass 19/19; this file adds the
checks the 2026-10-26 kill round named.

Exit 0 PASS · 1 FAIL · 2 unusable input. Stdlib + poppler `pdftotext` (or a .txt input).

Sources for each rule (all read 2026-10-26 23:2x KST):
  [SITE]  https://aimo-interp.github.io — "teams considered for awards must submit a technical report with
          details on their submission and its open-sourced implementation"; FAQ 16 "Each OpenReview submission
          must list the Codabench submission IDs it describes".
  [PAPER] arXiv 2607.13899 — "roughly 1200 training and 240 test instances"; footnote 4 "showing the contrary
          would have significant implications ... itself being a valuable contribution".
  [BYEOL] byeolki/aimo-interp report — "so it can succeed by reading problem difficulty" (prior public work).
  [KILL]  2026-10-26 kill round: converged escape named by all three killers (C1, C2, C3).
"""
import re, sys, json, shutil, subprocess

HEAD = re.compile(r"^\s*(?:[0-9A-Z]{1,2}(?:\.[0-9]+)?\s+)?(Limitations\b|AI Use Statement)", re.M)

RULES = [
    ("OWN_SCORED_IDS", "[SITE] FAQ 16 + [KILL]",
     "at least two official Codabench submission ids (numeric) appear in the main body",
     lambda t: len(set(re.findall(r"Codabench submission (?:id|ID)s?\s*#?\s*(\d{5,})", t)) |
                   set(re.findall(r"\bid\s+(\d{6,})\b", t))) >= 2),
    ("WHITEBOX_RUN", "[KILL] converged escape",
     "a white-box probe submission is reported with its own score",
     lambda t: bool(re.search(r"probe", t, re.I)) and bool(re.search(r"scored\s+\d{1,2}/14", t))),
    ("ABLATION", "[SITE] White-Box Award text + [KILL]",
     "the probe is compared against a control with the white-box signal removed (ablation)",
     lambda t: bool(re.search(r"ablation", t, re.I)) and bool(re.search(r"(text|problem)[- ]only|text control|problem-only control", t, re.I))),
    ("PREREGISTERED", "[KILL] C3 escape",
     "the comparison is stated as fixed before the scores were seen",
     lambda t: bool(re.search(r"pre-?registered|fixed before (we saw|scoring)|declared before", t, re.I))),
    ("PRIOR_WORK", "[BYEOL]",
     "the closest public prior work is cited and the difference to it is stated",
     lambda t: bool(re.search(r"byeolki|\[\d+\][^\n]{0,80}(prior|concurrent|public) (report|work)", t, re.I)) and
               bool(re.search(r"(unlike|in contrast to|beyond|what is new|differs from)", t, re.I))),
    ("FINAL_SET_240", "[PAPER] + C1 escape",
     "the board-size result is restated against the organizers' planned 240 test instances",
     lambda t: bool(re.search(r"\b240\b", t))),
    ("BLACKBOX_SUFFICIENCY", "[PAPER] footnote 4",
     "the result is tied to the organizers' open question on whether black-box signals suffice",
     lambda t: bool(re.search(r"black-box", t, re.I)) and bool(re.search(r"suffic|as well as|matches|no better than", t, re.I))),
]


def load(path):
    if path.lower().endswith(".pdf"):
        if not shutil.which("pdftotext"):
            return None, "pdftotext not installed (use the T-TOOLS fallback chain, or pass the .txt)"
        r = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
        return (r.stdout, None) if r.returncode == 0 else (None, r.stderr.strip())
    try:
        return open(path, encoding="utf-8").read(), None
    except OSError as e:
        return None, str(e)


def main(argv):
    if len(argv) != 2:
        print(__doc__); return 2
    t, err = load(argv[1])
    if t is None or len(t.strip()) < 500:
        print(json.dumps({"result": "UNUSABLE", "error": err or "empty text"})); return 2
    m = HEAD.search(t)
    body = t[:m.start()] if m else t
    rows, fails = [], []
    for cid, src, desc, fn in RULES:
        ok = bool(fn(body))
        rows.append({"check": cid, "source": src, "ok": ok, "needs": None if ok else desc})
        if not ok:
            fails.append(cid)
    print(json.dumps({"result": "PASS" if not fails else "FAIL", "failed": fails,
                      "passed": len(rows) - len(fails), "total": len(rows), "rows": rows}, indent=1))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
