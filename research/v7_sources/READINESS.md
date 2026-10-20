# v7 T2/T4 read-only submission preparation

Prepared from live public metadata fetched on 2026-10-20 18:30–18:33 KST (09:30–09:33 UTC). Each fetched file's URL, timestamp, HTTP status, byte count and SHA-256 is in `fetch_manifest.json`. This folder records preparation only. No login, account modification, dataset creation, submission, revision, push or message was performed; no attachment code was executed.

## Observed readiness

| Item | Current evidence |
| --- | --- |
| Codabench competition | 16180, published AIMO Interpretability Challenge |
| Current phase | 30038, Competition phase, current, 2026-09-01T09:00:00Z to 2026-11-01T11:55:00Z |
| Small task | 36241, AIMO Robustness Validation v8 - Small Model Track; task UUID `5b30ceda-7a5f-442c-a58d-9fe770e2f69c` |
| Limit metadata | 10 submissions/day, 300/person for this phase; execution time limit 4200 seconds |
| Leaderboard columns | accuracy, coverage, invalid_predictions; displayed precision 2 |
| Account quota and eligibility | UNVERIFIED: anonymous metadata's used counters are not the owner's authenticated counters |
| Standalone phase/task API GET | HTTP 403 without authentication; exact phase/task are nevertheless visible within competition metadata |
| OpenReview invitation | `NeurIPS.cc/2026/Workshop/AIMOInterp_Challenge/-/Submission`, HTTP 200 |
| Form modification | mdate/tmdate `1792484749788`, 2026-10-20 17:25:49.788 KST; invitation object equals attachment fixture. Only live response wrapper adds `fromCache` |
| Due / expiration | 2026-11-01 17:00 KST / 17:30 KST; do not treat expiration grace as the due time |
| Readers / writers for submitted note | venue and the author profile IDs, not everyone |
| License | only `CC BY 4.0` |
| PDF field | `.pdf`, maxSize 50 in invitation schema |
| Author account | UNVERIFIED. Public profile GET returned a human-verification challenge, HTTP 403; no challenge was attempted |
| Python environment | existing work `.venv` has neither openreview nor requests installed; no installation performed |

