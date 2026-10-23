# HANDOFF_v8.1 (gate v2.2 2026-10-24 06:35 KST: hardened fallback; sha256 38a23f9f…9031) — AIMO-Interp report v8 + Codabench ×2 (via workaround) + OpenReview submission (one pass)

Revision 2026-10-24 05:50 KST: Discord #announcements read (G-DISCORD closed — transcript attached as `announcements.txt`, sha256 340ffe7d…a7a6b8); form changed a 4th time 10-24 04:55 KST; Codabench outage ≥48 h confirmed by organizers; edits E6–E10 added; `prize_rubric_gate.py` now 17 checks.

Written 2026-10-22 ~10:40 KST by Claude for Codex on Felix's Mac. Supersedes HANDOFF_v7.md. Start from local commit `2b48022` (v7, READY_FOR_AUTHOR_REVIEW). Read-only facts first; every pre-registered value below is checked by your first act in each track. A value that matches is settled; a mismatch stops only that track and is reported with both values.

## 0. Pre-registered values (measured 2026-10-22 10:19–10:25 KST, sandbox)

| id | what | expected | how you re-measure |
|---|---|---|---|
| P1 | public remote HEAD | `a429a9e71b65e804481394f8b3a5f6799a9a6987` (v6; v7 NOT pushed) | `git ls-remote <public remote> HEAD` |
| P2 | v7 named PDF | sha256 `433f19fc65d970c7be58289a7a9e01564fad4e7f31f13462db60f88f4cde909e`, 9 pages, Type3=0 | `sha256sum`, `pdfinfo`, `pdffonts` on the v7 build artifact |
| P3 | v7 anonymous PDF | sha256 `a86f03a92c77e0d97979d259c2f140c665f68f02aa3f6169cc303395b83a1b88`, 9 pages, Type3=0 | same |
| P4′ | invitation re-fetched 2026-10-24 05:36 KST | `tmdate` = `1792785352965` (2026-10-24 04:55:52 KST); duedate/expdate unchanged; NEW required `submission_track` (checkbox: Main track / Small models track); NEW optional `voluntary_reviewers`; `leaderboard_submission_ids` still required, text now "that we should evaluate for the prizes … only the first two"; reciprocal reviewer reviews **three** submissions, failure = desk reject + no awards. sha256 `fc1e071245f12c4c8da4f3f2f83135a012d8ccf7158f5c00413d0ca386be3c39` | same |
| P4 | OpenReview Submission invitation JSON (superseded by P4′) (`https://api2.openreview.net/invitations?id=NeurIPS.cc/2026/Workshop/AIMOInterp_Challenge/-/Submission`) | `tmdate` = `1792599149662` (2026-10-22 01:12:29 KST); `duedate` = `1793969940000` (2026-11-06 21:59 KST); `expdate` = `1793971740000` (22:29 KST); raw file sha256 `fdcfe127a68652302ad81e0e049c17acdfc7f3dee14238f5589a27b61a9fd4f6` (sha of the exact bytes curl returned at 10:20 KST — may differ on re-fetch if the server reorders keys; compare `tmdate`, not the hash) | `curl -sS <url> -o inv.json`; parse `invitations[0]` |
| P5 | required note fields (optional absent/false) | title, authors, reciprocal_reviewers, keywords, abstract, pdf, **leaderboard_submission_ids**, ai_assistance, ai_use_statement, reciprocal_reviewing_acknowledgement, rules_compliance, venue, venueid. Optional: TLDR, white_box_award. `note.id` optional (revision supported). | from inv.json |
| P6 | licence enum | exactly one: `CC BY-SA 4.0` (NOT CC BY 4.0) | from inv.json |
| P7′ | Codabench | **outage since 10-22**, organizers 10-24 04:34 KST: "we started working on a temporary workaround that will allow you to evaluate your submissions through a super simple interface" — watch Discord #announcements for it | Felix reads Discord; Codex polls `https://www.codabench.org/` every 30 min and logs the first 200 |
| P7 | Codabench phase | last known 2026-10-20: competition 16180, phase 30038 ends `2026-11-01T11:55:00Z`, Small task 36241, Main 36237, 10/day, 300/person. **Blocked from the sandbox on 10-22** (connection reset) → UNVERIFIED, re-measure from the Mac. | `GET https://www.codabench.org/api/competitions/16180/` with the token |
| P8 | organizer email sent | 2026-10-22 ~10:35 KST from gangjeongmin23@gmail.com to aimo.interp@gmail.com, Gmail id `1a16136c8c73a587`, asking page limit + binding deadline. No reply yet. | Felix's inbox; Codex does not touch it |

