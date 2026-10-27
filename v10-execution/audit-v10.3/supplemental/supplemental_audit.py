#!/usr/bin/env python3
"""Read-only, fixed-artifact supplemental audit. No network or PDF authoring.

This is separate from the pinned audit_v83.py and never grants H2 approval.
PDF comparison ignores page footers, whitespace and display hyphenation; all
other section text must match the explicit R1 transformations below.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata
import xml.etree.ElementTree as ET

PDF_SHA = "2edf06ab6764af045e470acdc77f115700d9cf85303a11d174c80e273c182e51"
REF_SHA = "b740a790bfca2bb0400ea3dc2f5dc84da20a92616b3d12f33d552031ad31dc0a"
URL = "https://anonymous.4open.science/r/aimo-identifiability"
TOKENS = ["testofschool", "gangjeongmin", "Jung Min", "Kang", "Korea", "Felix", "github.com/testofschool"]
RUNS = [
    ("always-robust rule", "bde5e370-4dba-4f19-8291-4a998bfecdcd", "2026-10-24 19:01:28 KST"),
    ("length-and-digit control", "0c736e59-8248-4dee-8e4f-2df037c552d7", "2026-10-24 19:03:37 KST"),
]
E4 = ("Both reference baselines were scored once each through the organizers' temporary evaluation queue during the Codabench outage [11]; these runs are not on the leaderboard. "
      "The always-robust rule scored 7/14 (submission id bde5e370-4dba-4f19-8291-4a998bfecdcd, 2026-10-24 19:01:28 KST) and the length-and-digit control scored 7/14 "
      "(submission id 0c736e59-8248-4dee-8e4f-2df037c552d7, 2026-10-24 19:03:37 KST); each equals the fair-coin expectation and is not separable from it under the declared null.")
CPU_OLD = "We provide CPU reproduction and frozen reference baselines whose private-validation results remain unmeasured."
CPU_NEW = "We provide CPU reproduction rather than additional model runs."
PROVENANCE = "The 24 October temporary-evaluation-queue notice is documented in the supplied v8.3 handoff; the recorded queue responses accompany the archive."
RECEIPT_NEW = "The recorded queue receipt JSONs accompany the reproduction archive."
MASK = "[withheld for anonymous review]"
DISCLOSED = [CPU_NEW, PROVENANCE, MASK, RECEIPT_NEW]
HEADINGS = {
    "abstract": "Abstract",
    "s1": "1 Task and the evidence a leaderboard supplies",
    "s2": "2 A conditional analysis of the visible leaderboard",
    "s3": "3 Exact power and an item-budget design target",
    "limits": "Limitations and sensitivity directions",
    "ai": "AI Use Statement",
    "refs": "References",
    "a": "A Supporting label audit and problem-only controls",
    "b": "B Reproduction and assistance",
}
OLD_HEADINGS = dict(HEADINGS, limits="5 Limitations and sensitivity directions",
                    a="4 Supporting label audit and problem-only controls", b="6 Reproduction and assistance")
OLD_OWNER = ("We retain two frozen Small bundles: a length-and-digit control and an always-robust rule. Their own private-validation results are UNMEASURED because we have no linked owner receipt recording the bundle, submission identifier, status, accuracy and time. "
             "The anticipated constant/control results are receipt expectations motivated by public evidence, not pre-registered predictions of unknown labels. Even if both receipts match those expectations, they would show consistency for those submissions rather than prove exact per-problem balance.")


def words(text):
    """Normalize extraction artifacts; lexical hyphens only, never minus signs."""
    text = unicodedata.normalize("NFKC", text).replace("\u00ad", "")
    text = text.translate(str.maketrans({"’": "'", "–": "-", "—": "-"}))
    text = re.sub(r"-[ \t]*\n[ \t]*(?=\w)", "-", text)
    text = re.sub(r"(?<=[A-Za-z])-(?=[A-Za-z])", "", text)
    return " ".join(text.split())


def page_body(page, number):
    lines = page.strip().splitlines()
    if lines and (lines[-1].strip() == str(number) or (number == 1 and lines[-1].strip() == "Preprint.")):
        lines.pop()
    return "\n".join(lines).strip()


def sections(pages, headings):
    text = "\n".join(page_body(p, i) for i, p in enumerate(pages, 1))
    marks = []
    for key, value in headings.items():
        pattern = r"^[ \t]*" + r"[ \t]+".join(re.escape(x) for x in value.split()) + r"[ \t]*$"
        matches = list(re.finditer(pattern, text, re.M))
        if len(matches) != 1:
            raise ValueError("missing/duplicate section " + key)
        marks.append((matches[0].start(), matches[0].end(), key))
    marks.sort()
    bodies = {"prologue": words(text[:marks[0][0]])}
    for n, (_, end, key) in enumerate(marks):
        bodies[key] = words(text[end:marks[n + 1][0] if n + 1 < len(marks) else len(text)])
    return bodies, [m[2] for m in marks]


def fidelity(pages, reference):
    old, old_order = sections(reference.split("\f")[:-1], OLD_HEADINGS)
    new, new_order = sections(pages, HEADINGS)
    applied = {}

    def replace(key, before, after):
        before, after = words(before), words(after)
        count = old[key].count(before)
        applied[key + ":" + str(len(applied))] = count == 1
        old[key] = old[key].replace(before, after)

    replace("prologue", "Jung Min Kang Independent", "Anonymous Author(s)")
    replace("abstract", "labels. We do not identify which owners were affected. [11]", "labels. [11] We do not identify which owners were affected.")
    replace("abstract", CPU_OLD, CPU_NEW + " " + E4)
    replace("s2", "fetched on October 20 in Korea.", "fetched on October 20 KST.")
    replace("a", "The two frozen bundles are reference baselines (a constant rule and a surface-feature control), planned for one submission each when the service and owner session permit.", "The two frozen bundles are reference baselines (a constant rule and a surface-feature control).")
    replace("a", OLD_OWNER, E4)
    replace("a", "Private-validation receipts are pending.", RECEIPT_NEW)
    for n in (1, 2, 3):
        replace("a", "4." + str(n), "A." + str(n))
    replace("limits", "Private-validation receipts for our frozen reference baselines (a constant rule and a surface-feature control) remain pending; the report has no final-test outcomes.", E4 + " The report has no final-test outcomes.")
    replace("limits", "provide context for evaluation cautions while the owner measurements remain unavailable.", "provide context for evaluation cautions.")
    replace("refs", "Original bytes, source hash and date-provenance notes accompany the evidence manifest in the reproduction archive.", PROVENANCE + " Original bytes, source hash and date-provenance notes accompany the evidence manifest in the reproduction archive.")
    for key in ("refs", "b"):
        replace(key, "https://github.com/testofschool/aimo-interp-abc", URL)
    count = len(re.findall(r"6f81bc3b\s*31472dfeb1179b25c31fd7bb128dd19f", old["b"]))
    applied["b:source_commit_mask"] = count == 1
    old["b"] = re.sub(r"6f81bc3b\s*31472dfeb1179b25c31fd7bb128dd19f", MASK, old["b"])
    equal = {key: old[key] == new[key] for key in old}
    order_ok = old_order == ["abstract", "s1", "s2", "s3", "a", "limits", "b", "ai", "refs"] and new_order == ["abstract", "s1", "s2", "s3", "limits", "ai", "refs", "a", "b"]
    return all(equal.values()) and all(applied.values()) and order_ok, {
        "section_equal_after_explicit_transforms": equal, "transforms_applied_exactly_once": applied,
        "E11_section_order": order_ok, "disclosed_changed_lines_verbatim": DISCLOSED,
        "normalization": "page-number/Preprint footers, Unicode ligatures/quotes/dashes, whitespace and alphabetic display hyphenation; no other text is ignored",
    }


def collect(pdf):
    from pypdf import PdfReader
    reader = PdfReader(pdf)
    extract = subprocess.run([shutil.which("pdftotext") or "pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, timeout=30)
    fonts = subprocess.run([shutil.which("pdffonts") or "pdffonts", str(pdf)], capture_output=True, text=True, timeout=30)
    pages = extract.stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    uris, file_annotations, associated = [], 0, 0
    root = reader.trailer["/Root"]
    xmp = root.get("/Metadata")
    xmp_text = ""
    if xmp:
        xml = ET.fromstring(xmp.get_object().get_data())
        xmp_text = " ".join(list(xml.itertext()) + [v for e in xml.iter() for v in e.attrib.values()])
    associated += len(root.get("/AF", []))
    for page in reader.pages:
        associated += len(page.get("/AF", []))
        for ref in page.get("/Annots", []):
            annotation = ref.get_object()
            file_annotations += annotation.get("/Subtype") == "/FileAttachment"
            action = annotation.get("/A")
            if action:
                action = action.get_object()
                if "/URI" in action:
                    uris.append(str(action["/URI"]))
    return {"sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), "reader_page_count": len(reader.pages),
            "pages": pages, "metadata": {str(k): str(v) for k, v in (reader.metadata or {}).items()},
            "xmp_text": xmp_text, "uris": uris, "embedded_attachment_count": len(reader.attachments),
            "file_attachment_annotations": int(file_annotations), "associated_files_count": associated,
            "extract": {"returncode": extract.returncode, "stderr_present": bool(extract.stderr)},
            "fonts": {"returncode": fonts.returncode, "stdout": fonts.stdout, "stderr_present": bool(fonts.stderr)}}


def validate(snapshot, reference):
    rows = []

    def add(name, ok, value=None):
        rows.append({"check": name, "ok": bool(ok), "value": value})

    pages = snapshot["pages"]
    full = "\n".join(pages)
    add("EXACT_FROZEN_SHA256", snapshot["sha256"] == PDF_SHA, snapshot["sha256"])
    add("REFERENCE_TEXT_SHA256", hashlib.sha256(reference.encode()).hexdigest() == REF_SHA)
    add("TEXT_EXTRACTION_SUCCEEDED", snapshot["extract"]["returncode"] == 0 and len(pages) == snapshot["reader_page_count"] and all(len(p.strip()) > 100 for p in pages))
    add("TOTAL_PAGES_10", snapshot["reader_page_count"] == len(pages) == 10, len(pages))
    unlimited = re.compile(r"^[ \t]*(?:Limitations and sensitivity directions|AI Use Statement|References|Appendix.*)[ \t]*$", re.M)
    p5_lines = page_body(pages[4], 5).splitlines() if len(pages) > 4 else []
    p6_lines = page_body(pages[5], 6).splitlines() if len(pages) > 5 else []
    boundary = len(pages) == 10 and all(not unlimited.search(p) for p in pages[:5]) and bool(p5_lines) and bool(p6_lines) and p6_lines[0].strip() == HEADINGS["limits"] and p5_lines[-1].strip() == "validation grid."
    add("MAIN_ENDS_5_LIMITATIONS_STARTS_6", boundary)
    sources = {"text": full, "document_metadata": json.dumps(snapshot["metadata"]), "xmp_metadata": snapshot["xmp_text"], "URIs": "\n".join(snapshot["uris"])}
    counts = {name: {"token#" + str(i): len(re.findall(re.escape(" ".join(token.casefold().split())), " ".join(value.casefold().split()))) for i, token in enumerate(TOKENS)} for name, value in sources.items()}
    add("IDENTITY_TEXT_METADATA_URI_CASE_INSENSITIVE_ZERO", all(n == 0 for bucket in counts.values() for n in bucket.values()), counts)
    add("AUTHOR_METADATA_REQUIRED_ANONYMOUS", snapshot["metadata"].get("/Author", "").strip() == "Anonymous Author(s)")
    attachments = {k: snapshot[k] for k in ["embedded_attachment_count", "file_attachment_annotations", "associated_files_count"]}
    add("NO_EMBEDDED_ATTACHMENTS", all(v == 0 for v in attachments.values()), attachments)
    font = snapshot["fonts"]
    lines = font["stdout"].splitlines()
    parsed = [re.fullmatch(r"(\S+)\s+(.+?)\s+(\S+)\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+(\d+)\s+(\d+)\s*", line) for line in lines[2:] if line.strip()]
    valid_fonts = font["returncode"] == 0 and len(lines) >= 3 and "object ID" in lines[0] and bool(parsed) and all(parsed)
    type3 = sum(bool(re.fullmatch(r"Type\s+3", m.group(2))) for m in parsed if m)
    add("PDFFONTS_SUCCESS_VALID_ROWS_TYPE3_ZERO", valid_fonts and type3 == 0, {"returncode": font["returncode"], "valid_font_rows": len(parsed) if all(parsed) else 0, "Type3": type3})
    try:
        parts, _ = sections(pages, HEADINGS)
    except ValueError:
        parts = {}
    for key in ("abstract", "limits"):
        part = parts.get(key, "")
        expected = words(E4)
        add("E4_" + key.upper() + "_TWO_SCORE_ID_TIMESTAMP_BINDINGS", expected in part, {"exact_expected_E4_paragraph_present": expected in part})
    add("NO_STRONGEST_NONPERFECT_OWNER_COMPARISON", words("strongest non-perfect owner").casefold() not in words(full).casefold())
    add("FINAL_TEST_UNMEASURED_CONTEXT_PRESERVED", words("Final-test performance of these bundles is also UNMEASURED.") in words(full) and words("The report has no final-test outcomes.") in parts.get("limits", ""))
    add("EXACT_ANONYMOUS_REPOSITORY_URL", full.count(URL) == 2, {"visible_occurrences": full.count(URL), "mirror_verified": False})
    for i, line in enumerate(DISCLOSED, 1):
        add("DISCLOSED_DELTA_" + str(i) + "_PRESENT", words(line) in words(full), line)
    try:
        ok, value = fidelity(pages, reference)
        add("SECTION_FIDELITY_ONLY_EXPLICIT_TRANSFORMS", ok, value)
    except (ValueError, KeyError) as error:
        add("SECTION_FIDELITY_ONLY_EXPLICIT_TRANSFORMS", False, {"error": str(error)})
    return {"result": "PASS" if all(r["ok"] for r in rows) else "FAIL", "failed": [r["check"] for r in rows if not r["ok"]],
            "passed": sum(r["ok"] for r in rows), "total": len(rows), "rows": rows,
            "scope": "Supplemental frozen-artifact checks, separate from pinned audit_v83.py; not scientific truth verification or external receipt authentication",
            "H2": "PENDING", "author_approval": False, "PDF_edited_or_rebuilt": False,
            "full_visual_review": "NOT_RERUN; exact hash anchors prior ten-page visual review"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("reference_text", type=Path)
    args = parser.parse_args()
    try:
        report = validate(collect(args.pdf), args.reference_text.read_text())
    except Exception as error:
        report = {"result": "UNUSABLE", "error_class": type(error).__name__, "H2": "PENDING", "author_approval": False}
        print(json.dumps(report, indent=2))
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
