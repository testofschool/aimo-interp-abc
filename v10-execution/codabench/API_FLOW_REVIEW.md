# Codabench v10.1 API flow review

Public source/schema GET only. No authentication, credential use, participant submission list, leaderboard, or outcome request was performed. Competition 16180, phase 30038, task 36241 are the supplied target. The JSON companion inventories downloaded source SHA256 values and exact source URLs. Public throwaway CSRF values in the two HTML snapshots were redacted.

## Exact upload flow

1. `POST /api/datasets/` JSON: `type="submission"`, `competition=16180`, `request_sassy_file_name=<basename>`, `file_name=<basename>`, `file_size=<actual bytes>`. Live client.js 186–195 and Riot 4033–4040. Backend datasets.py 104–144 requires file_size and returns HTTP201 `{key,sassy_url}`.
2. `PUT <returned sassy_url>` raw ZIP, `Content-Type: application/zip`; live client.js 199–225. The observed public platform HTML says `STORAGE_TYPE="s3"`. Azure-only headers are conditional and are not applicable to this observed setting. Do not forward platform CSRF or authorization to the cross-origin signed storage URL, or persist/print that URL.
3. `PUT /api/datasets/completed/{key}/`; live client.js 227–230. Current official backend datasets.py 254–280 checks created_by=request.user, marks completed and returns `{key}`.
4. `POST /api/submissions/` JSON: `{data:key, phase:30038, tasks:[36241], fact_sheet_answers:{}, organization:null, queue:<competition.queue.id or null>, selected_groups:[]}`. Live Riot 4050–4058; use current competition metadata for queue/fact-sheet/group settings. The current official serializer starts the submission when auto_run_submissions is true. Capture HTTP201 native numeric id; an uncertain POST response must be held and reconciled rather than repeated.

## Login and identity verification

The public `/accounts/login/` HTML contains a POST form with username, password, csrfmiddlewaretoken. The official accounts URL source maps it to profiles.views.log_in; views.py 272–323 validates LoginForm, authenticates, logs in and redirects home (or query-string next). The live utils JS, byte-identical to the current official source, attaches `X-CSRFToken` from the current csrftoken cookie to unsafe same-origin API requests. Use current cookie after login, because a successful login may rotate it. Never print/persist password, cookies, session ids, signed URLs, or authenticated HTML.

There is no demonstrated `/me` endpoint in this API schema. The existing frontend provides an evidence-backed identity check: authenticated `GET /`, parse only `CODALAB.state.user` from its inline `JSON.parse` payload, require logged_in=true and username=testofschool. Official context_processors.py14–25 builds this object from request.user and exposes its id. Do not save the entire authenticated HTML or its email/bio fields.

## Own submission list and duplicate checking

Live Riot 2957–2985 calls `GET /api/submissions/?phase=30038&page=1&page_size=...`, no owner parameter. The official backend source at commit `69b44570b9ddf36c3a08b753e90e2299062dc806`, submissions.py112–137 returns none to anonymous callers; nonstaff/nonsuperuser GET visibility is owner OR competition creator/collaborator. Require every returned row.owner to equal testofschool. Never request leaderboard or other participants' outcomes. Backend source is current official repository evidence; the live deployed backend revision was not independently proven.

Handle `{count,next,previous,results}` and same-origin pagination only. Live client also tolerates a bare array. Schema exposes filename, id, parent/children, task and phase but no SHA256 or file_size in the submission list. A unique matching filename with verified owner, phase and Small task can be linked under the latest root-relayed user instruction, while explicitly leaving server bytes/SHA unverified; multiple or contradictory matches must stop before any POST. No broad owner search or guessed filter is needed.

## Score and response schema

GET submission records include id/pk, owner, filename, phase, task, parent/children, status/status_details and scores. `scores` is an array from serializer-submissions.py79–81; each visible score has id,index,score,column_key,precision,is_primary (serializer-scores.py8–19). score is decimal text; is_primary is boolean in source. The live UI displays the primary score or first entry and applies precision. Preserve raw decimal and key; the API does not establish a k/N interpretation or denominator. Keep N unknown unless the actual task scoring contract proves it; do not invent 14.

The generated OpenAPI has known mismatches: missing required file_size; Data create response omits actual sassy_url; completed PUT is labelled no-body; GET scores and is_primary are labelled string despite source/UI semantics. Prefer the exact live frontend plus current official implementation and validate actual owned responses conservatively.

## Parent versus Small score id

Current official `src/apps/competitions/tasks.py` 434–475 creates children only for multiple tasks or multiple group queues. Otherwise it sets the same submission.task to the one task. The CLI requests only [36241], preserves the accepted id and separately verifies the Small score id. If children appear it fetches only child ids named by the owned parent, verifies owner/phase/parent/Small task, and holds on unexpected tasks or multiple Small children rather than treating an aggregate parent score as the Small score.
