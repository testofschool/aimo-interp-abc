# HANDOFF_v10 — AIMO-Interp: everything left, in one pass (Codabench is back)

Executor: **Codex on Felix's M5** (MacBook), folder `/Users/kangjungmin/Desktop/02_대회·해커톤/AIMO Interpretability Challenge/` (git HEAD `542f44b` unless HANDOFF_v8.5 work already moved it; record the actual HEAD).
Written 2026-10-27 00:35 KST by Claude. **This file replaces HANDOFF_v8.3, v8.4, v8.5 and v9 as the instruction.** Read the older files only as reference data; where they differ, this file wins.
Attachments: this file · `v9_lead_gate.py` (sha256 `a8a0cede549cdc5fd5add4a55bc2525af8314aa50529925f9cdb12283af0c0c4`) · `SWEEP.json` (the 2026-10-26 direction sweep). Already on the M5: `aimo_v84_bundle.zip` (sha256 `8279ed48…0a8c`, unpacked and verified 7/7 on 10-26), which holds `reference/v8.1-named-approved.pdf`, `reference/v8.1-named-approved.txt`, `HANDOFF_v8.md` (E1–E10 edit list) and `prize_rubric_gate.py` v3.

## 0. What the deliverable is

One OpenReview note (one per first author, ever; later changes are revisions) for the AIMO Interpretability Challenge writeup prize. It carries an anonymous PDF with a main body of ≤5 pages, plus Codabench submission ids **from the `testofschool` account** (site FAQ 16: "Each OpenReview submission must list the Codabench submission IDs it describes; we check that these are linked to the same Codabench user ID").

Two versions of the PDF, built in this order:
- **v8.3 (insurance)**: the approved v8.1 content, cut to a 5-page anonymous body, with official baseline ids. It is posted first.
- **v9 (lead upgrade)**: the 2026-10-26 kill round found that v8.3's lead claim is weakened. The organizers' proposal plans "roughly 1200 training and 240 test instances", which already exceeds our 69–169 item design target. All three killers named the same fix: lead with our own Codabench-scored runs plus a pre-registered ablation, comparing the organizers' trained probe against our text-only control. v9 lands as a **revision** of the same note, and only if Felix says "v9 진행" (H0).

## Operating rule

- Do not pause for Felix except at the human gates below. Every other step carries an ordered fallback chain. If every fallback fails, record the failure and continue every step that does not depend on it.
- Track independence is an outcome: a failure in one track halts only that track. Every other track finishes, posts and reports, naming the failed track.
- A mismatch against a pre-registered value is recorded, and halts only the steps that use that value.
- Report **once**: at the end, or while waiting at a human gate. Batch everything you need from Felix into that message.

## Human gates

| gate | what Felix does | when | dissolves when |
|---|---|---|---|
| H0 | Types **"v9 진행"** or **"v8.3 유지"** | any time; Codex prepares both paths regardless | answered once. "v8.3 유지" cancels only the bundle-3 upload, T-V9 and T-V9-POST |
| H1 | Logs in at https://www.codabench.org as `testofschool`, opens competition 16180 → **Small Model Track**, and uploads the zips Codex prepared, in the order given. Then pastes each submission id and score shown on the page | right after T-ZIP. **Latest 2026-11-01 20:00 KST** (Codabench closes 20:55 KST) | every prepared zip is uploaded and its id is pasted |
| H2 | Opens the anonymous PDF and types "v8.3 PDF 확인" (and later "v9 PDF 확인") | after T-BUILD83 / T-V9 | typed |
| H3 | At https://anonymous.4open.science, signs in with GitHub and creates a mirror: repo `testofschool/aimo-interp-abc`, branch `main`, ID `aimo-identifiability`, terms to hide `testofschool, Kang, Jung Min, felix, gangjeongmin` | right after the first push (same sitting as H2) | `curl -sI https://anonymous.4open.science/r/aimo-identifiability` returns 200 |
| H4 | Types the OpenReview password (and MFA) at the openreview-py prompt; also any git credential the push needs | at T-POST | note posted |
| H5 | Writes 3 reviews as `~Jung_Min_Kang1` | when assigned; due 2026-11-13 20:59 KST | done (missing, late, low-effort or undisclosed-AI reviews mean desk reject) |

Sittings: **tonight** H0 + H1 (bundles 1–2, plus 3 if "v9 진행"). **Next**: H2 + H3 + H4 for v8.3. **Later**: H2 + H4 for v9.

## Pre-registered values

