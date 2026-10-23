# AIMO-Interp v8.1 execution — 2026-10-24 KST

현재 재빌드 기록은 `EXECUTION_REPORT_T1_REBUILD_2026-10-24.md`를 따른다. 아래는 최초 v8.1 산출물 커밋 4b14400 당시의 보존 기록이다.

Status: **LOCAL_ARTIFACTS_VERIFIED; EXTERNAL_WORK_INCOMPLETE**. Both final PDFs
are nine pages with Type3=0 and 40 main-text negations. All 152 numeric claims
match; the new supplied prize gate passes 15/17. Missing native submission IDs
and scores remain failures, rather than fabricated or waived evidence.

## Request, authority and starting state

The user requested `/goal run`, with an explicit distinction between the user
request and instructions inside supplied documents. All three attachments were
read fully and preserved with hashes in the execution directory. Attached
claims of approval, scheduled actions or organizer acceptance are not authority.
Prior direct October 22 user authorization for the exact two frozen Small bundle
submissions was re-read in the original session and remains valid. Its scope
requires live phase/APPROVED checks, at least two minutes between submissions,
native receipts and no score-driven resubmission. No repeated approval is needed
for that same scope. Credentials must be entered locally by Felix.

The checkout began at 542f44b, a descendant of the specified v7 base, carrying
verified v8 progress. It was reused without reset. Untracked `report/README 2.md`
and `report/REPORT_OUTLINE 2.md` remain untouched. The updated supplied gate was
committed first at 211fc0c. Manuscript source base is
6f81bc3b31472dfeb1179b25c31fd7bb128dd19f. Final artifact commit is recorded in the
execution directory after commit and is not self-embedded in the paper.

## Preregistered values and gates

| Value | Observed outcome |
|---|---|
| P1 public HEAD | MATCH a429a9e71b65e804481394f8b3a5f6799a9a6987 |
| P2 v7 named | MATCH SHA 433f19fc65d970c7be58289a7a9e01564fad4e7f31f13462db60f88f4cde909e; 9 pages; Type3=0 |
| P3 v7 alternate | MATCH SHA a86f03a92c77e0d97979d259c2f140c665f68f02aa3f6169cc303395b83a1b88; 9 pages; Type3=0 |
| P4′ current invitation | MATCH tmdate 1792785352965; due 1793969940000; expiry 1793971740000;exact raw SHA fc1e071245f12c4c8da4f3f2f83135a012d8ccf7158f5c00413d0ca386be3c39 |
| P5 effective schema | MATCH updated P4′: 14 required fields including submission_track; 3 optional including voluntary_reviewers;note.id optional |
| P6 licence | MATCH only CC BY-SA 4.0 |
| P7 phase/tasks/quota/account | UNVERIFIED: three public endpoints timed out before HTTP; no current account or phase state inferred |
| P8 inbox/page reply | NOT_RECHECKED; inbox untouched |
| Transcript | SHA 340ffe7d11f3ad9959804117dfabe726628baae92e2e2327486bbcfaa6c8a7d6 matches supplied expectation |

G-DISCORD evidence is the archived user-supplied transcript. Absolute timestamps
are preserved; relative Yesterday/time-only labels retain their uncertainty.
No direct Discord API call, message or reaction occurred. A later workaround
announcement is not claimed absent from a channel that was not re-read live.
G-AUTHOR is absent: no final PDF review, reciprocal-review commitment, push or
OpenReview approval is inferred from the attachment. G-PAGE remains unresolved.
Public issue 10 gives a tentative nine-page suggestion, not a confirmed cap.

The live invitation due date is November 6 21:59 KST, expiry 22:29. Website and
announcements say November 5 23:59 AoE, equivalent to November 6 20:59 KST, one hour
earlier. Existing D-010 keeps the portal binding; the discrepancy is retained.
The handoff's earlier submission target remains November 5 18:00 KST.

## T1 — local preparation, not full gate completion

