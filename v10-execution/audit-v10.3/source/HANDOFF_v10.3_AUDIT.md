# HANDOFF_v10.3 — independent audit of v8.3 before H2, in the same sitting

Executor: **Codex on Felix's M5**, folder `/Users/kangjungmin/Desktop/02_대회·해커톤/AIMO Interpretability Challenge/v84-execution/rebuild/`. This file adds one step before H2. HANDOFF_v10.2 (H2 → push → H3 → H4) and HANDOFF_v10.1 (Codabench uploads, now waiting at H1-auth) are otherwise unchanged.
Written 2026-10-27 09:15 KST by Claude after an audit-crossvalidate round on Codex's two reports (08:53 and 08:59 KST). Attachment: `audit_v83.py` (sha256 in the table below).

## What the audit found (Claude, from the reports alone)

| # | Codex claim | verdict | action |
|---|---|---|---|
| 1 | v10.2 check a ✗ (source mtime earlier than commit) | FALSE ALARM: the check was mis-specified by Claude, since source and PDF were committed together | drop check a |
| 2 | v10.2 check e ✗ (no "§5") | FALSE ALARM: E11 moved old §5 to the unnumbered Limitations by design | read e as "E4 sentence in abstract and Limitations" |
| 3 | numbers **158/158** (08:53) and **164/164** (08:59) | **UNMEASURED inconsistency**: same PDF or a rebuild? | step 1 |
| 4 | f △, 4 extra changes beyond E4/E11/E12/[11] | UNMEASURED for Claude (lines not seen) | step 2 bundle; Claude reads them |
| 5 | body 5 / total 10 pages · gate v3 19/19 · identity 0 · Type3 0 | [self-reported]; promotable by re-measure on the original PDF | steps 2–3 |
| 6 | H2 handoff not recorded as approval | TRUE, correct behaviour | keep |

## Operating rule

Do not pause for Felix except at the human gates below. A mismatch against a pre-registered value is recorded and named in the H2 message; it halts nothing else. H1-auth keeps waiting in parallel. Report once, as part of the H2 message.

## Human gates

| gate | what Felix does | when | dissolves when |
|---|---|---|---|
| H-ATTACH | Drags `AUDIT_BUNDLE_v8.3.zip` from the Desktop into the Claude chat (one file) | same sitting as H2, before typing approval | Claude returns its verdict, or Felix types "v8.3 PDF 확인" without it (then the grade stays [self-reported]) |
| H2 | unchanged (HANDOFF_v10.2) | after H-ATTACH | typed |
| H1-auth | unchanged: password at the local terminal prompt, or "입력창이 보이지 않음" → route D | any time | as in v10.1 |

## Pre-registered values

| id | value | source |
|---|---|---|
| A0 | `audit_v83.py` sha256 `b2bd47f681dc332a6fa17225f9e75f15f4072f7b2543109a938e1e152ec37392` | `shasum -a 256 audit_v83.py` |
| A1 | `python3 -I audit_v83.py <anon.pdf> reference/v8.1-named-approved.txt` → **PASS**, PAGES 10, BODY_LE_5 = 5, IDENTITY_0 hits {}, TYPE3_0 = 0, FORBIDDEN_0 {} | expected from Codex's own reports |
| A2 | Claude's control run: the same script on a different (wrong) PDF → FAIL exit 1; a missing file → exit 2 | run by Claude 2026-10-27 09:10 KST |
| PDF83 | anonymous v8.3 sha256 prefix `2edf06ab`, suffix `82e51` (01:18 report). If it changed, record the old and new values and the commit that changed it | Codex reports |

## Steps

1. **Explain 158 vs 164.** For each of the two numbers, record:
   - the PDF sha256 it was measured on
   - the commit
   - the exact command line
   - the raw `report_numbers.py --check` stdout tail

   Write the result to `v8-execution/AUDIT_numbers.md`. If the PDF changed between 08:53 and 08:59, list the changed source files with byte deltas.
2. **Build `~/Desktop/AUDIT_BUNDLE_v8.3.zip`** containing:
   - the anonymous v8.3 PDF
   - `reference/v8.1-named-approved.txt`
   - `H2_CHECKS.json`, `BUILD_v8.3.json`, `DIFF_v8.3.md`, `AUDIT_numbers.md`
   - the raw stdout of gate v3 (normal mode) and of `report_numbers.py --check`
   - `SHA256SUMS` for every file inside
3. **Run `audit_v83.py`** on the PDF in the bundle with the reference text, and add its JSON as `audit_v83.json` inside the bundle. Python fallbacks, in order: `python3 -m pip install --user pypdf` if pypdf is missing; else the script falls back to pdftotext on its own. Compare against A1 and mark match | MISMATCH.
4. **Put the zip's own sha256 in the H2 message text**, not inside the zip, so the manifest and the artifact ship together. The H2 message then carries:
   - the bundle path and its sha256
   - the A1 comparison
   - the 158/164 explanation in one line
   - the four extra-change lines verbatim
   - the existing H2 content from v10.2
5. **After H2 is typed:** continue HANDOFF_v10.2 step 3 (push → H3 → H4) unchanged.

## Report

Part of the H2 message: bundle sha256 · A1 match|MISMATCH (+ failed checks) · 158/164 explanation · four extra lines · H1 password-gate status (else route D).
