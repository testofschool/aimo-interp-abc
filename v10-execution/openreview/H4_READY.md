# OpenReview H4 execution checklist

Status: **LOCAL PREPARATION ONLY — authentication, note lookup, attachment upload, creation and revision have not run.** This checklist implements the one-note constraint in the directly adopted v10 flow; it grants no additional authority. Keep all existing gates and their actual outcomes visible.

## Inputs to settle before H4

- [ ] Final anonymous PDF has the version-specific H2 confirmation and an exact recorded SHA-256. Main body is at most five pages; AI Use Statement precedes references. Check rendered pages, metadata, attachment filename and source for identity leaks. The invitation still requires real author profiles in private author metadata; PDF anonymity is not achieved by falsifying that field.
- [ ] Actual ID/score receipts and their `testofschool` ownership support the proposed IDs. v8.3 uses baseline 1 then 2; the authorized v9 revision uses probe 3 then control 2. The form ranks only the first two IDs. Queue UUID syntax passing a regex does not establish organizer acceptance or a Codabench user-ID match.
- [ ] Record T-PUSH and H3/G-MIRROR status. If using the adopted handoff's mirror fallback, retain `REPO_URL` failure and the exact fallback wording; do not report a general gate PASS or a live anonymous mirror.
- [ ] Re-fetch the official invitation immediately before each write; preserve tmdate, deadlines, descriptions and a field diff. The retained local snapshot is tmdate **1793023952361**, not evidence of current rules. Stop by the applicable earlier execution cutoff; API expiration is not an extension of the human/organizer deadline.
- [ ] Reuse `tools/openreview_payload_gate.py` and `tools/openreview_submission_preflight.py` for the fresh invitation, actual payload, approved PDF and TeX. Their success does not authenticate receipts, prove author review, establish an anonymous mirror, or permit another note. Verify the on-disk gate hashes before running; no gate changes are proposed here.

## H4 credentials and authenticated read-only reconciliation

1. Felix enters credentials locally in an interactive terminal. Use `getpass.getpass()` for password and OTP; never arguments, environment credentials, saved tokens, key inspection or a transcript. Do not print the client, headers, login result, raw authentication exceptions, pending MFA token, or authentication response.
2. Use explicit `https://api2.openreview.net`. The SDK constructor can otherwise read environment credentials and initiate login. SDK 2.9.1's default OTP prompt uses ordinary `input()` and echoes; use a `getpass` TOTP provider. If email OTP is required, prepare a private local prompt before continuing rather than accepting that default.
3. Confirm the authenticated profile is `~Jung_Min_Kang1`, without dumping account data. Authentication alone is not a submission receipt.
4. Inventory prior local OpenReview note/receipt ledgers and previous execution records. Reconcile every recorded note ID by authenticated `get_note(id=...)`. A filename search that finds no ledger is not proof of zero server notes. Never inspect credentials while locating these records.
5. Enumerate all authenticated authored submission notes, including soft-deleted notes, for the exact venue. SDK `get_notes()` accepts `tauthor`, `signature`, `writer`, `trash`, `limit`, `offset` and `with_count`; paginate completely. `get_all_notes()` does **not** accept `tauthor` in this installed version.
6. Also enumerate the authenticated visible venue submissions with `get_all_notes(invitation=SUBMISSION, trash=True)` and inspect first-author profile metadata locally; do not rely only on titles, public anonymous search, one page of results, or a `tauthor` query. The first author can differ from the account that originally created a note. Reconcile aliases/legacy author fields, signatures/writers, ledger IDs and uncertain matches before deciding there are zero.
7. Store a minimal local reconciliation record: query scope/time, authenticated profile ID, completeness/counts, relevant note IDs and their tmdates, ledger paths/hashes, and the resulting decision. Do not log unrelated papers or author lists.

