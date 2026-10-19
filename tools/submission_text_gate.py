#!/usr/bin/env python3
"""submission_text_gate.py — refuse a report source that still carries draft/self-limiting front matter.

Usage: python3 -I tools/submission_text_gate.py report/main.tex [more files]
Exit 0 = clean · 1 = banned strings found (blocks PDF build for OpenReview) · 2 = unreadable.
Why: V1-V4 passed on v5 while the PDF said "Working draft. Not submitted." and "Author ... pending";
a contest postmortem (JUMP AI 2026-09-09) traced elimination to self-imposed text that vacated rubric criteria.
Stdlib only.
"""
import json, re, sys
BANNED = [r"working draft", r"not submitted", r"pending owner confirmation", r"author confirmation pending",
          r"technical draft", r"human author review remains pending", r"author review and final portal instructions pending"]

def main(paths):
    if not paths:
        print("usage: submission_text_gate.py FILE...", file=sys.stderr); return 2
    hits = []
    for p in paths:
        try:
            lines = open(p, encoding="utf-8").read().splitlines()
        except OSError as e:
            print(json.dumps({"result": "UNREADABLE", "file": p, "error": str(e)})); return 2
        for i, line in enumerate(lines, 1):
            for pat in BANNED:
                if re.search(pat, line, re.I):
                    hits.append({"file": p, "line": i, "pattern": pat})
    print(json.dumps({"result": "CLEAN" if not hits else "BLOCKED", "hits": hits}, indent=1))
    return 0 if not hits else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