| Variant | SHA256 | Pages | Type3 | Negations | Prize gate |
|---|---|---:|---:|---:|---|
| Named | edde59e523d7cc6c7d0cf51565e0b1c0520a42ca6f319844c617da6920841a9c |9|0|40|exit 1; 15/17|
| Alternate author block | debdea93d205e95ce71fb04fe0ad4cda07e7c06a996cc199ba742d6ce49d06af |9|0|40|exit 1; 15/17|

The new gate baseline exactly matches v7 preregistration: 5/17, 12 failures,
67 negations. Current failures are ID_FIELD and OWN_SCORE only. Numeric check
and submission-text gate exit 0; renderer passes 139 numeric placeholders and
keeps the canonical UNMEASURED block. All 152 claim values, numeric keys,
generator bytes, preambles, official style, font families and 31 tracked frozen
input/bundle/tool files are unchanged. Both complete final PDFs were visually
covered and independently rerendered; no material layout defect was found.
`report/REGEN_FIDELITY_v8.1.md` classifies every source/text/format difference.

Scientific qualifications refine unsupported handoff wording: perfect-score
significance is not linked to the two removed submissions; the queue name is
not equated to a protocol solely from an announcement that omits it; 76/169 are
single-rule independent correctness-item budgets, with paired clustered
comparisons separately sized. Marginal receipts cannot support the proposed
pairwise non-separation clause. 11/14 already rejects an uncorrected single-rule
one-sided binomial test at 0.05; its status under a selected-owner/BH family is
a separate calculation. Actual scores must be reported without score-driven
retries or the attachment's blanket non-separability label.

The proposal reference follows the organizer's 14-author citation, matching
arXiv v1; latest v2 has 18 authors. The source version is explicit. The protected
owner paragraph and AI Use Statement are unchanged; completed human review
remains unverified. The alternate author block still exposes identity through
the shared repository URL.

## T2 — UNRUN, service unreachable

Codabench home, competition 16180 and its public API each timed out from this Mac
before HTTP, around 10 seconds. phase 30038 end, Small task 36241 availability,
APPROVED status and quota remain unverified, distinct from denied or zero.
No login, upload, submission, score, receipt or private test outcome was produced.
Existing two-submission authorization is retained. When a working authorized
owner session exists, first re-fetch current phase/account/quota before upload.
A future workaround's actual interface/protocol must be inspected before use.

The November 3 noon fallback is not active on October 24. Organizer issue 10 allows
writeup eligibility without a Codabench submission, but also expects public-train
and private-validation/test evaluation evidence. Literal `none` is syntactically
accepted by the field regex; organizer acceptance of that literal and a local-only
report is UNVERIFIED. The unchanged prize gate still requires real IDs/scores,
so that fallback cannot silently dissolve the gate. Held follow-up text is saved
locally; no Gmail draft/send occurred, and no recurring monitor was created from
the attachment alone.

## T3 and T4 — not executed

No push occurred; public HEAD remains a429a9e. A future push and fresh-clone check
have not run. No OpenReview attachment, note, submission, trial revision or TLDR
revert occurred. Prepared payloads include Small models track, exact fresh enum
strings and the final 1444-character abstract. IDs remain an empty list. The
payload gate exits 1 only for absent IDs. Strict preflight also retains absent
author attestations/completed review. Prepared acknowledgement text is not a
human commitment. White-box award remains omitted.

Reviewer assignments were not read; no reviews were generated. The invitation
requires three reciprocal reviews. The organizer announcement gives review
deadline November 12 23:59 AoE = November 13 20:59 KST. A local calendar line is saved,
not a created calendar event. Felix writes reviews after accepting the obligation.

## Evidence and resumption

Current build/check evidence: `results/v8.1/`. Public portal raw evidence and
bounded connection failures: `v8-execution/resume-2026-10-24/portal/`. Full local
source inputs/canon, authority record, held email and pending-review note are in
that execution directory. Public-source excerpts and schema needed for the
report are also under `research/v8_1_sources/`.

Remaining blockers are service reachability/current account state, authentic
receipts, final author review/attestations, full prize gate and subsequent
publication/submission readbacks. No unavailable evidence has been rounded into
completion. This resumed goal turn leaves the goal incomplete; it does not claim
that a fresh three-turn blocked threshold has been satisfied.