Measured by Claude in its sandbox on 2026-10-26 23:25 to 2026-10-27 00:30 KST (public sources), or recorded on the M5 earlier (marked M5).

| id | value | how to re-measure |
|---|---|---|
| CB1 | `https://www.codabench.org/` → 200 (00:24 KST) | `curl -sI` |
| CB2 | competition 16180, phase "Competition phase" ends `2026-11-01T11:55:00Z` (= 20:55 KST); 10 submissions/day, 300/person; task ids Small 36241, Main 36237 | `curl -s https://www.codabench.org/api/competitions/16180/` |
| OR1 | invitation `NeurIPS.cc/2026/Workshop/AIMOInterp_Challenge/-/Submission` tmdate **1793023952361** (2026-10-26 23:12:32 KST, 7th change: adds optional `supplementary_material` ZIP ≤50 MB); duedate 2026-11-06 21:59 KST; expdate 22:29 KST | `curl -s "https://api2.openreview.net/invitations?id=…/-/Submission"` |
| OR2 | required fields: title, authors, reciprocal_reviewers, keywords, abstract, pdf, leaderboard_submission_ids ("We will evaluate and rank only the first two submission IDs provided"), submission_track, ai_assistance, ai_use_statement, reciprocal_reviewing_acknowledgement, rules_compliance, venue, venueid. Optional: TLDR, voluntary_reviewers, supplementary_material, white_box_award | same fetch |
| D1 | binding report deadline **2026-11-06 20:59 KST** (Discord "Nov 5 11:59 PM AoE"; site "November 5, 2026 (AoE)") | — |
| GS1 | `aimo-interp/getting-started` HEAD `de794053debe75a711400696e66b60937cebbb1b` | `git ls-remote` |
| GS2 | `solutions/trained-probe/probe_artifacts/probe_artifact.pkl` 54,729,307 B, sha256 `8607478c7408922a6490adb7bda34d6a7d95403b7aa62f80dd3f2649139ccdeb` | sha256 after clone |
| P1 | public repo `testofschool/aimo-interp-abc` HEAD `a429a9e71b65e804481394f8b3a5f6799a9a6987` | `git ls-remote` |
| Z1 (M5) | always-robust `solution-always-true-small.zip` 519 B sha256 `4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a`; queue id `bde5e370-4dba-4f19-8291-4a998bfecdcd` = 7/14 | `v8-execution/queue/` |
| Z2 (M5) | length-and-digit control `solution-text-length-control-small.zip` 1387 B sha256 `30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd`; queue id `0c736e59-8248-4dee-8e4f-2df037c552d7` = 7/14 | same |
| S1 | expected official scores for Z1 and Z2: **7/14 each**. The board is balanced per problem and per model; byeolki's report says always-true "scores exactly 0.50" | the H1 paste |
| R1 (M5) | `reference/v8.1-named-approved.pdf` sha256 `31c5ee0c79278c7b31a038acde4ed3f6ff61fbc2dbc361280000fc485b512c95`, 9 pages; its `pdftotext -layout` text sha256 `b740a790bfca2bb0400ea3dc2f5dc84da20a92616b3d12f33d552031ad31dc0a` | sha256 |
| G3 (M5) | `prize_rubric_gate.py` v3 sha256 `152e2a488eb0c3cdeadbe4195bb09ac90acab464df4326a612098dc63f5c7630`, 19 checks | sha256 |
| G9 | `v9_lead_gate.py` sha256 `a8a0cede…c0c4`, 7 checks. Controls run by Claude: good text → PASS exit 0; same text without "ablation" and "240" → FAIL [ABLATION, FINAL_SET_240] exit 1 | rerun the controls in T-V9 |
| BY | byeolki/aimo-interp HEAD `0bbdcac000bfbef3d9317cbf5664eeec2ce00fec`; `report/report.pdf` title "Prompt Probes Read Solve Rate, Not Robustness" | `git ls-remote`; read the PDF |

## Tracks

### T-PRE — preflight (record every line)

1. Run `command -v git python3 zip curl gh`. For `pdftotext pdfinfo pdffonts`, try each in order:
   - `command -v pdftotext` → else `brew install poppler` if brew exists
   - → else micromamba, user-level:
     ```
     mkdir -p ~/mm && curl -Ls https://micro.mamba.pm/api/micromamba/osx-arm64/latest | tar -xvj -C ~/mm bin/micromamba
     ~/mm/bin/micromamba create -y -p ~/mm/env -c conda-forge poppler
     export PATH="$HOME/mm/env/bin:$PATH"   # also append to ~/.zprofile
     ```
   - → else `python3 -m pip install --user pdfminer.six pypdf`: use `pdf2txt.py` for text and `pypdf` for page counts, and record "gates run without poppler".
