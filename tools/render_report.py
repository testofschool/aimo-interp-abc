#!/usr/bin/env python3
"""Render the report draft from {{key}} placeholders and refuse hand-typed numbers.

    python3 -I tools/render_report.py report/REPORT_OUTLINE.md results/report_numbers.json report/REPORT_DRAFT.md

Exit 1 if (a) a {{key}} does not exist in report_numbers.json, or (b) a decimal number appears in the
outline OUTSIDE a placeholder (e.g. "0.686" typed by hand). Integers in headings/citations are allowed;
any number with a decimal point, or a percentage, must come from a key. Allowed literal exceptions are
listed one per line in report/ALLOWED_LITERALS.txt with a source (e.g. organizer-reported 0.6262 from README).
"""
import json
import importlib.util
import hashlib
import os
from pathlib import Path
import re
import sys
from datetime import datetime, timezone

PH = re.compile(r"\{\{([A-Za-z0-9_.]+)\}\}")
NUM = re.compile(r"(?<![A-Za-z0-9_])\d+\.\d+%?|(?<![A-Za-z0-9_.])\d+%")
ROOT = Path(__file__).resolve().parents[1]
OWNER_BEGIN = "<!-- BEGIN_OWNER_PRIVATE_VALIDATION -->"
OWNER_END = "<!-- END_OWNER_PRIVATE_VALIDATION -->"
OWNER_FALLBACK_SHA256 = "e51dd37e3eefe81e0163aa20d4fe8c5b68fd9acf99c296506e14b2f448298da2"


def owner_private_validation(text, outline, *, receipts=None, now=None):
    """Select only the owner result paragraph; leave public statistics intact.

    Receipt/time arguments support isolated synthetic tests. The CLI uses the
    actual owner receipt path and current UTC time. A deadline never creates
    evidence, so measured_score_statements_allowed controls the paragraph.
    """
    outline = Path(outline)
    fallback = outline.parent / "OWNER_PRIVATE_VAL_UNMEASURED.md"
    has_markers = "BEGIN_OWNER_PRIVATE_VALIDATION" in text or "END_OWNER_PRIVATE_VALIDATION" in text
    required = outline.name == "REPORT_OUTLINE.md" and fallback.exists()
    if not has_markers and not required:
        return text, None  # Historical v5 outline and unrelated fixture outlines.
    if not fallback.is_file():
        raise ValueError("owner-private configuration error: canonical UNMEASURED fallback is missing")
    if text.count(OWNER_BEGIN) != 1 or text.count(OWNER_END) != 1:
        raise ValueError("owner-private configuration error: exactly one complete marker pair is required")
    begin, end = text.index(OWNER_BEGIN), text.index(OWNER_END)
    if end <= begin:
        raise ValueError("owner-private configuration error: markers are reversed")
    queue_mode = bool(re.search(r"\{\{queue_(?:always_true|text_length_control)_", text))
    section_pattern = r"^##\s+Appendix A[^\n]*$" if queue_mode else r"^##\s+4\.[^\n]*$"
    section = re.search(section_pattern, text, re.M)
    section_end = re.search(r"^##\s+", text[section.end():], re.M) if section else None
    stop = section.end() + section_end.start() if section and section_end else len(text)
    if not section or not section.end() <= begin < end < stop:
        raise ValueError("owner-private configuration error: marker pair must be inside " + ("Appendix A" if queue_mode else "section 4"))
    fallback_bytes = fallback.read_bytes()
    if hashlib.sha256(fallback_bytes).hexdigest() != OWNER_FALLBACK_SHA256:
        raise ValueError("owner-private configuration error: canonical UNMEASURED fallback hash mismatch")
    unmeasured = fallback_bytes.decode("utf-8")
    if not unmeasured.strip() or "OWNER_PRIVATE_VALIDATION" in unmeasured:
        raise ValueError("owner-private configuration error: fallback must be nonempty and marker-free")
    module_name = "queue_receipt_scope_v83" if queue_mode else "codabench_receipt_scope"
    spec = importlib.util.spec_from_file_location(module_name, ROOT / "tools" / (module_name + ".py"))
    scope_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scope_module)
    if queue_mode:
        state = scope_module.inspect(now=now)
        # Queue facts occur in abstract and limitations too. A missing source
        # must block the whole new rendering instead of leaking stale numbers.
        if not state["measured_score_statements_allowed"]:
            raise ValueError("queue receipt source invalid: " + "; ".join(state["errors"]))
    else:
        state = scope_module.inspect(ROOT / "research/PREREG_v6.json",
                                     Path(receipts) if receipts is not None else ROOT / "results/v6/codabench_receipts.json",
                                     now if now is not None else datetime.now(timezone.utc))
    candidate = text[begin + len(OWNER_BEGIN):end].strip()
    if not candidate:
        raise ValueError("owner-private configuration error: authored block is empty")
    allowed = state["measured_score_statements_allowed"]
    selected = candidate if allowed else unmeasured.strip()
    rendered = text[:begin] + selected + text[end + len(OWNER_END):]
    return rendered, {"measurement_status": state["measurement_status"],
                      "rendered_variant": "recorded_owner_scores" if allowed else "canonical_unmeasured",
                      "measured_score_statements_allowed": allowed,
                      "render_gate_expired": state.get("render_gate_expired", False),
                      "source": state.get("source", "CODABENCH_OWNER_RECEIPTS"),
                      "association_basis": state.get("association_basis"),
                      "native_owner_receipt_verified": state.get("native_owner_receipt_verified"),
                      "per_problem_balance_inference_allowed": False}


def get(d, key):
    cur = d
    for k in key.split("."):
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur


def main(outline, numbers, out, *, owner_receipts=None, owner_now=None):
    text = open(outline).read()
    try:
        text, owner_scope = owner_private_validation(text, outline, receipts=owner_receipts, now=owner_now)
    except (OSError, ValueError) as error:
        print(json.dumps({"result": "FAIL", "errors": [str(error)]}, indent=1))
        return 1
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
    result = {"result": "PASS", "placeholders": len(PH.findall(text)), "out": out}
    if owner_scope is not None:
        result["owner_private_validation"] = owner_scope
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
