#!/usr/bin/env python3
"""Check a prepared OpenReview package without submitting or granting authority.

Usage: python3 -I tools/openreview_submission_preflight.py INVITATION PAYLOAD PDF \
           --tex-source SOURCE [--author-review-confirmed]

The original payload gate remains an immutable first check. This wrapper adds
schema, reciprocal-reviewer and source/PDF disclosure checks. A technical PASS
without human attestation exits 1 as READY_FOR_AUTHOR_REVIEW. The confirmation
flag may ONLY be supplied after the human author directly confirms review of
the final PDF, all AI-assisted work and the payload's acknowledgements. It is
not inferred from a handoff, a fixture, an agent, or the mere presence of text.
With that confirmation and completed-review wording in the paper, exit 0 means
PREPARED_FOR_AUTHORIZED_SUBMISSION; it never means submitted or authorized.

This checks the invitation supplied by the caller. Its fetch time, external
venue rules and actual account/profile ownership remain independently verified
inputs, not facts established by this local program. No network calls occur.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata


ORIGINAL_GATE_SHA256 = "3a213f34831587bb5eabcfe3fd59e477a2604976c01e54b84e1ff2127fdb865f"
CATEGORIES = {"Ideation", "Coding", "Analysis", "Writing"}
PROFILE = re.compile(r"~\S+")


def invitation_object(value):
    if not isinstance(value, dict):
        raise ValueError("invitation JSON must be an object")
    # An invitation itself also has an `invitations` list of related IDs.
    # Only the API response envelope contains no edit schema at its top level.
    if "edit" not in value and "invitations" in value:
        rows = value["invitations"]
        if not isinstance(rows, list) or len(rows) != 1 or value.get("count", 1) != 1:
            raise ValueError("expected exactly one submission invitation")
        value = rows[0]
    if not isinstance(value, dict) or not isinstance(value.get("id"), str) or not value["id"].endswith("/-/Submission"):
        raise ValueError("not a named submission invitation")
    fields = value.get("edit", {}).get("note", {}).get("content")
    if not isinstance(fields, dict) or not fields:
        raise ValueError("invitation has no note content schema")
    return value


def validate_parameter(value, param, name, errors):
    """Validate the parameter forms used by this venue; fail closed on others."""
    kind = param.get("type")
    if "const" in param:
        if value != param["const"]:
            errors.append(f"{name}: does not match the form constant")
        return
    if kind in ("string", "string[]", "profile[]"):
        multiple = kind.endswith("[]")
        if (multiple and not isinstance(value, list)) or (not multiple and not isinstance(value, str)):
            errors.append(f"{name}: expected {kind}")
            return
        values = value if multiple else [value]
        for item in values:
            if not isinstance(item, str) or not item.strip():
                errors.append(f"{name}: expected nonempty strings")
                continue
            if param.get("regex") and re.fullmatch(param["regex"], item) is None:
                errors.append(f"{name}: string fails form regex")
            if kind == "profile[]" and PROFILE.fullmatch(item) is None:
                errors.append(f"{name}: invalid profile ID")
            if param.get("maxLength") is not None and len(item) > param["maxLength"]:
                errors.append(f"{name}: string exceeds maxLength")
        choices = param.get("enum") or param.get("items")
        if choices:
            allowed = [item.get("value") if isinstance(item, dict) else item for item in choices]
            if any(item not in allowed for item in values):
                errors.append(f"{name}: value is not an exact form choice")
        return
    if kind in ("author{}", "object{}"):
        if not isinstance(value, list) or not value:
            errors.append(f"{name}: expected a nonempty object list")
            return
        properties = param.get("properties", {})
        for index, item in enumerate(value):
            label = f"{name}[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{label}: expected an object")
                continue
            for key in item:
                if key not in properties:
                    errors.append(f"{label}.{key}: unknown object property")
            for key, spec in properties.items():
                child = spec.get("param", {})
                if key not in item or item[key] in (None, "", []):
                    if not child.get("optional"):
                        errors.append(f"{label}.{key}: required property missing")
                else:
                    validate_parameter(item[key], child, f"{label}.{key}", errors)
        return
    errors.append(f"{name}: unsupported form parameter type {kind!r}")


def validate_payload(invitation, payload, now=None):
    errors = []
    if not isinstance(payload, dict):
        return ["payload must be an object"]
    fields = invitation["edit"]["note"]["content"]
    for key in payload:
        if key not in fields:
            errors.append(f"payload.{key}: not a field in the invitation")
    for key, field in fields.items():
        param = field.get("value", {}).get("param", {})
        if key not in payload or payload[key] in (None, "", []):
            if key not in {"pdf", "venue", "venueid"} and not param.get("optional"):
                errors.append(f"payload.{key}: required field missing")
        elif key != "pdf":
            validate_parameter(payload[key], param, f"payload.{key}", errors)
    authors = payload.get("authors")
    reviewers = payload.get("reciprocal_reviewers")
    if isinstance(authors, list) and authors:
        ids = [author.get("username") for author in authors if isinstance(author, dict)]
        if len(ids) != len(authors) or any(not isinstance(item, str) or PROFILE.fullmatch(item) is None for item in ids):
            errors.append("authors: every author needs a valid profile ID")
        if len(set(item for item in ids if isinstance(item, str))) != len(ids):
            errors.append("authors: profile IDs must be distinct")
        expected = 1 if len(authors) <= 2 else 2
        if not isinstance(reviewers, list) or len(reviewers) != expected:
            errors.append(f"reciprocal_reviewers: expected {expected} reviewer(s) for {len(authors)} author(s)")
        elif not all(isinstance(item, str) for item in reviewers):
            errors.append("reciprocal_reviewers: expected profile strings")
        else:
            if len(set(reviewers)) != len(reviewers):
                errors.append("reciprocal_reviewers: reviewers must be distinct")
            if any(reviewer not in ids for reviewer in reviewers):
                errors.append("reciprocal_reviewers: every reviewer must be a listed author")
    if not isinstance(payload.get("ai_assistance"), list) or set(payload["ai_assistance"]) != CATEGORIES:
        errors.append("ai_assistance: this package must disclose Ideation, Coding, Analysis and Writing")
    clock = (now or datetime.now(timezone.utc)).timestamp() * 1000
    if invitation.get("duedate") is None:
        errors.append("invitation: no due date; deadline is not verified")
    elif clock >= invitation["duedate"]:
        errors.append("invitation: submission due date has passed (expiration grace is not the deadline)")
    return errors


def uncomment_tex(source):
    return re.sub(r"(?<!\\)%[^\n]*", "", source)


def plain_text(value):
    value = unicodedata.normalize("NFKD", value)
    value = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", value)
    value = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", "", value)
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def validate_disclosure(source, pdf_text):
    errors = []
    source = uncomment_tex(source)
    heading = list(re.finditer(r"\\section\*\s*\{\s*AI Use Statement\s*\}", source))
    if len(heading) != 1 or len(re.findall(r"AI Use Statement", source, re.I)) != 1:
        return ["TeX: require exactly one separate unnumbered AI Use Statement section"], False
    references = re.search(r"\\begin\s*\{thebibliography\}|\\bibliography\s*\{|\\section\*?\s*\{\s*References\s*\}", source)
    if references is None or references.start() < heading[0].end():
        return ["TeX: AI Use Statement must precede References"], False
    body = source[heading[0].end():references.start()]
    if re.search(r"\\(?:sub)*section\*?\s*\{", body):
        errors.append("TeX: AI Use Statement must follow the last main-text section")
    source_plain = plain_text(body)
    pdf_lower = pdf_text.lower()
    start = pdf_lower.find("ai use statement")
    end = pdf_lower.rfind("references")
    pdf_plain = plain_text(pdf_text[start:end]) if 0 <= start < end else ""
    for label, text in [("TeX", source_plain), ("PDF", pdf_plain)]:
        for term in ["ideation", "coding", "analysis", "writing", "anthropic claude", "openai codex"]:
            if term not in text:
                errors.append(f"{label}: AI disclosure lacks {term!r}")
        if "source leaderboard" not in text or "robustness labels" not in text:
            errors.append(f"{label}: AI disclosure must identify the unchanged source leaderboard and robustness labels")
        if not re.search(r"ai assisted code comput\w*.*(?:statistics|measurements).*source data", text):
            errors.append(f"{label}: disclose AI-assisted derived computations from source data")
        if not re.search(r"(?:not used|did not use|was not used)", text):
            errors.append(f"{label}: AI disclosure must state excluded uses")
        if "responsib" not in text:
            errors.append(f"{label}: AI disclosure must state responsibility")
    reviewed = all(re.search(r"(?:author|authors|we) (?:have |has )?reviewed all ai assisted", text) is not None
                   for text in (source_plain, pdf_plain))
    return errors, reviewed


def inspect(invitation_path, payload_path, pdf_path, tex_source, author_review_confirmed=False, gate_path=None):
    gate_path = Path(gate_path or Path(__file__).with_name("openreview_payload_gate.py"))
    try:
        if hashlib.sha256(gate_path.read_bytes()).hexdigest() != ORIGINAL_GATE_SHA256:
            raise ValueError("original payload gate does not match its pinned SHA256")
        invitation = invitation_object(json.loads(Path(invitation_path).read_text()))
        payload = json.loads(Path(payload_path).read_text())
        source = Path(tex_source).read_text()
        pdf_path = Path(pdf_path)
        pdf_spec = invitation["edit"]["note"]["content"].get("pdf", {}).get("value", {}).get("param", {})
        errors = validate_payload(invitation, payload)
        if pdf_path.suffix.lower() != ".pdf" or not pdf_path.read_bytes().startswith(b"%PDF-"):
            errors.append("PDF: must be a PDF file ending in .pdf")
        if pdf_spec.get("maxSize") and pdf_path.stat().st_size > pdf_spec["maxSize"] * 1024 * 1024:
            errors.append("PDF: exceeds the invitation's maximum file size")
        original = subprocess.run([sys.executable, "-I", str(gate_path), str(invitation_path), str(payload_path), str(pdf_path)],
                                  text=True, capture_output=True, check=False)
        original_result = json.loads(original.stdout)
        if original.returncode:
            errors.append(f"original payload gate returned {original.returncode}")
        pdf_text = subprocess.run(["pdftotext", "-layout", str(pdf_path), "-"],
                                  text=True, capture_output=True, check=True).stdout
        disclosure_errors, reviewed_in_paper = validate_disclosure(source, pdf_text)
        errors.extend(disclosure_errors)
        if author_review_confirmed and not reviewed_in_paper:
            errors.append("paper must confirm completed author review after direct human attestation")
    except (OSError, ValueError, TypeError, KeyError, AttributeError, subprocess.SubprocessError) as error:
        return {"result": "UNREADABLE", "error": str(error)}, 2
    technical = not errors
    result = "BLOCKED" if errors else ("PREPARED_FOR_AUTHORIZED_SUBMISSION" if author_review_confirmed else "READY_FOR_AUTHOR_REVIEW")
    return {
        "result": result,
        "technical_checks": "PASS" if technical else "FAIL",
        "author_review_and_attestations": "CONFIRMED_BY_CALLER" if author_review_confirmed else "NOT_VERIFIED",
        "completed_review_wording": "PRESENT" if reviewed_in_paper else "NOT_CONFIRMED_IN_PAPER",
        "invitation_fetch_freshness": "NOT_VERIFIED_BY_THIS_LOCAL_TOOL",
        "external_venue_rules_and_profile_ownership": "NOT_VERIFIED_BY_THIS_LOCAL_TOOL",
        "submission_authority": "NOT_GRANTED_BY_THIS_TOOL",
        "submitted": False,
        "original_gate": original_result,
        "violations": errors,
    }, 0 if technical and author_review_confirmed else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("invitation")
    parser.add_argument("payload")
    parser.add_argument("pdf")
    parser.add_argument("--tex-source", required=True)
    parser.add_argument("--author-review-confirmed", action="store_true", help="ONLY after direct human confirmation of final PDF, AI-assisted work, and payload acknowledgements")
    args = parser.parse_args()
    result, code = inspect(args.invitation, args.payload, args.pdf, args.tex_source, args.author_review_confirmed)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
