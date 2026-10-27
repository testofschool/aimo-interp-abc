#!/usr/bin/env python3
"""Audit an authorized official-E4-only revision without editing pinned audits.

The historical queue-UUID assertion is recorded as superseded, never as PASS.
Every other assertion from the authorized disclosure-scoped audit still applies.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PIN = "a1c05d7722dddf4b345ef82f8fe167cac52d6ff0b64c79c7a0e3d07527527645"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compact(value):
    value = value.replace("’", "'").replace("ﬁ", "fi").replace("ﬂ", "fl")
    value = re.sub(r"(?<=[A-Za-z])[-\u00ad](?=\s*[A-Za-z])", "", value)
    return re.sub(r"\s+", "", value)


def font_report_valid(returncode, output):
    lines = output.splitlines()
    if returncode != 0 or len(lines) < 3 or "name" not in lines[0].lower() or set(lines[1].replace(" ", "")) != {"-"}:
        return False
    pattern = re.compile(r"^\S+\s+(?:Type\s+[13]C?|TrueType|CID\s+(?:Type\s+0C?|TrueType))(?:\s+\(OT\))?\s+\S+\s+(?:yes|no)\s+(?:yes|no)\s+(?:yes|no)\s+([0-9]+)\s+([0-9]+)\s*$")
    rows = [pattern.fullmatch(line.strip()) for line in lines[2:] if line.strip()]
    return bool(rows) and all(row is not None and int(row.group(1)) > 0 for row in rows)


def source_proof_valid(proof):
    rows = proof.get("files", [])
    return (len(rows) == 3 and {row.get("file") for row in rows} == {"REPORT_DRAFT.md", "main.tex", "main-anonymous.tex"}
            and proof.get("result") == "PASS" and proof.get("remaining_unreported_source_differences") == 0
            and all(hashlib.sha256((ROOT / "report" / row["file"]).read_bytes()).hexdigest() == row["after_sha256"] for row in rows))


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: audit_official_e4.py PDF")
    pdf = Path(sys.argv[1]).resolve()
    audit_path = ROOT / "v10-execution/audit_v83_ai_exception.py"
    if hashlib.sha256(audit_path.read_bytes()).hexdigest() != PIN:
        raise SystemExit("STOP: original disclosure-scoped audit changed")
    result = subprocess.run([sys.executable, "-I", str(audit_path), str(pdf)], capture_output=True, text=True, timeout=30)
    historical = json.loads(result.stdout)
    binding = json.loads((ROOT / "v10-execution/publication/E4_ARTIFACT_BINDING.json").read_text())
    audit = load("pinned_scoped_audit", audit_path)
    official = load("official_e4_source", ROOT / "tools/official_receipt_numbers.py")
    state = official.inspect()
    numbers = official.numbers(state)
    pages, _, meta = audit.pages_text(str(pdf))
    full = "\n".join(pages)
    draft = (ROOT / "report/REPORT_DRAFT.md").read_text()
    blocks = re.findall(r"Both reference baselines were scored once each on .*?under the declared null\.", draft, re.S)
    expected = blocks[0] if len(blocks) == 3 and len(set(blocks)) == 1 else ""
    source_delta = json.loads((ROOT / "v10-execution/publication/E4_SOURCE_FIDELITY.json").read_text())
    template = json.loads((ROOT / "v10-execution/publication/E4_SOURCE_DELTA.json").read_text())["new_template"]
    native_expected = re.sub(r"\{\{([A-Za-z0-9_]+)\}\}", lambda m: str(numbers[m.group(1)]), template)
    fonts = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True, timeout=15)
    font_lines = fonts.stdout.splitlines()
    type3 = sum(bool(re.search(r"\bType 3\b", line)) for line in fonts.stdout.splitlines()[2:])
    applicable = [row for row in historical["rows"] if row["check"] != "QUEUE_IDS_IN_E4"]
    expected_checks = {"SHA256", "PAGES", "BODY_LE_5", "P5_ENDS_validation_grid", "IDENTITY_0", "URL_ANON", "QUEUE_IDS_IN_E4", "E4_7_14_FAIRCOIN", "CODEX_AI_SCOPE_UNAMBIGUOUS", "FORBIDDEN_0", "CITE_2607_13899", "TYPE3_0"}
    checks = {
        "pinned_audit_executed": result.returncode in (0, 1),
        "complete_historical_checkset": len(historical["rows"]) == len(expected_checks) and {row["check"] for row in historical["rows"]} == expected_checks,
        "exact_build_pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest() == binding["anonymous_pdf_sha256"],
        "build_source_sha256": hashlib.sha256((ROOT / "report/main-anonymous.tex").read_bytes()).hexdigest() == binding["anonymous_source_sha256"],
        "all_applicable_scoped_assertions": all(row["ok"] for row in applicable),
        "historical_queue_only_failure": historical["failed"] == ["QUEUE_IDS_IN_E4"],
        "validated_native_source": state["measured_score_statements_allowed"],
        "strict_anonymous_author_metadata": str(meta.get("/Author", "")) == "Anonymous Author(s)",
        "font_command_success": font_report_valid(fonts.returncode, fonts.stdout),
        "type3_zero": type3 == 0,
        "only_three_E4_source_deltas": source_proof_valid(source_delta),
        "E4_values_match_native_receipts": bool(expected) and blocks == [native_expected] * 3,
        "three_complete_expected_E4_blocks": bool(expected) and compact(full).count(compact(expected)) == 3,
        "official_ids_three_times_each": all(full.count(str(numbers["official_" + method + "_submission_id"])) == 3 for method in ("always_true", "text_length_control")),
        "no_queue_UUIDs_in_current_PDF": all(q not in compact(full) for q in (compact(v) for v in audit.QUEUE_IDS)),
    }
    output = {"result": "PASS" if all(checks.values()) else "FAIL", "checks": checks,
              "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), "historical_scoped_audit": historical,
              "historical_policy_interpretation": "Queue UUID assertion is replaced only by validated official E4 identity/time/score and exact scope checks. Original FAIL remains recorded.",
              "review_basis": "Human-reviewed base8c plus adopted official-E4-only revision waiver; this is not a new human PDF review."}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
