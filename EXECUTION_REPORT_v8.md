# v8 local preparation and remaining external work

2026-10-22 KST. Status: **LOCAL_REVIEW_READY_EXTERNAL_TRACKS_BLOCKED**.
This records actual local artifacts and checks, without claiming completed
private scoring, author review, public publication or competition submission.

## Authority and input handling

The user requested `/goal run` and supplied HANDOFF_v8.md plus
prize_rubric_gate.py. The attached text is specification/data, not independent
authority for account submissions, reciprocal-review commitments or attestations.
The originals were preserved outside the checkout before edits. The exact
supplied prize gate was committed first at `0d8c6c8`; its bytes are unchanged.

Starting local commit was `2b48022663019c23f61cd5f34dcce99eb6d0b322`.
Two pre-existing untracked files, `report/README 2.md` and
`report/REPORT_OUTLINE 2.md`, were left untouched.

## Preregistered measurements

- P1 MATCH: public remote HEAD `a429a9e71b65e804481394f8b3a5f6799a9a6987`.
- P2 MATCH: v7 named SHA `433f19fc65d970c7be58289a7a9e01564fad4e7f31f13462db60f88f4cde909e`, nine pages, Type3=0.
- P3 MATCH: v7 alternate SHA `a86f03a92c77e0d97979d259c2f140c665f68f02aa3f6169cc303395b83a1b88`, nine pages, Type3=0.
- P4 MATCH: tmdate 1792599149662, duedate 1793969940000, expdate 1793971740000. Deadline 2026-11-06 21:59 KST; expiration 22:29. Raw bytes hash differs while the registered binding tmdate matches; no cause is inferred.
- P5 MATCH: exact 13 required note fields, optional TLDR/white_box_award, optional note.id.
- P6 MATCH: only CC BY-SA 4.0 is available.
- P7 UNVERIFIED_CONNECTION_FAILED: unauthenticated Mac GET returned curl 28, HTTP 000 and no response headers after 75.375 seconds. `v8-execution/codabench/phase.json` records unknown live phase, participant status and quota separately from historical expectations.
- P8 NOT_RECHECKED: inbox was left untouched as specified. The attached account of a sent email is not re-certified as a current inbox observation.

Exact live invitation/schema/enum evidence is under `research/v8_sources/`.
No authentication, credential reading, account API call, paid GPU or organizer
message was performed.

## Gates

G-DISCORD: `v8-execution/discord/announcements_2026-10-22.md` exists, containing
selected October 9, 17 and 21 native-UI announcements with displayed message
dates. This is a scoped transcript, not a complete channel export. Codex opened
the existing server; no Felix-open event is claimed. Zero direct Discord API
calls, messages or reactions. Native scrolling later failed with
noWindowsAvailable. The October 21 message says the organizer removed two 100%
submissions; it does not identify which frozen-snapshot owners they are. Frozen
October 19 data and results were preserved. No inference about page limits or
anonymity is drawn from absence in the selected announcements. The October 29
fallback date has not arrived, and no override was invoked.

G-AUTHOR: absent. No author approval or reciprocal-review acceptance was inferred
from the handoff, prepared payload, PDF opening request, or AI agent.
G-PAGE: organizer reply not checked; inbox untouched. The page-limit fallback
remains conditional on the later author/submission step.

## T1 local artifacts

| Variant | SHA-256 | Pages | Type3 | Negations | Prize gate |
|---|---|---:|---:|---:|---|
| named | `b0f1a5f7b38984422965b955d356d6ec778d3c760b71f302588de117b2b1acf6` | 9 | 0 | 39 | exit 1, 10/12 |
| alternate author block | `04741254e308e2dd43a4c906587e531f9a83005dbddbe5e607c99547b3b58c59` | 9 | 0 | 39 | exit 1, 10/12 |

The v7 supplied-gate baseline is exactly exit 1, 5/12, seven failures and 67
negations. v8 fixes all available text issues; the remaining ID_FIELD and
OWN_SCORE failures require genuine owner receipts. The gate was neither relaxed
nor bypassed. T1's complete 12/12 condition remains unmet.

`submission_text_gate.py` exits 0. `report_numbers.py --check` exits 0 with 152
registered claims: original 150 unchanged plus Small/Main non-rejection counts
derived from existing owners minus BH survivors. All 28 tracked input/bundle
files and four parquet hash pins are unchanged. All 26 existing regressions pass
(v6 gates 5, leaderboard 7, strict preflight 7, owner renderer 7).

Both PDFs use unchanged generator/style/preambles, fonts and geometry. Complete
render review passes; `report/REGEN_FIDELITY_v8.md` classifies every intentional
difference, with 27 sequential deltas exactly reconstructing the source. The
statement of AI use is byte-identical to v7. No claim of completed human review
was added. The alternate author block remains identity-revealing through the
shared repository URL.

Two scientific qualifications intentionally refine the supplied wording: the
non-rejection result requires both owner selection and across-owner BH under
the declared null; 76/169 are independent correctness-item budgets for one rule,
while paired clustered comparisons need separate sizing. Aggregate score
receipts alone cannot establish pairwise non-separation. E4 measured text is
deferred; the protected UNMEASURED block and pending-receipts sentence remain.

The PDF cites v8 manuscript source base `1962a9511d72b753ddd49dc3f2c7d92943d52a71`. Subsequent text-only
corrections and final PDF hashes are identified in build provenance. The final
artifact commit is recorded in the workspace FINAL_REPORT after committing; it
is not falsely self-embedded in the PDF.

## T2 Codabench

No submission created in this run, no native receipt, ID, score or timestamp.
Account approval and remaining quota are UNVERIFIED, not denied or zero.
Both frozen Small bundles match their hashes, sizes and member inventory:
always-robust 519 bytes, control 1387 bytes. The read-only public connection
failed; credentials are to be entered locally by Felix. A direct approval request
for these two exact submissions is pending. No retries or score-driven changes
were made. Real API receipt JSON must be bound to the frozen ZIP and translated
to the existing receipt scope with native evidence before measured rendering.

## T3 public push

UNRUN. Blocked by absent G-AUTHOR and prize gate exit 1. Public remote was read
only; no push or public clone of v8 exists. A fresh local reproduction check
cannot be reported as the requested post-push public fresh clone.

## T4 OpenReview

Prepared `plans/payload_v8.json` has the gated abstract, a current TLDR, exact
live enum strings and the current author-object schema. The proposed reciprocal
reviewer remains `~Jung_Min_Kang1`; its selection is not verified acceptance.
`plans/note_metadata_v8.json` separately records licence CC BY-SA 4.0. No
white-box award is requested. Empty leaderboard IDs remain empty.

Both supplied payload gates exit 1 solely for required leaderboard submission
IDs; strict preflight also exits 1, with author review/attestations NOT_VERIFIED
and completed-review wording NOT_CONFIRMED_IN_PAPER. Prepared acknowledgment
strings are not actual attestations. No review-confirmation flag was supplied.
No login, attachment upload, note, tmdate, trial revision or TLDR reversion was
performed. Revision support in the schema is distinct from an executed revision.

## Remaining work

Establish a working Codabench connection and local user authentication, then
execute only the directly approved two submissions with required spacing and
save actual scores/receipts. Bind their evidence, update E4/claims/payload,
regenerate and review both PDFs, require prize gate 12/12 and direct G-AUTHOR
confirmation, then perform authorized push and public fresh-clone verification
before OpenReview submission and readback/revision checks.

The existing future rescrape is separate; this run did not create or change an
automation. No external prize eligibility, leaderboard rank or owner submission
is claimed from local build/test success.