Fixed decisions (do not reopen): portal date binding (D-010) → now 11-06 21:59 KST; reciprocal reviewer `~Jung_Min_Kang1`; ai_assistance = Ideation, Coding, Analysis, Writing; named PDF is the submitted one; white_box_award unchecked; 0 Discord API calls; credentials typed locally by Felix only; no paid GPU; total spend cap unchanged.

## 1. Gates and when each dissolves

| gate | who closes it | dissolves when | fallback |
|---|---|---|---|
| G-DISCORD | **closed 10-24 05:35 KST** (transcript attached). Re-open only to catch the workaround announcement. | — | — |
| G-DISCORD(old) | Felix opens the AIMO announcements channel on screen; Codex transcribes to `v8-execution/discord/announcements_<date>.md` (verbatim, with message dates) | file exists | if the channel is not open by **2026-10-29 12:00 KST**, proceed with T2–T4 anyway and write `discord: NOT_READ` in the report — Felix chose "Discord first", but the Codabench phase end (P7, 11-01) makes waiting past 10-29 incompatible with his success definition (no submission = no prize). Record that override in the report. |
| G-AUTHOR | Felix types, in the Codex session, after opening the v8 PDF: "v8 검토했고 ~Jung_Min_Kang1 상호 심사 참여, GitHub push·Codabench 2건·OpenReview 제출(CC BY-SA 4.0) 승인" | that message exists | none — no document substitutes for it |
| G-PAGE | organizer reply on page limit (P8) | reply arrives | if no reply by G-AUTHOR time, submit v8 at 9 pages; a later reply with a smaller limit → revision before expdate (note.id optional, P5) |

Tracks are independent as an outcome: a hard-gate failure in one track stops only that track; every other track completes and reports with its own results, naming the failed track.

## 2. T1 — build v8 (text edits only; all numbers unchanged)

Edit `v6-execution/work/report/` sources (REGEN_SPEC_v8.md = this section). Every number still renders through `report_numbers.py`; no hand-typed decimals.

E1 §2.2 BH sentence — replace "the rule retains the largest rank r satisfying the threshold below and rejects the preceding ranks" with "the rule finds the largest rank r satisfying the threshold below and rejects ranks 1 through r". (Text contradicted the procedure; counts are unchanged: Small 2, Main 1.)

E2 §2.3 — delete the two sentences beginning "The snapshot records 1 perfect Small submission through the queue named aimo_organizer_rerun." and "We report this as an observed queue label …". Keep "The analysis assigns no causal interpretation or accusation to a score or a queue." only if a queue is still mentioned anywhere; otherwise delete it too.

E3 Abstract + §1 lead — replace the abstract's first sentence with: "On the AIMO-Interp public validation board (14 Small and 21 Main items, inferred from the score grid), no score below perfect is separable from a fair coin after per-owner selection: 59 of 61 Small owners, including a 12/14 result, and 40 of 41 Main owners are not rejected under the declared null." Replace §1's "The report concerns evaluation design and uncertainty; it does not propose a new robustness predictor." with: "The report turns this into an actionable rule for the organizers and for any later evaluation of robustness predictors: at least 76 independent problems (169 for a true accuracy of 0.60) scored with paired, problem-clustered comparisons, before any selection correction." Keep the sentence that the label-audit half overlaps prior work.

E4 §4.1 + §5 — after T2 returns receipts, replace "Their own private-validation results are UNMEASURED because we have no linked owner receipt …" with the measured sentence template: "Both bundles were scored on the private validation board: the always-robust rule scored {K_const}/14 (submission id {ID_const}, {ts_const} KST) and the length-and-digit control scored {K_ctrl}/14 (submission id {ID_ctrl}, {ts_ctrl} KST); neither is separable from the strongest non-perfect owner under the declared null." Register `K_const`, `K_ctrl`, `ID_*`, `ts_*` in the claims ledger from the receipt JSON, never typed. In §5 delete "The report has not measured our own frozen bundles on private validation" and keep "has no final-test outcomes". Add to §6 one sentence with the public repo URL and the v8 commit hash, and add the same URL to references [8] (reproduction archive).

