#!/usr/bin/env python3
"""Synthetic regression fixtures: these are not author attestations or submissions."""
from copy import deepcopy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("submission_preflight", ROOT / "tools/openreview_submission_preflight.py")
preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)

STATEMENT = """We used AI assistance for Ideation, Coding, Analysis and Writing.
The tools were Anthropic Claude and OpenAI Codex. AI was not used to create
or alter the source leaderboard or robustness labels, fabricate measurements,
or write peer reviews. AI-assisted code computed the reported statistics from
the released source data. The author reviewed all AI-assisted content and
takes full responsibility for the final content."""
SOURCE = "\\section{Main text}\nSYNTHETIC FIXTURE ONLY.\n\\section*{AI Use Statement}\n" + STATEMENT + "\n\\begin{thebibliography}{1}\n\\end{thebibliography}\n"


def synthetic_pdf(path, statement=STATEMENT):
    """Write a small, visibly synthetic text PDF without a TeX dependency."""
    lines = ["SYNTHETIC FIXTURE ONLY", "Main text", "AI Use Statement", *textwrap.wrap(statement, 82), "References", "Synthetic reference."]
    commands = ["BT /F1 10 Tf 45 760 Td 13 TL"]
    for index, line in enumerate(lines):
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        commands.append(("T* " if index else "") + f"({escaped}) Tj")
    commands.append("ET")
    stream = "\n".join(commands).encode("ascii")
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
               b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
               b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
               f"<< /Length {len(stream)} >>\nstream\n".encode() + stream + b"\nendstream"]
    data = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data.extend(f"{number} 0 obj\n".encode() + obj + b"\nendobj\n")
    start = len(data)
    data.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        data.extend(f"{offset:010d} 00000 n \n".encode())
    data.extend(f"trailer << /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n".encode())
    path.write_bytes(data)