2. Network: `curl -sI` to codabench.org, github.com, huggingface.co, api2.openreview.net, anonymous.4open.science. A failure is recorded; the tracks that need that host stay pending until it answers, and all others continue.
3. Check `openreview-py` with `python3 -c "import openreview"`; if it is missing, use `python3 -m pip install --user openreview-py`, else use a venv (`python3 -m venv ~/orvenv`).
4. Record RAM (`sysctl hw.memsize`) and free disk.
5. Re-measure CB1, CB2, OR1, GS1, P1 and record match | MISMATCH.

### T-ZIP — the Codabench bundles (runs now; no H0 needed for bundles 1–2)

1. Bundle 1 = Z1 and bundle 2 = Z2, byte-identical. Check sha256. If a file is missing, rebuild it from the repo source with `small.txt` at the zip root, record the new hash, and continue.
2. Bundle 3 = the organizers' trained probe, unmodified, built per the getting-started README:
   ```
   git clone --depth 1 https://github.com/aimo-interp/getting-started v9-execution/gs   # fallback: GitHub "Download ZIP" of de794053
   cd v9-execution/gs/solutions/trained-probe && touch small.txt
   zip -r ../../../bundle3-trained-probe-small.zip solution.py probe_inference.py probe_artifacts small.txt
   ```
   Check GS1 and GS2. Change no byte of the organizers' code: the report presents it as their probe, scored under our account.
3. **Before any upload**, write and commit `v9-execution/PREREG.md`. Its commit time must precede the bundle-3 score. Text:
   > Pre-registered 2026-10-27 (commit time). Small Model Track validation board, Codabench competition 16180. Bundles: (1) always-true, (2) length-and-digit text control, (3) the organizers' trained probe (getting-started de794053, unmodified). Primary test: probe (3) vs text control (2), paired exact McNemar on per-item predictions if Codabench exposes them, else an exact two-sided binomial comparison of the two accuracies; α = 0.05. Secondary: the number of paired items needed for 80% power to separate the observed accuracies, from the report's existing power code. Both outcomes are reported.
4. Write `v9-execution/ZIPS.json` with name, bytes, sha256 and upload order 1, 2, 3.
5. Send Felix the H0 + H1 message: the three zips, the upload order, and the note "bundle 3 only if v9 진행". If Felix prefers, he can instead `export CODABENCH_TOKEN=…` in the Codex shell and Codex submits through the API; otherwise the browser upload (H1) is the path.

### T-SCORE — record the official runs (after H1)

1. For each pasted id: read status and score through `https://www.codabench.org/api/submissions/<id>/` → else the competition's submission list with Felix's session token → else take the score Felix pasted. Write `v9-execution/SCORES.json` with id, task, score as k/14, coverage, finished time in KST.
2. Compare bundles 1–2 to S1 (7/14). Record a mismatch, and still use the measured values.
3. If bundle 3 ran: try to download each submission's prediction output (the ingestion writes `predictions.jsonl`). Run the PREREG test with paired data if the download works, else unpaired, and record which. Write `v9-execution/ABLATION.json`.
4. All numbers enter documents only through `report_numbers.py` (no hand-typed decimals; D-003).

### T-CANON — rebuild v8.1 on the M5 and prove it equals the approved PDF

1. `git switch -c v10 <HEAD>`. If HANDOFF_v8.5 already built `v8.1-rebuilt-on-m5`, reuse that commit and record it.
2. Install gate v3 as `tools/prize_rubric_gate.py` (check G3) and commit.
3. Apply to the LaTeX source every text change between `542f44b` and v8.1: `HANDOFF_v8.md` §2 E1–E10, plus the AI Use Statement sentence "The author has reviewed all AI-assisted work and takes full responsibility for the final content, including AI-assisted text, claims, code, reported statistics and other artifacts." Use `reference/v8.1-named-approved.txt` as the answer key.
4. Acceptance:
   - `diff <(tr -s ' \n' < reference/v8.1-named-approved.txt) <(tr -s ' \n' < rebuilt.txt)` = 0 lines
   - `report_numbers.py --check` exit 0
   - 9 pages
   - Type3 fonts 0
5. If the diff is still not 0 after your best effort, record the remaining lines verbatim, continue on the closest rebuild, and mark the H2 message "T-CANON residual diff: N lines (attached)". Felix decides at H2.

