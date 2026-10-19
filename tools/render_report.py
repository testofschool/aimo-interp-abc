#!/usr/bin/env python3
"""Render the report draft from {{key}} placeholders and refuse hand-typed numbers.

    python3 -I tools/render_report.py report/REPORT_OUTLINE.md results/report_numbers.json report/REPORT_DRAFT.md

Exit 1 if (a) a {{key}} does not exist in report_numbers.json, or (b) a decimal number appears in the
outline OUTSIDE a placeholder (e.g. "0.686" typed by hand). Integers in headings/citations are allowed;
any number with a decimal point, or a percentage, must come from a key. Allowed literal exceptions are
listed one per line in report/ALLOWED_LITERALS.txt with a source (e.g. organizer-reported 0.6262 from README).
"""
import json
import os
import re
import sys

PH = re.compile(r"\{\{([A-Za-z0-9_.]+)\}\}")
NUM = re.compile(r"(?<![A-Za-z0-9_])\d+\.\d+%?|(?<![A-Za-z0-9_.])\d+%")


def get(d, key):
    cur = d
    for k in key.split("."):
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur


def main(outline, numbers, out):
    text = open(outline).read()
    nums = json.load(open(numbers))
    allowed = set()
    al = os.path.join(os.path.dirname(outline), "ALLOWED_LITERALS.txt")
    if os.path.exists(al):
        allowed = {l.split()[0] for l in open(al) if l.strip() and not l.startswith("#")}
    errs = []
    registry_path = os.path.join(os.path.dirname(outline), "..", "research", "claims.json")
    registry = {}
    if not os.path.isfile(registry_path):
        errs.append("missing research/claims.json numeric registry")
    else:
        for claim in json.load(open(registry_path))["claims"]:
            if claim["key"] in registry:
                errs.append("duplicate claim key " + claim["key"])
            registry[claim["key"]] = claim["value"]
    for k in PH.findall(text):
        if get(nums, k) is None:
            errs.append(f"unknown key {{{{{k}}}}}")
        elif k not in registry:
            errs.append(f"unregistered key {{{{{k}}}}}")
        elif get(nums, k) != registry[k]:
            errs.append(f"claim mismatch for {{{{{k}}}}}")
    stripped = PH.sub("", text)
    for line_no, line in enumerate(stripped.splitlines(), 1):
        for n in NUM.findall(line):
            if n not in allowed:
                errs.append(f"line {line_no}: hand-typed number '{n}' — use a {{{{key}}}} or list it in ALLOWED_LITERALS.txt with its source")
    if errs:
        print(json.dumps({"result": "FAIL", "errors": errs}, indent=1, ensure_ascii=False))
        return 1
    open(out, "w").write(PH.sub(lambda m: str(get(nums, m.group(1))), text))
    print(json.dumps({"result": "PASS", "placeholders": len(PH.findall(text)), "out": out}))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
