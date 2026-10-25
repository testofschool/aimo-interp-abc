# HANDOFF_v8.3 — move canon to the M5, 5-page anonymized v8.3, push, OpenReview (one pass)

Written 2026-10-24 19:25 KST by Claude for Codex on Felix's **M5 Pro Max** (work folder `/Users/kangjungmin/Desktop/02_대회·해커톤/AIMO Interpretability Challenge/`). Supersedes HANDOFF_v8.2 §0–§5; T2 of v8.2 is DONE and stays as recorded. A pre-registered value that matches is settled; a mismatch stops only that track, report both values, continue the others.

## Why v8.2 stopped, and what changed since (all measured 19:05–19:25 KST)

1. **The canon lives on the other machine.** Commit `144ce58` (v8.1, gate v2.2, author approval) exists only in the Mac Studio clone (`/Users/felix/Desktop/AIMO Interpretability Challenge/`). It was never pushed: public HEAD is still `a429a9e`. The M5 clone is older (`542f44b`, named PDF `b0f1a5f…`, gate `27da04b…`). Do **not** rebuild v8.1 on `542f44b`.
2. **The form changed a 5th time** (invitation `tmdate` 1792834257455 = 2026-10-24 18:30:57 KST; raw sha256 `4109db75b1d6cb2809e9308f319b9fca00d4c7e31d8b37e6906d291b353f24a5`). Only the `pdf` field changed, and its new text is binding:
   > "The main body of the report should not exceed 5 pages and needs to be anonymized. In addition, you can use an unlimited number of pages for the AI usage statement, limitations, s, and appendix."
3. **v8.1 fails both new rules** (measured on the PDFs Claude holds):
   - Main body uses 7 pages: §1–§4 run to the top of page 7, and Limitations starts on page 7. The limit is 5.
   - The anonymous variant still contains 3 identity strings (the repository URL ×2 and a country mention). The named variant has 5 and a named Author field.
4. **D-013's "submit the named PDF" default is reversed:** submit the **anonymous** variant.

## 0. Pre-registered values