E6 citation (required, Discord 10/23) — add to references and cite in §1 first paragraph: `@article{stefanik2026aimointerp, author={Michal Stef{\'{a}}nik and Philipp Mondorf and Andreas Waldis and Qianying Liu and Chuan Yang and Michal Spiegel and Josef Kuchar and Marek Kadlc{\'{\i}}k and Adam Vawda{-}Oomerjee and Chaoran Liu and Simon Frieder and Barbara Plank and Fazl Barez and Pontus Stenetorp}, title={{AIMO} Interpretability Challenge}, journal={CoRR}, volume={abs/2607.13899}, year={2026}, url={https://doi.org/10.48550/arXiv.2607.13899}, doi={10.48550/ARXIV.2607.13899}, eprinttype={arXiv}, eprint={2607.13899}}`. Also add a reference for the organizer announcements: "AIMO-Interp organizers. Announcements, Discord #announcements, 9–24 October 2026 (M. Štefánik, A. Waldis, M. Spiegel). Archived transcript in the evidence manifest."

E7 pre-removal framing (converged: KC1+KC2) — abstract sentence 2 and §2.3: "The snapshot predates the organizers' 21 October removal of two 100% submissions that they attribute to iterative profiling of problems and labels [announcements]. Under the declared null, only perfect observed scores separated from the fair-coin reference (Small 2 of 61 owners, Main 1 of 41); the board's only separable outcomes were therefore of the kind the organizers later identified as exploitation, rather than any moderate-accuracy method. We do not identify which owners were affected." Also §1: "The organizers have stated that the validation board does not cover final-evaluation problems [announcements, 21 Oct]. We address a different question: even inside its own distribution, the board cannot statistically identify a non-perfect method." Cite the 10/9 statement ("several highly ranking submissions rely on the balanced distribution of labels … a sort of overfitting") as the [official] source for the balance premise, replacing the second-hand attribution to [5].

E8 queue paragraph (converged: KC2 killing sentence + KC1) — replace the whole aimo_organizer_rerun paragraph in §2.3 with one sentence: "Rows from the queue aimo_organizer_rerun are organizer re-evaluations of top submissions under the 16 October per-problem protocol [announcements]; they are counted like any other row." Delete "make no inference about how that run was produced".

E9 baselines, not probes (KC1; Discord 10/21 "attempts to exploit labels in validation sets are against our rules") — everywhere the two bundles are described (§4.1, §5, §6): call them "reference baselines (a constant rule and a surface-feature control)"; delete every sentence that presents them as a way to check, verify or test label balance on the private board. They are submitted once each, never iterated.