class SubmissionPreflightTests(unittest.TestCase):
    def setUp(self):
        self.invitation = preflight.invitation_object(json.loads((ROOT / "attach/fixtures/invitation_live_2026-10-20T0917Z.json").read_text()))
        self.payload = json.loads((ROOT / "attach/fixtures/payload_v7.json").read_text())
        self.invitation.update(cdate=0, duedate=9999999999998, expdate=9999999999999)

    def test_reject_original_false_passes(self):
        cases = [lambda p: p.update(reciprocal_reviewers=["~Non_Author1"]),
                 lambda p: p.update(reciprocal_reviewers=["~Jung_Min_Kang1", "~Other1"]),
                 lambda p: p["authors"][0].pop("fullname"),
                 lambda p: p["authors"][0].update(fullname="   "),
                 lambda p: p.update(reciprocal_reviewers=["~Jung_Min_Kang1", "~Jung_Min_Kang1"]),
                 lambda p: p.update(keywords="not an array"),
                 lambda p: p.update(authors=[{"fullname": "Synthetic", "username": "email@example.org"}])]
        for mutation in cases:
            with self.subTest(mutation=mutation):
                payload = deepcopy(self.payload)
                mutation(payload)
                self.assertTrue(preflight.validate_payload(self.invitation, payload))

    def test_three_authors_require_two_distinct_author_reviewers(self):
        payload = deepcopy(self.payload)
        payload["authors"] += [{"fullname": "Synthetic Second", "username": "~Synthetic_Second1"}, {"fullname": "Synthetic Third", "username": "~Synthetic_Third1"}]
        self.assertTrue(preflight.validate_payload(self.invitation, payload))
        payload["reciprocal_reviewers"] += ["~Synthetic_Second1"]
        self.assertFalse(preflight.validate_payload(self.invitation, payload))
        payload["reciprocal_reviewers"] = ["~Jung_Min_Kang1"] * 2
        self.assertTrue(any("distinct" in error for error in preflight.validate_payload(self.invitation, payload)))

    def test_deadline_is_not_expiration_grace(self):
        now = datetime(2026, 11, 1, 8, 15, tzinfo=timezone.utc)
        self.invitation.update(duedate=1793520000000, expdate=1793521800000)
        self.assertTrue(any("due date has passed" in error for error in preflight.validate_payload(self.invitation, self.payload, now)))

    def test_disclosure_needs_separate_unnumbered_last_section(self):
        pdf = "AI Use Statement\n" + STATEMENT + "\nReferences"
        self.assertEqual(preflight.validate_disclosure(SOURCE, pdf), ([], True))
        for source in [SOURCE.replace("\\section*{AI Use Statement}", "Inline AI Use Statement"),
                       SOURCE.replace("\\section*{AI Use Statement}", "\\section{AI Use Statement}"),
                       SOURCE.replace("\\begin{thebibliography}", "\\section{More main text}\n\\begin{thebibliography}")]:
            self.assertTrue(preflight.validate_disclosure(source, pdf)[0])

    def test_disclosure_does_not_hide_tools_or_derived_data(self):
        pdf = "AI Use Statement\n" + STATEMENT + "\nReferences"
        for missing in ["OpenAI Codex", "source leaderboard", "AI-assisted code computed"]:
            self.assertTrue(preflight.validate_disclosure(SOURCE.replace(missing, "omitted"), pdf)[0])
            self.assertTrue(preflight.validate_disclosure(SOURCE, pdf.replace(missing, "omitted"))[0])

    @unittest.skipUnless(shutil.which("pdftotext") and shutil.which("pdfinfo"), "Poppler required")
    def test_real_gate_and_synthetic_attestation_boundary(self):
        with tempfile.TemporaryDirectory(prefix="synthetic-openreview-") as directory:
            directory = Path(directory)
            invitation = directory / "synthetic-invitation.json"
            payload = directory / "synthetic-payload.json"
            pdf = directory / "synthetic.pdf"
            source = directory / "synthetic.tex"
            invitation.write_text(json.dumps({"invitations": [self.invitation], "count": 1}))
            payload.write_text(json.dumps(self.payload))
            source.write_text(SOURCE)
            synthetic_pdf(pdf)
            result, code = preflight.inspect(invitation, payload, pdf, source)
            self.assertEqual((code, result["technical_checks"], result["result"]), (1, "PASS", "READY_FOR_AUTHOR_REVIEW"), result)
            self.assertEqual(result["author_review_and_attestations"], "NOT_VERIFIED")
            result, code = preflight.inspect(invitation, payload, pdf, source, author_review_confirmed=True)
            self.assertEqual((code, result["result"]), (0, "PREPARED_FOR_AUTHORIZED_SUBMISSION"), result)
            self.assertFalse(result["submitted"])
            # A flag cannot fix missing completed-review wording in the paper.
            prospective = STATEMENT.replace("The author reviewed all", "The author is responsible for reviewing all")
            source.write_text(SOURCE.replace(STATEMENT, prospective))
            synthetic_pdf(pdf, prospective)
            result, code = preflight.inspect(invitation, payload, pdf, source, author_review_confirmed=True)
            self.assertEqual(code, 1)
            self.assertIn("completed author review", " ".join(result["violations"]))
            result, code = preflight.inspect(invitation, payload, ROOT / "attach/fixtures/ctrl_bad.pdf", source)
            self.assertEqual(code, 1)
            self.assertEqual(result["original_gate"]["result"], "BLOCKED")
            self.assertTrue(any("Writing" in error for error in result["original_gate"]["violations"]))

    def test_current_report_source_structural_disclosure(self):
        source = ROOT / "report/main.tex"
        text = source.read_text()
        if "\\section*{AI Use Statement}" not in text:
            self.skipTest("current report has not yet been rendered with the v7 statement")
        body = text.split("\\section*{AI Use Statement}", 1)[1].split("\\begin{thebibliography}", 1)[0]
        errors, _ = preflight.validate_disclosure(text, "AI Use Statement\n" + body + "\nReferences")
        self.assertFalse(errors)


if __name__ == "__main__":
    unittest.main()