| id | what | expected | re-measure |
|---|---|---|---|
| R1 | bundle from Mac Studio | contains commit `144ce58`; that commit's named PDF sha256 `31c5ee0c79278c7b31a038acde4ed3f6ff61fbc2dbc361280000fc485b512c95`, anonymous sha256 `a290cac61a5dbf98c65f91e0f8f44ec350dc973b2ee81c568ce9ecf5199a1542` (the anonymous one was not regenerated after the AI-statement fix; report the actual value), `tools/prize_rubric_gate.py` sha256 `38a23f9febc62e45c492bc982db2180e26ee67611c9cfeff5f050861ed369031` | `git cat-file -t 144ce58`, sha256 |
| R2 | new gate | attached `prize_rubric_gate.py` **v3** sha256 `152e2a488eb0c3cdeadbe4195bb09ac90acab464df4326a612098dc63f5c7630`: 19 checks (v2.2's 17 + MAIN_BODY_5_PAGES + ANONYMIZED). Controls run in Claude's sandbox: synthetic 5-page body → MAIN_BODY ok (5); 6-page body → fail (6); v8.1 anonymous → FAIL 15/19 [ID_FIELD, OWN_SCORE, MAIN_BODY_5_PAGES (7), ANONYMIZED (3 hits)]; v8.1 named → FAIL 15/19 (5 hits, Author not anonymous) | sha256; run on the v8.1 PDFs from the bundle |
| R3 | tooling on the M5 | `pdftotext`, `pdfinfo` and `pdffonts` present (`brew install poppler` if missing — v8.2's gate run failed with "pdftotext missing") | `which pdftotext` |
| T2 | queue receipts (done) | always-robust `bde5e370-4dba-4f19-8291-4a998bfecdcd` 7/14 at 2026-10-24 19:01:28 KST, zip 519 B sha256 `4a3718e3…49e0a`; length-and-digit `0c736e59-8248-4dee-8e4f-2df037c552d7` 7/14 at 19:03:37 KST, zip 1387 B sha256 `30e59012…9cbbfd`. Both ≤ 11/14 = matches E1 | receipts in `v8-execution/queue/` |
| P1 | public HEAD | `a429a9e71b65e804481394f8b3a5f6799a9a6987` | `git ls-remote` |
| P4 | invitation | `tmdate` 1792834257455; duedate 2026-11-06 21:59 KST; fields unchanged except `pdf` (above). **Binding deadline 2026-11-06 20:59 KST** (Discord "Nov 5 11:59 PM AoE") | curl; if `tmdate` changes again, diff it and re-run the payload gate before T4 |

## 1. Gates

| gate | who | closes when | fallback |
|---|---|---|---|
| G-BUNDLE | Felix, on the Mac Studio | the bundle file and its sha256 are in this session (§2) | if the Mac Studio is unreachable until 2026-10-27 12:00 KST, say so — Claude writes a rebuild plan from the PDFs; do not improvise one |
| G-LOOK | Felix | types "v8.3 PDF 확인" after opening the rebuilt **anonymous** PDF | none |
| G-MIRROR | Felix, in a browser | the anonymized repository mirror exists at the URL in §3 E12 | if not made by T4 time, T4 waits; latest 2026-11-05 18:00 KST |

## 2. T0 — move the canon (Felix does steps 1–2 on the Mac Studio, Codex does step 3 on the M5)

1. Mac Studio Terminal:
   ```
   cd "/Users/felix/Desktop/AIMO Interpretability Challenge"
   git log -1 --format='%H %s'
   git bundle create ~/Desktop/aimo-canon.bundle --all
   shasum -a 256 ~/Desktop/aimo-canon.bundle
   ```
   Copy the two printed lines into this chat.
2. AirDrop `aimo-canon.bundle` to the M5 (it lands in `~/Downloads`).
3. Codex on the M5:
   ```
   git bundle verify ~/Downloads/aimo-canon.bundle
   git fetch ~/Downloads/aimo-canon.bundle '+refs/heads/*:refs/remotes/studio/*'
   git cat-file -t 144ce58          # expect: commit
   git switch -c v8.3 144ce58
   ```
   Check R1 and R3. Keep the M5's `542f44b` work as-is; do not merge it. Copy the T2 receipts and the private recovery key from the M5 folder into the `v8.3` working tree (`v8-execution/queue/`, `v8-execution/private/`; private stays git-ignored). Then install gate v3 (attached) as `tools/prize_rubric_gate.py` and commit it.

## 3. T1 — build v8.3 (anonymous is the submission)

E4, the measured baselines. Replace every "unmeasured" baseline sentence (end of abstract, §4.1, §5) with this text, filling values from the receipt JSON through `report_numbers.py`:
> Both reference baselines were scored once each through the organizers' temporary evaluation queue during the Codabench outage [announcements, 24 October]; these runs are not on the leaderboard. The always-robust rule and the length-and-digit control each scored 7/14 (submission ids bde5e370-4dba-4f19-8291-4a998bfecdcd and 0c736e59-8248-4dee-8e4f-2df037c552d7, 2026-10-24 19:01:28 and 19:03:37 KST), which is the fair-coin expectation and is not separable from it under the declared null.

E11, the five-page body. New order:
- §1 Task, §2 Leaderboard analysis, §3 Power and design target (this is the main body and must end on or before page 5);
- then **Limitations** (the old §5, unchanged);
- then **AI Use Statement**;
- then **References**;
- then **Appendix A**: the old §4 (label audit and problem-only controls), with its figures and tables;
- then **Appendix B**: the old §6 (reproduction).

Fix every cross-reference ("§4" becomes "Appendix A"). Text inside the moved sections stays word-for-word. If the main body still exceeds 5 pages, shorten only §2.3's prose. Never shorten numbers, tables or the declared assumptions.

E12, anonymization:
- In the anonymous variant, replace both repository URLs with `https://anonymous.4open.science/r/aimo-identifiability`.
- Delete "in Korea" from the snapshot sentence (keep the date and the timezone as "KST").
- Keep the PDF Author metadata "Anonymous Author(s)".
- The named variant keeps the GitHub URL; it is only for the public repo and the camera-ready.
- Move the abstract citation "[11]" to the end of the removal sentence.

Gates (all required):
- `report_numbers.py --check` exit 0
- `submission_text_gate.py` exit 0
- `python3 tools/prize_rubric_gate.py <anonymous v8.3 PDF>` in normal mode: **PASS 19/19**, exit 0
- Type3 0
- `pdftotext` diff of v8.1 → v8.3: only E4, E11 (moved blocks), E12 and the citation move may differ.

Write `v8-execution/BUILD_v8.3.json` (hashes of both variants, page counts, MAIN_BODY value, gate JSON). Commit, and send Felix the anonymous PDF plus the diff. Wait for G-LOOK.

**The author approval record must be updated.** `AUTHOR_APPROVAL_v8.1.json` covers the 4cf4e1ac/31c5ee0c named PDF. G-LOOK on the v8.3 **anonymous** PDF is recorded as `AUTHOR_APPROVAL_v8.3.json` with the same fields and that PDF's sha256.

## 4. T3 — push (after G-LOOK)

Push branch `v8.3` to `main` on the public remote within 10 minutes of G-LOOK, and no later than 2026-11-05 12:00 KST. Done means all three:
- `git ls-remote` HEAD equals the local v8.3 commit;
- a fresh clone passes `report_numbers.py --check` (exit 0);
- `git ls-files | grep -c private` in the fresh clone is 0.

Then tell Felix to create the mirror (G-MIRROR): at https://anonymous.4open.science, sign in with GitHub, choose repository `testofschool/aimo-interp-abc`, branch `main`, set the ID to `aimo-identifiability`, and add the terms to anonymize: `testofschool`, `Kang`, `Jung Min`, `felix`, `gangjeongmin`. Done means `curl -sI https://anonymous.4open.science/r/aimo-identifiability` returns 200 and the mirrored README contains none of those terms. Report the counts only, not the tokens.

## 5. T4 — OpenReview (after T3 and G-MIRROR)

1. Re-fetch the invitation (P4) and run `openreview_payload_gate.py`: exit 0.
2. Post with:
   - pdf = **v8.3 anonymous**
   - `leaderboard_submission_ids` = `[bde5e370-4dba-4f19-8291-4a998bfecdcd, 0c736e59-8248-4dee-8e4f-2df037c552d7]`
   - `submission_track` = `["Small models track"]`
   - reciprocal_reviewers `[~Jung_Min_Kang1]`
   - ai_assistance `[Ideation, Coding, Analysis, Writing]`
   - the three fixed sentences copied from the live JSON
   - licence CC BY-SA 4.0
   - white_box_award and voluntary_reviewers omitted
   - title, abstract, TLDR and keywords from v8.3. The abstract and TLDR contain no names or URLs.
3. Trial revision (TLDR plus one word), then revert, reading the note back each time.
4. Done means: the note id, three tmdates, and a readback showing the ids field equals the two UUIDs and the pdf matches the v8.3 anonymous sha256.

### 5a. Deferred steps (executor and latest time)

| trigger | executor | action | latest |
|---|---|---|---|
| organizer reply (Gmail thread `1a16136c8c73a587`) changes what the ids field should hold | Codex, within 30 min of Felix pasting it | revise the note | 2026-11-06 20:00 KST |
| official Codabench reachable (poll `https://www.codabench.org/` every 6 h, log the first 200) | Codex | resubmit both zips once to the official Small task; swap the ids in the PDF and the note (same gates, G-LOOK) | 2026-11-06 20:00 KST |
| invitation `tmdate` changes | Codex | diff it, re-run the payload gate and gate v3, revise if needed | 2026-11-06 20:00 KST |
| 2026-11-03 12:00 KST (existing scheduled check) | Codex | confirm the note exists and the readback matches; if T4 has not run, escalate to Felix the same hour | 2026-11-03 12:30 KST |

## 6. G-REVIEW (unchanged)

Three reviews by `~Jung_Min_Kang1` by 2026-11-12 23:59 AoE (= 11-13 20:59 KST). Felix writes them himself. Missing, late, low-effort or undisclosed-AI reviews mean desk reject.

## 7. Report back (one message)

```
T0: bundle sha256 + verify; 144ce58 present; R1/R3 match
T1: anonymous + named v8.3 sha256/pages/Type3; MAIN_BODY value; gate JSON (PASS 19/19); diff summary
G-LOOK: quoted message, time; AUTHOR_APPROVAL_v8.3.json written
T3: ls-remote HEAD; fresh clone exit; private paths 0
G-MIRROR: HTTP status; identity-term hits in mirror README (count)
T4: note id; tmdates; readback ids + pdf hash
Deferred: polls scheduled; 11-03 check
Blocked (not the same as not found): ...
```