E10 design target (converged: KC1 wounded + KC2 keep-lead) — the item-budget sentences in abstract/§1/§3: "Detecting a 0.65 (0.60) accuracy predictor against chance at 80% power needs at least 76 (169) independent problems with paired, problem-clustered scoring. We offer this as a design target for future validation boards, not as a statement about the unpublished final set." Keep the numbers; drop the word "actionable" from the report (it is the prize's word, not ours).

E5 hedging cut — in §2.3, §3.1, §4.2, §4.3, §5: keep at most one "does not establish / is not" sentence per paragraph; merge §5's three dependence paragraphs into one. Target: ≤ 40 negation tokens (not/no/never/cannot/neither/nor) in main text, counted by `grep -owiE 'not|no|never|cannot|neither|nor' main.txt | wc -l` on `pdftotext` output (v7 count ≈ 64). This is a style gate, not a content gate: do not remove a caveat that names an assumption.

Build both variants; gates: `submission_text_gate.py` exit 0, `report_numbers.py --check` exit 0, Type3 = 0, pages ≤ 9, and **`python3 tools/prize_rubric_gate.py <named v8 PDF>` exit 0** (17 checks; pre-registered: v7 exits 1 with 12 failures (5/17 pass, negations 67); v8 must exit 0 (17/17)). Commit `prize_rubric_gate.py` (attached) as `tools/prize_rubric_gate.py` first; its exit 1 blocks T3 and T4.  Write `v8-execution/BUILD.json` with sha256, pages, Type3, negation count for both PDFs. Send both PDFs to Felix for G-AUTHOR. Commit locally (do not push yet).

## 3. T2 — Codabench ×2 (approved by Felix 10-22; blocked by the outage; run through the organizers' workaround the moment it ships, or Codabench if it returns first)

If neither exists by **2026-11-03 12:00 KST**: (i) add to §4.1 and the abstract's last sentence that Codabench was unreachable from 22 October (cite the organizers' 24 October announcement) so the baselines' private-validation results remain unmeasured; (ii) run `python3 tools/prize_rubric_gate.py <named PDF> --fallback-none --ids none` on the real clock — it refuses before 11-03 12:00 KST, without the outage sentence, without a citation of the organizers' 24 October Discord announcement, with any ids other than `none`, and whenever a live HEAD probe of codabench.org answers (then submit the baselines instead); required result `PASS_FALLBACK`, exit 0. `--now`/`--probe-result` are test-only and always exit 3; (iii) enter the literal value `none` in `leaderboard_submission_ids` (regex `^\S+$` accepts it; issue #10, organizer michalspiegel: "No, you do not need to submit a Codabench submission to be eligible for the writeup prize."), keep §4.1 with the baselines described as planned-not-run, and Felix sends the held email (§7) the same day. Record this override in the report.

1. Re-measure P7 from the Mac (token via `api-token-auth/`, Felix types credentials). Record phase end, tasks, limits in `v8-execution/codabench/phase.json`. Mismatch with P7 → report, continue.
2. Confirm participant status APPROVED (`/api/competitions/16180/` participant field or the "You do not have access" error on a dry call). Not approved → stop T2 only, report; T1 still builds with E4 left as the v7 sentence plus "receipts pending".
3. Submit the two frozen Small bundles (always-robust, length-and-digit control) to phase 30038, task 36241, one at a time, ≥ 2 min apart, 2 of today's 10. Save each response JSON (submission id, status, created time) to `v8-execution/codabench/receipt_<bundle>.json`; poll status until scored or failed (exec limit 4200 s). Expected: both score ≤ 11/14 (not separable) — a value above 11/14 is a mismatch to report, not a reason to resubmit.
4. Return the two `id` values; these go into E4 and into `leaderboard_submission_ids`.

## 4. T3 — push (after G-AUTHOR and `prize_rubric_gate.py` exit 0 on the v8 PDF)

Push the v8 commit to the public remote. Done = `git ls-remote <remote> HEAD` equals the local v8 commit AND a fresh clone into a new directory builds `report_numbers.py --check` exit 0. Record both in the report. Push within 10 min of G-AUTHOR, no later than 2026-11-05 12:00 KST.

## 5. T4 — OpenReview submission + trial revision (after T3)

openreview-py 2.9.0, `OpenReviewClient(baseurl='https://api2.openreview.net', username, password, mfa_code_provider)` with Felix typing. `put_attachment(named v8 PDF)`, then `post_note_edit` with content: title (v8 title), authors `[~Jung_Min_Kang1]`, reciprocal_reviewers `[~Jung_Min_Kang1]`, keywords (from v8), abstract (v8 abstract ≤ 5000), TLDR (≤ 250), pdf, `leaderboard_submission_ids` = the two T2 ids, `submission_track` = `[Small models track]`, ai_assistance `[Ideation, Coding, Analysis, Writing]`, ai_use_statement / reciprocal_reviewing_acknowledgement / rules_compliance = the single enum sentence each (copy from inv.json, never retype), licence `CC BY-SA 4.0`, white_box_award omitted. Run `tools/openreview_payload_gate.py` against the live inv.json first; gate exit 0 required.
Then the trial revision: re-post the same note with `note.id` set and the TLDR changed by one word; done = the note's `tmdate` advances and content reads back; then revert the TLDR. Record note id, both tmdates.
Deadline: duedate 2026-11-06 21:59 KST; submit no later than 2026-11-05 18:00 KST.

## 6a. G-REVIEW — reciprocal reviewing obligation (not optional)
The nominated reviewer `~Jung_Min_Kang1` will be assigned three submissions; review deadline **Thursday 2026-11-12 23:59 AoE (= 11-13 20:59 KST)**; a missed, late, low-effort or undisclosed-AI review = desk reject + no awards (invitation 10-24 + Discord 10/23). Codex: when the assignments appear, create `v8-execution/reviews/` with one file per paper and a calendar line for Felix; Felix writes the reviews himself.

## 7. Held email (send only if T2 fallback fires or on 2026-11-01, whichever first) — reply in Gmail thread 1a16136c8c73a587
> Following up on my 10-22 note: if the Codabench workaround cannot give me evaluation IDs before Nov 5, what should a writeup-prize-only report enter in the required `leaderboard_submission_ids` field? Is a report whose numbers come from local runs on the public train set acceptable in that case? The page-limit question from my earlier message still stands.

## 6. Report back (one message)

```
P1..P7 re-measure: <match|MISMATCH old→new>
G-DISCORD: <file|NOT_READ (override recorded)> · G-AUTHOR: <quoted sentence, time> · G-PAGE: <reply|none>
T1 v8: named sha256/pages/Type3/negations, anonymous same; gates exit codes incl. prize_rubric_gate (expected v7 exit 1 → v8 exit 0, 12/12); local commit
T2: phase.json end=<ts>; receipts: const id/score/ts, ctrl id/score/ts
T3: ls-remote HEAD=<hash>; fresh clone check=<exit>
T4: note id, submit tmdate, revision tmdate, reverted=<y/n>
Blocked (not the same as not found): <list>
```
