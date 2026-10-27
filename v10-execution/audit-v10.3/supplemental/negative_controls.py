#!/usr/bin/env python3
"""Invented in-memory mutations of collected observations; no PDFs are authored.

These are negative controls for validator logic, never competition measurements.
"""
import argparse
import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("supplemental", HERE / "supplemental_audit.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("reference_text", type=Path)
    args = parser.parse_args()
    real = audit.collect(args.pdf)
    reference = args.reference_text.read_text()
    baseline = audit.validate(real, reference)
    controls = []

    def control(name, target, mutate):
        fixture = copy.deepcopy(real)
        mutate(fixture)
        result = audit.validate(fixture, reference)
        passed = result["result"] == "FAIL" and target in result["failed"]
        controls.append({"control": name, "expected_failed_check": target,
                         "actual_failed_checks": result["failed"], "correctly_rejected": passed,
                         "fixture_kind": "SYNTHETIC_IN_MEMORY_OBSERVATION_NOT_A_PDF_OR_RECEIPT"})

    control("named Author outside the text token list", "AUTHOR_METADATA_REQUIRED_ANONYMOUS",
            lambda s: s["metadata"].update({"/Author": "A Named Researcher"}))
    control("empty Author", "AUTHOR_METADATA_REQUIRED_ANONYMOUS",
            lambda s: s["metadata"].update({"/Author": ""}))
    control("pdffonts process fails with empty stdout", "PDFFONTS_SUCCESS_VALID_ROWS_TYPE3_ZERO",
            lambda s: s.update(fonts={"returncode": 1, "stdout": "", "stderr_present": True}))
    control("pdffonts exits zero but has no font rows", "PDFFONTS_SUCCESS_VALID_ROWS_TYPE3_ZERO",
            lambda s: s.update(fonts={"returncode": 0, "stdout": "name type encoding emb sub uni object ID\n---\n", "stderr_present": False}))
    control("wrong full SHA", "EXACT_FROZEN_SHA256", lambda s: s.update(sha256="0" * 64))

    def move_uuid(s):
        assert audit.RUNS[0][1] in s["pages"][0]
        s["pages"][0] = s["pages"][0].replace(audit.RUNS[0][1], "SYNTHETIC-MISSING-ID", 1)
        s["pages"][-1] += "\n" + audit.RUNS[0][1]

    control("UUID exists elsewhere but not abstract E4", "E4_ABSTRACT_TWO_SCORE_ID_TIMESTAMP_BINDINGS", move_uuid)
    control("uppercase identity in hidden URI", "IDENTITY_TEXT_METADATA_URI_CASE_INSENSITIVE_ZERO",
            lambda s: s["uris"].append("https://example.invalid/FELIX"))
    control("unexpected embedded attachment", "NO_EMBEDDED_ATTACHMENTS",
            lambda s: s.update(embedded_attachment_count=1))
    control("pdftotext process failure despite stale text", "TEXT_EXTRACTION_SUCCEEDED",
            lambda s: s["extract"].update(returncode=1))
    control("new undisclosed claim in section 3", "SECTION_FIDELITY_ONLY_EXPLICIT_TRANSFORMS",
            lambda s: s["pages"].__setitem__(4, s["pages"][4].replace("validation grid.", "validation grid. This new scientific claim is synthetic.")))
    control("blank page 6 is rejected without indexing exception", "MAIN_ENDS_5_LIMITATIONS_STARTS_6",
            lambda s: s["pages"].__setitem__(5, ""))

    def remove_final_test_unmeasured(s):
        assert sum(p.count("UNMEASURED") for p in s["pages"]) == 1
        s["pages"] = [p.replace("UNMEASURED", "MEASURED") for p in s["pages"]]

    control("removed final-test unknown status", "FINAL_TEST_UNMEASURED_CONTEXT_PRESERVED", remove_final_test_unmeasured)
    controls.append({"control": "Unicode mathematical minus remains distinct", "expected": "words('x−y') differs from words('xy')",
                     "correctly_rejected": audit.words("x−y") != audit.words("xy"),
                     "fixture_kind": "SYNTHETIC_NORMALIZER_DISTINCTION_NOT_A_PDF_OR_RECEIPT"})
    result = {"result": "PASS" if baseline["result"] == "PASS" and all(c["correctly_rejected"] for c in controls) else "FAIL",
              "actual_baseline_result": baseline["result"], "negative_controls_correctly_rejected": sum(c["correctly_rejected"] for c in controls),
              "negative_control_count": len(controls), "controls": controls,
              "PDFs_created_or_modified": 0, "network_requests": 0, "H2": "PENDING"}
    print(json.dumps(result, indent=2))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