Sources: [Codabench competition metadata](https://www.codabench.org/api/competitions/16180/), [OpenReview invitation](https://api2.openreview.net/invitations?id=NeurIPS.cc/2026/Workshop/AIMOInterp_Challenge/-/Submission). Files `codabench_competition.json`, `invitation_live.json`, `openreview_schema_summary.json` retain the fetched detail.

## Exact local Small bundles

The inventory only read ZIP members; it did not import solution code or deserialize joblib.

| Bundle under v6-execution/work/bundles | Bytes | SHA-256 | Members |
| --- | ---: | --- | --- |
| solution-text-length-control-small.zip | 1387 | `30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd` | small.txt, solution.py, artifacts/text_length.joblib |
| solution-always-true-small.zip | 519 | `4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a` | small.txt, solution.py |

Both byte counts and hashes match the preregistered handoff. Member hashes are saved in `small_bundle_inventory.json`. `results/v6/codabench_receipts.json` does not exist as of this read.

## T2 workflow verified against primary code

Current upstream Codabench source was pinned at commit `4b6252a7fb7208187b6aa68cf1ed936209262a99`. This is source evidence, not a verification of the deployed server's exact source revision.

1. After direct authorization and owner authentication, token auth is `POST /api/api-token-auth/`. Keep passwords/token in process memory; never print/save them. The account still has to be approved for this competition.
2. Before creating/uploading anything, authenticated `GET /api/can_make_submission/30038/` returns `{can, reason}`. A false result does not license creating a new account or joining/changing membership automatically.
3. `POST /api/datasets/` needs `type: "submission"`, `request_sassy_file_name`, and nonzero numeric `file_size`; the frontend also sends `file_name` and `competition: 16180`. Name is optional in the model, and if sent must not duplicate an existing dataset name for the user. For the text control the exact file size is 1387; always-true is 519. Do not send the ZIP as JSON or base64.
4. The response returns `key` and `sassy_url`. `PUT` the raw ZIP bytes to that URL with content type `application/zip`, using a separate request that does not forward the Codabench Authorization header. Upstream frontend adds Azure blob headers only for Azure storage; do not invent headers for a different returned storage service.
5. **Correction to handoff:** completion is **`PUT /api/datasets/completed/<key>/`**, not POST. Both the view's method decorator and the frontend use PUT.
6. `POST /api/submissions/` accepts `{"phase": 30038, "tasks": [36241], "data": "<key>"}`. The `tasks` value is a Task primary key, not the phase-task UUID. The serializer checks approved participation, active phase, per-user quota, and tasks belonging to that phase.
7. Preserve the returned submission ID and poll authenticated `GET /api/submissions/<id>/`. Read-only status and score evidence should include the task, owner, status/status_details, timestamp, accuracy, coverage and invalid_predictions. Preserve raw response/readback and a screenshot after native Finished status. The 4200-second metadata is execution limit, not a demonstrated queue-plus-poll completion guarantee.

Primary code: [URLs](https://github.com/codalab/codabench/blob/4b6252a7fb7208187b6aa68cf1ed936209262a99/src/apps/api/urls.py), [dataset serializer](https://github.com/codalab/codabench/blob/4b6252a7fb7208187b6aa68cf1ed936209262a99/src/apps/api/serializers/datasets.py), [dataset views](https://github.com/codalab/codabench/blob/4b6252a7fb7208187b6aa68cf1ed936209262a99/src/apps/api/views/datasets.py), [submission serializer](https://github.com/codalab/codabench/blob/4b6252a7fb7208187b6aa68cf1ed936209262a99/src/apps/api/serializers/submissions.py), [eligibility view](https://github.com/codalab/codabench/blob/4b6252a7fb7208187b6aa68cf1ed936209262a99/src/apps/api/views/submissions.py), [frontend upload methods](https://github.com/codalab/codabench/blob/4b6252a7fb7208187b6aa68cf1ed936209262a99/src/static/js/ours/client.js).

### Actual receipt requirements

The frozen `tools/prereg_codabench_gate.py` expects a top-level `receipts` list containing one row for each preregistered bundle. Each row needs bundle, sha256, track `Small`, submission_id, status `Finished`, accuracy, and timezone-bearing submitted_at later than registration `2026-10-20T00:56:29+09:00`.

The existing `tools/codabench_receipt_scope.py` adds necessary checks: exactly two rows, known/nonduplicate bundles, distinct numeric submission IDs, finite numeric accuracy in [0,1] fitting the registered 14-item displayed grid, no future timestamp, and a real screenshot file named by each row's `screenshot` field, relative to the receipt file's directory. Preserve coverage, task/phase and raw API responses as additional supporting evidence although the frozen gate does not enforce them.

The frozen gate's `CONSISTENT`/`REFUTED_OR_PARTIAL` string is a diagnostic verdict to record verbatim. Two aggregate control accuracies do not establish per-problem label balance. The existing receipt-scope wrapper explicitly prohibits that inference. Missing receipts remain UNMEASURED. No fabricated or placeholder receipt file was created.

## T4 form and revision preparation

Exact live types, enum strings and descriptions are in `openreview_schema_summary.json`. The attachment payload's selected enum strings all match the live schema as fetched. This check did not run or replace the PDF/payload gate.

- Required user content: title, authors, reciprocal_reviewers, keywords, abstract, pdf, ai_assistance, ai_use_statement, reciprocal_reviewing_acknowledgement, rules_compliance. TLDR is optional with maxLength 250; title regex allows 1–250 characters; abstract maxLength is 5000.
- `authors` uses structured author objects including fullname and username; username/profile IDs must match `^~\S+$`. The venue requires author profiles before submission.
- `ai_assistance` exact values: `Ideation`, `Coding`, `Analysis`, `Writing`, `No AI assistance was used`. The no-assistance option is exclusive in meaning.
- `white_box_award` is optional; its only value is `Consider this submission for the White-Box Award`. Omission is permitted, and the payload omits it.
- The three required acknowledgment strings are exact live radio enums; reuse their exact values from the verified JSON. Do not paraphrase those values.
- Sole-author reciprocal reviewing requires one named author and an explicit commitment to assigned reviews on time. The attachment's default nominates `~Jung_Min_Kang1`; that embedded default alone is not direct owner authorization to make the commitment.
- The form requires a separate AI Use Statement after main text and before references; it is excluded from page limit. The statement's truth and the selected usage categories require author review. The form does not specify an anonymity rule or a numeric main-text page limit; absence of such a field does not settle an unseen venue announcement.

Current `openreview-py` source for the methods is pinned to `9a75405b2af20ba242fcc431f8e0ba2fb25e43b6`; fetched file matches master bytes. The minimal API2 call sequence after authorization, account access, and a fresh gate PASS is:

1. Re-fetch invitation and rerun the PDF/payload gate within 10 minutes of any post.
2. `OpenReviewClient(baseurl='https://api2.openreview.net', ...)` using transient owner input; satisfy any human verification through the supported owner flow. The invitation advertises humanVerificationRequired with limit 15/windowMs 3600000. No bypass is prepared.
3. `put_attachment(pdf_path, invitation_id, 'pdf')` uploads using PUT `/attachment` and returns a relative PDF URL. Assign that returned URL to content `pdf: {'value': url}`; wrap each other payload value as `{'value': value}`.
4. `post_note_edit(invitation=invitation_id, signatures=['~Jung_Min_Kang1'], note=Note(license='CC BY 4.0', content=content), await_process=True)` posts to `/notes/edits`. Let invitation-generated readers/writers apply. Preserve returned edit ID and `result['note']['id']`.
5. Read back the note with `get_note(note_id)` and edit history with `get_note_edits(note_id=note_id)`. Record content, PDF URL, true timestamps, read permissions and the native receipt/forum URL. Download the resulting attachment through authorized readback and compare bytes/hash before claiming uploaded-PDF identity.
6. A revision targets the **same** note ID by constructing `Note(id=existing_id, ...)` and posting a note edit under an invitation that still permits it. The current invitation's `note.id` param is optional with matching venueid, so current schema supports this structure. Revision success is UNRUN, and later editing permission is not guaranteed by today's schema. A failed identical-PDF test or unchanged tmdate alone does not prove all future revisions are forbidden; preserve the server error/edit history and determine its actual cause. Do not create a duplicate submission as a workaround.

Sources: [current Python client](https://github.com/openreview/openreview-py/blob/9a75405b2af20ba242fcc431f8e0ba2fb25e43b6/openreview/api/client.py), [official note creation/editing guide](https://docs.openreview.net/how-to-guides/workflow/how-to-create-change-and-delete-notes), [official API authentication overview](https://docs.openreview.net/getting-started/using-the-api).

## Deadline conflicts and next concrete steps

The [official competition website](https://aimo-interp.github.io/) says reports are due by November 15 and shows a November 1–15 report window. The live OpenReview submission form closes much earlier: November 1 at 17:00 KST due, 17:30 KST expiration. Codabench closes November 1 at 20:55 KST, 3 hours 55 minutes after the OpenReview due time. Do not infer that an OpenReview revision is allowed until November 15. Website FAQ's 3600 seconds is the prediction-run budget; phase metadata says 4200 seconds execution. These may cover different scopes and should not be silently substituted.

The safe next work is to complete and verify the local v7 PDFs, preserve the exact two ZIPs, and present the concrete payload/author commitments plus final PDF hash for owner authorization if that authorization is not already present directly in the current session. After authorization and owner access, first use the authenticated Codabench eligibility GET and the current OpenReview form gate. Any Discord-only rules still require the owner's visible native evidence; no Discord interaction was attempted here.