| Reconciled state | Allowed next action |
| --- | --- |
| One existing report for this first author | Fix its `note.id` in the ledger and **revise that ID only**, including v8.3 to v9. |
| Zero existing reports, all authenticated queries complete and ledger reconciled | Create **one** note once; immediately persist the returned note ID and verify it by readback. |
| Multiple, deleted/withdrawn, unknown, truncated, inaccessible, or conflicting records | Resolve the existing record; do not create a replacement to bypass the one-first-author rule. |

On a creation timeout or unknown result, query and reconcile before any further create call. SDK edit requests can retry POST on 429/5xx. For the eventual create operation, use a single-attempt POST policy and preserve the response/uncertainty; do not assume automatic retries cannot create a duplicate. No write helper is supplied in this preparation.

## Prepare the actual submission or revision

- Required fields in the retained snapshot: `title`, `authors`, `reciprocal_reviewers`, `keywords`, `abstract`, `pdf`, `leaderboard_submission_ids`, `submission_track`, `ai_assistance`, `ai_use_statement`, `reciprocal_reviewing_acknowledgement`, `rules_compliance`, `venue`, `venueid`.
- Use `~Jung_Min_Kang1` as the actual first author and reciprocal reviewer, Small models track, the four disclosed AI assistance categories, and the three acknowledgement values copied exactly from the fresh invitation. Confirm CC BY-SA 4.0 in the note license. Keep White-Box Award unticked and supplementary material omitted for the v8.3 path.
- Bind the upload to the approved anonymous PDF hash. The attachment upload is itself a write and belongs after the execution gates, not this preparation. Never substitute the named PDF.
- For a revision, use `openreview.api.Note(id=EXISTING_NOTE_ID, ...)` with the currently permitted revision invitation. `post_note_edit()` creates or updates; omitting `note.id` is not a revision. Preserve unrelated existing content and its visibility/author metadata. Use API-v2 content cells of the form `{"value": ...}`; the local gate's flat payload is not a directly postable Note.
- After the write, use authenticated `get_note(id=EXISTING_NOTE_ID)` and `get_attachment(field_name="pdf", id=EXISTING_NOTE_ID)`. Verify the exact ID order, track, acknowledgements, unchanged author order, anonymous attachment SHA-256, license and note ID. Record the returned edit ID and server tmdate without inventing either.

## Trial TLDR revision, exact restoration, and final readback

1. Snapshot the original TLDR content cell exactly, including whether it is absent, plus full normalized content and PDF hash. Use the same established note ID for every step.
2. Construct a harmless one-word TLDR addition that remains within the fresh maximum length (currently 250). If no TLDR exists, record that fact and the exact intended temporary value. Run the applicable local payload check before the trial write.
3. Submit only the TLDR change as an edit of that note; fetch the note again and verify the intended trial value, the same note ID, unchanged other content/ID order/PDF hash, and record its actual tmdate/edit ID.
4. Restore the exact original cell. For an originally absent field use the invitation-authorized deletion form, not an empty-string approximation; verify that syntax against the live invitation/API before writing. Fetch again, confirm restoration and unchanged other content, and record its actual tmdate/edit ID.
5. If a trial or restoration has an unknown outcome, read the established note before any retry. If restoration fails, record **RESTORE_PENDING**, retain the original snapshot, and resolve it before declaring completion. Never create a second note for a trial or recovery.

Completion evidence is one note ID, initial/trial/restored server tmdates and edit IDs, the three readbacks, final exact PDF hash and exact ID order, plus the one-note reconciliation record. Later v9 PDFs and official-ID replacements are revisions of this same note after their own required review gates.

## Local review provenance

`SDK_REVIEW.json` records the installed SDK and local invitation hashes. Existing validation scripts were inspected from Git HEAD without executing them. Some direct working-tree file reads stalled; on-disk equality and execution remain to be checked by the executor. No OpenReview SDK client was instantiated, no credentials or authentication environment values were read, and no network request ran during this preparation.