### T-BUILD83 — v8.3 anonymous (the insurance PDF)

Edits on top of T-CANON:
- **E4, own runs.** Replace every "unmeasured" baseline sentence (end of abstract, §4.1, §5) with:
  > Both reference baselines were scored once each on the official Codabench Small Model Track: the always-robust rule scored k1/14 (Codabench submission id ID1, YYYY-MM-DD HH:MM KST) and the length-and-digit control scored k2/14 (Codabench submission id ID2, YYYY-MM-DD HH:MM KST), which is the fair-coin expectation and is not separable from it under the declared null.

  Values come from SCORES.json; timestamps must keep the ISO form "YYYY-MM-DD HH:MM" because gate v3 OWN_SCORE needs it. Fallback if H1 has not happened by T-BUILD83 time: use the queue sentence with the two queue UUIDs (Z1/Z2) and 2026-10-24 19:01:28 / 19:03:37 KST, prefixed "through the organizers' temporary evaluation queue during the Codabench outage [announcements, 24 October]; these runs are not on the leaderboard". Swap it out by revision once official ids exist.

  Compare only with the fair-coin expectation. Never write a comparison with "the strongest non-perfect owner".
- **E11, five-page body.** Order: §1 Task, §2 Leaderboard analysis, §3 Power and design target → Limitations (old §5) → AI Use Statement → References → Appendix A (old §4 with its figures and tables) → Appendix B (old §6). Fix cross-references ("§4" becomes "Appendix A"). Moved text stays word-for-word. If the body is still over 5 pages, shorten only §2.3's prose.
- **E12, anonymize.**
  - Repository URL → `https://anonymous.4open.science/r/aimo-identifiability`.
  - Delete "in Korea" and keep "KST".
  - PDF Author metadata "Anonymous Author(s)".
  - Move the abstract's "[11]" to the end of the removal sentence.
  - Build the named variant too, with the GitHub URL, for the public repo only.
- **Gates** (all required on the anonymous PDF):
  - `report_numbers.py --check` 0
  - `submission_text_gate.py` 0
  - `python3 tools/prize_rubric_gate.py <anon.pdf>` normal mode **PASS 19/19** exit 0
  - Type3 0
  - `pdftotext` diff v8.1 → v8.3 shows only E4, E11 moves, E12 and the [11] move

  If a gate fails, fix the source and rebuild, up to 5 iterations; never edit a gate. After that, send H2 anyway with the gate JSON and the failures named.
- Write `v8-execution/BUILD_v8.3.json` (hashes, pages, MAIN_BODY value, gate JSON) and commit. Send H2 + H3 in one message: the anonymous PDF, the diff summary, the sentence to type, the mirror steps.
- After H2, record `AUTHOR_APPROVAL_v8.3.json` with the same fields as v8.1, plus the anonymous PDF's sha256.

### T-PUSH — publish the repo (after H2 on v8.3)

1. Push branch `v10` to public `main` within 10 minutes of H2, no later than 2026-11-05 12:00 KST. On non-fast-forward, run `git pull --rebase origin main` and push again; never force-push. On an auth failure, run `gh auth status`; if gh is logged in, run `gh auth setup-git` and push again, else list the exact error and Felix types the credential at H4.
2. Done means all three:
   - `git ls-remote` HEAD equals the local commit
   - a fresh clone passes `report_numbers.py --check`
   - `git ls-files | grep -c private` = 0
3. Then H3 (mirror). Report identity-term hits in the mirrored README as a count only.

### T-POST — the one OpenReview note (after T-PUSH; H3 preferred, not required)

1. Re-fetch the invitation. If tmdate ≠ OR1, diff the fields, re-run `openreview_payload_gate.py`, and fill any new required field from facts in this file; otherwise ask at H4.
2. Post **one** note:
   - pdf: v8.3 anonymous
   - `leaderboard_submission_ids`: official ID1, ID2 if they exist, else the two queue UUIDs
   - `submission_track`: `["Small models track"]`
   - reciprocal_reviewers: `[~Jung_Min_Kang1]`
   - ai_assistance: `[Ideation, Coding, Analysis, Writing]`
   - the three fixed sentences, copied from the live JSON
   - license CC BY-SA 4.0
   - title, abstract, TLDR and keywords from v8.3 (no names, no URLs)
   - white_box_award unticked
   - supplementary_material omitted
3. Run a trial revision (TLDR plus one word), revert it, and read the note back after each step.
4. If H3 is not done by T-POST time, post anyway with "Code: anonymized repository link provided upon request to the organizers" in place of the URL, record the gate as failing REPO_URL only, and revise once the mirror exists.
5. Done means: note id, three tmdates, and a readback where the ids equal the posted ids and the pdf matches the anonymous v8.3 sha256.

### T-V9 — the v9 report (prepare after T-BUILD83; post only after H0 = "v9 진행" and a bundle-3 score)

Build on the v8.3 anonymous source. Main body ≤5 pages.
- **§1 Task and the shortcut.** Keep the v8.3 §1 core. Cite byeolki's public report as concurrent work and state in one sentence what is new: official scored runs on the post-16-October board, and a pre-registered paired test.
- **§2 Pre-registered ablation on the scored board.**
  - Bundles 1–3 with ids, k/14 scores and KST timestamps.
  - The PREREG test and its result.
  - The items needed to separate the probe from the control.
  - Tie it to the organizers' open question (proposal footnote 4: whether black-box signals suffice).
  - Wording: the probe is "the organizers' trained probe, unmodified", never ours.
- **§3 Board size**, shortened from v8.3 §2–§3. Keep the sentences gate v3 needs ("59 of 61", "40 of 41", "at least 76 … 169 … paired … problem-clustered", "design target … not as a statement about the unpublished final set"). Add one sentence on power at the organizers' planned 240 test instances, from the existing power code.
- Then Limitations → AI Use Statement → References → Appendix A (label audit) → Appendix B (reproduction).
- **Gates**:
  - `report_numbers.py --check` 0
  - `submission_text_gate.py` 0
  - gate v3 on the anonymous v9 PDF **PASS 19/19**
  - `python3 -I v9_lead_gate.py <anon v9.pdf>` **PASS 7/7**
  - Type3 0

  Before trusting `v9_lead_gate.py`, run it on two control .txt files and expect PASS, then FAIL:
  - good: ≥600 characters containing "Pre-registered", "scored 8/14 (Codabench submission id 412345", "Codabench submission id 412346", "ablation", "text-only control", "Unlike byeolki", "black-box control matches", "240", then a line "Limitations"
  - bad: the same text with "ablation" and "240" removed

  Iterate on failures up to 5 times; never edit a gate.
- Write `v9-execution/BUILD_v9.json` and commit. Send H2 (v9) with the PDF and a diff summary against v8.3.

### T-V9-POST — revision (after H2 "v9 PDF 확인")

1. Push as in T-PUSH, with the same fallbacks.
2. Revise the same note:
   - pdf = v9 anonymous
   - `leaderboard_submission_ids` = **bundle-3 id, then bundle-2 id**
   - abstract and TLDR from v9
3. Read the note back and confirm the ids and pdf sha256.

### T-POLL — deferred steps, each with executor and latest time

| trigger | executor | action | latest |
|---|---|---|---|
| H1 not done by 2026-10-31 12:00 KST | Codex | re-send the H1 message with the zips | 2026-10-31 12:30 KST |
| official ids arrive after T-POST | Codex | revise E4, the ids field and the PDF (same gates; H2 only if text beyond the E4 sentence changes) | 2026-11-06 20:00 KST |
| invitation tmdate changes | Codex, check every 6 h | diff, re-run the payload gate, revise if needed | 2026-11-06 20:00 KST |
| organizer reply pasted by Felix (Gmail `1a16136c8c73a587`, Discord) | Codex | revise within 30 min | 2026-11-06 20:00 KST |
| 2026-11-03 12:00 KST | Codex | confirm the note exists and the readback matches; if T-POST has not run, escalate to Felix the same hour | 2026-11-03 12:30 KST |

## Report (one message, at the end or while waiting at a gate)

```
T-PRE: tool route · hosts · RAM/disk · CB1 CB2 OR1 GS1 P1 match|MISMATCH old→new
T-ZIP: ZIPS.json · PREREG.md commit time
H0: quote+time · H1: ids+scores pasted+time · T-SCORE: SCORES.json, S1 match|MISMATCH, ABLATION.json (paired|unpaired)
T-CANON: diff lines · pages · Type3 · commit
T-BUILD83: anon/named sha256 · pages · MAIN_BODY · gate v3 JSON · H2 quote · AUTHOR_APPROVAL_v8.3.json
T-PUSH: ls-remote · fresh clone exit · private=0 · H3 status · identity hits (count)
T-POST: note id · tmdates · readback ids + pdf hash
T-V9 / T-V9-POST: gate v3 + v9 gate JSON · H2 quote · readback
Failures recorded and what continued past them
```
