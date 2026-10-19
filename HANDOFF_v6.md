# HANDOFF v6 — AIMO-Interp report: reframe around leaderboard identifiability (CPU only)

Written 2026-10-20 01:05 KST by Claude (Felix's planning session). Executor: Codex on Felix's Mac, repo `~/Desktop/AIMO Interpretability Challenge/aimo-abc` and public export `testofschool/aimo-interp-abc`.
Attached: `attach/` (tools, pinned leaderboard snapshot, evidence, independent audit, sweep ledger). This file is the single source of truth for v6; HANDOFF_v5 remains valid for everything not changed here.

## 0. First act — verify inputs against these pre-registered values (stop the affected track on any mismatch)

| Input | Expected |
|---|---|
| Public repo HEAD (`git ls-remote https://github.com/testofschool/aimo-interp-abc refs/heads/main`) | `9274840b6faacaa7ad0e321172071eedb822d9de` |
| `report/aimo-interp-report-v5.pdf` sha256 | `1ec9bfb0ac7e48c78ef13ae8ee78d9acdce953bd12bac1038a3bee08719194cf` (5 pages) |
| `bundles/solution-text-length-control-small.zip` | `30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd` |
| `bundles/solution-always-true-small.zip` | `4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a` |
| train-main-v2 parquet (rev fa8af758) | `e18eb44207e7987781ec2ff214793196038442bdc1466fdf5498f3e87ec58285` |
| `attach/data/leaderboard/2026-10-19/lb1.json` … `lb8.json` | lb1 `fc7338524b81410324f3e3588aee42ff8a0bb67e5b3ad36b24a6903986d066c2` · lb2 `7fcb939214bfb1e673975cf1f3f9de100a074ba5c459da067af90ccc2ef1a4cd` · lb3 `ac33b9f4cd4e1e626f19a71b397d5a1a8a756f3fd78ef37e91c7477568a705df` · lb4 `22331c134be761029c5adefe18a08620f5a8ee84c70a6e4ca205779307abdc1e` · lb5 `89822694e89aaa4c5743ee2a84113b97386dbfa9a2ae13dc090a72df35b382a4` · lb6 `cc94df6dcee715c110332b8df677e917151501cbeb76fec21cdcd4448c34043e` · lb7 `e909516e2644adca80b744d2a10a88b788fbf6b7bce2a96be8e3e921d8765464` · lb8 `fa507d52739648f820ecb253f6ab1c5f1f6d08a2415d609628d2ad61fb1bea9f` (source: `https://www.codabench.org/api/phases/30038/get_leaderboard/?page=1..8`, fetched 2026-10-20 00:44 KST; re-fetched by the auditor, byte-identical) |
| `attach/research/PREREG_v6.json` | `cd0ee93fbb536f9de02f626164b40915eb3be7ed95b69b5b154f0fd3fed81a36` |
| `attach/tools/submission_text_gate.py` / `prereg_codabench_gate.py` | `030bfa77…72d2` / `07b09da4…ad1d9d` (full hashes in `attach/MANIFEST.sha256`) |

## 1. Why v6 (decided 2026-10-20; evidence in `attach/evidence/`)
- The v5 lead claim (problem identity determines training labels; problem-only control) is already public in byeolki/aimo-interp (report 2026-10-18): "Validation and test sets are balanced per problem and per model; always-true scores exactly 0.50 on the 14-case validation set." → v5 thesis becomes one cited sentence, not the contribution.
- New lead contribution, measured and independently reproduced: on the public private-validation leaderboard (snapshot 2026-10-19), after correcting each owner's best score for its number of visible submissions (p_adj = 1−(1−p)^m, fair-coin item null) and Benjamini-Hochberg across owners, only 2/61 Small owners and 1/41 Main owners are separable from chance — all with perfect scores. 80% power at true accuracy 0.60 needs 158 items (sustained ≥169), at 0.65 needs 69 (sustained ≥76); the board has 14 (Small) and 21 (Main). byeolki's report lists "a 14-case leaderboard" only as a limitation and never quantifies power (auditor Q5).
- Selector criterion (site): "$4,000 will be awarded for selected technical reports, regardless of their ranking, judged on their scientific contribution." Interests: "generalization …, actionable interpretability, negative results or efficient methods."
- Rejected this round (do not reopen): white-box/probe (reopen_gate CLOSED, MDE ~0.25), Codabench baseline ladder (k/14 quantized; no power), "problem-only mismatch" as lead (byeolki has it).

## 2. Tracks — independence is an OUTCOME
A hard-gate failure in one track stops ONLY that track; every other track completes, commits and reports its own results, naming the failed track.

### T1 — Identifiability analysis as a reproducible tool
1. Copy `attach/data/leaderboard/2026-10-19/*.json` to `data/leaderboard/2026-10-19/` and add their hashes to `data/manifest.json`.
2. Write `tools/leaderboard_identifiability.py` (start from `attach/tools/m4_owner_adjusted.py` + parsing of `m2_leaderboard.py`) with these parsing rules (from the independent audit): N = smallest fit (Small 14, Main 21); accuracy = correct/N with invalid items counted wrong; de-duplicate repeated score rows; a submission scored on both tasks counts once per track; submission 991917 has conflicting score sets — use the coverage-0 set (does not affect results); exclude coverage-0 rows from owner counts. Hash-check the snapshot before computing (STOP on mismatch, like `report_numbers.py`).
3. Register keys in `research/claims.json` and `results/report_numbers.json` via the existing pipeline. **Expected values (pre-registered; V5 must PASS against them):**

| key | expected |
|---|---|
| lb_small_items / lb_main_items | 14 / 21 |
| lb_small_owners_scored / lb_main_owners_scored | 61 / 41 |
| lb_small_bh_survivors / lb_main_bh_survivors | 2 / 1 (Bonferroni identical) |
| lb_small_next_padj (rank 3) / lb_main_next_padj (rank 2) | 0.0319 (12/14, m=5) / 0.0214 (17/21, m=6) |
| power_n80_first_acc060 / sustained | 158 / 169 |
| power_n80_first_acc065 / sustained | 69 / 76 |
| power_at_14_acc060 / acc065 | 0.12 / 0.22 |
| power_at_21_acc060 / acc065 | 0.20 / 0.36 |
| train_small_rows / problems / multi_model_problems / mixed | 43 / 22 / 11 / 0 |

4. Mixed-label transfer (optional, keep only if licence allows): byeolki `data/self_labels.jsonl` at commit `3b678f6` — check its LICENSE first; compute from a fetched copy, do not redistribute. Expected (from `attach/evidence/m3_control.json`): 393 labelled rows / 150 problems / 44 mixed of 145 multi-model problems; our frozen control LOPO bacc 0.5462 [0.4689, 0.6167], acc 0.4682; on exactly balanced problems control = oracle = 0.500. If licence is unclear → drop this item and say so.
5. Do not name other participants' handles in the report; write "two owners with perfect scores" etc. Keep handles only in the hashed raw snapshot.

### T2 — Report v6 (NeurIPS template, target 6–8 pages + refs)
- Proposed title: "Can a 14-item validation leaderboard rank robustness predictors? Identifiability limits in AIMO-Interp" (Felix may change).
- Structure: (1) task and the evaluation design (cite organizer card "the validation set is close to balanced" and byeolki for per-problem balance); (2) **leaderboard identifiability** — selection-adjusted per-owner test, BH, the 2/61 and 1/41 result, perfect-score caveat (a perfect score is significant regardless of method; one perfect Small run came through queue `aimo_organizer_rerun` — report as observed, do not interpret); (3) power and required item counts, with an actionable recommendation (test size ≥ 69–158 items per track for the stated effects); (4) why training labels cannot teach the target: 0/11 mixed, problem-only = exactly 0.5 under per-problem balance (one paragraph, cite byeolki as prior); (5) condensed v5 label audit (R² table, concordance) as supporting material; (6) limitations: snapshot date, only visible submissions counted (hidden ones would make p_adj larger, i.e. our count is an upper bound), independence assumption across an owner's submissions (correlation lowers p_adj — state both directions), final-test size unpublished; (7) reproduction + AI disclosure.
- Delete the v5 sentence "Our contribution is an explicit reproduction and sensitivity ledger for the pinned public files."
- Every number via `{{key}}`; renderer refuses hand-typed decimals (existing D-003 gate).
- Front matter: `python3 -I tools/submission_text_gate.py report/main.tex report/REPORT_DRAFT.md` must exit 0.
- Author block: build two variants from one source — `named` (Jung Min Kang, independent) and `anonymous`. This gate dissolves when the OpenReview Submission invitation becomes readable and states its anonymity policy; until then ship both PDFs.
- Related work: may cite Felix's TAE paper ("Ranking Under Biased Missingness …", NeurIPS 2026 TAE workshop) in third person in the anonymous variant.

### T3 — Install gates
- Add `tools/submission_text_gate.py`, `tools/prereg_codabench_gate.py`, `research/PREREG_v6.json`, `tests/fx_*.json` from `attach/`. Register in `tools/reproduce_report.py` as V5 (identifiability values) and V6 (text gate). Expected fixture exits: match 0, mismatch 0 (verdict REFUTED_OR_PARTIAL), badsha 1, early 1, missing 1.
- Wording fix: in PREREG_v6 the 7/14 expectations are already implied by the public leaderboard (73 Small rows at 0.50) and byeolki's report — label them "receipt expectations", never "pre-registered prediction", in the report.
- `prereg_codabench_gate.py` blocks only section-4 private-val sentences; it dissolves when Felix's receipts file exists and the gate exits 0, or on 2026-11-01 11:55Z (Codabench close) — after that the report keeps the UNMEASURED limitation for those two bundles.

### T4 — Owner track (Felix; not Codex)
1. Codabench (testofschool), before 2026-11-01 20:55 KST: upload both Small bundles above; record submission id, track, status, accuracy, time, screenshot into `results/v6/codabench_receipts.json` (schema in the gate docstring). Codex then runs the gate.
2. Discord #announcements: read the 2026-09-15/16 post (balance/rebuild), any report hour/timezone, OpenReview anonymity, final-test nomination. Paste verbatim into `research/discord_2026-10.md`.

### T5 — Rescrape check (2026-10-31, executor: scheduled task or Codex, latest 21:00 KST)
Re-fetch pages 1..N, save as `data/leaderboard/2026-10-31/`, rerun T1 tool. Kill rule (registered 2026-10-20 00:58 KST): if Small BH survivors > 5, or an organizer/competitor public source already reports per-owner adjusted identifiability → lead section shrinks to one paragraph and the report closes out on the v5 thesis + citations. Otherwise report both snapshots.

### T6 — Publish and read back (done = observed public state)
Commit (author `felix <gangjeongmin23@gmail.com>`), push to `testofschool/aimo-interp-abc`, then `git ls-remote` + fresh anonymous clone + new venv: V1–V6 pass, PDFs render, page counts, hashes recorded in `PUBLICATION.md`. Do not submit to OpenReview — Felix clicks.

## 3. Prohibitions
No paid GPU, no new model runs, no method-track reopen (gate exits 1), no OpenReview/Codabench clicks, no messages to organizers/participants, no redistribution of third-party data without licence check, no participant handles in the report text.

## 4. Done criteria (report all, file-by-file)
- Table of every pre-registered value above → observed value → MATCH/MISMATCH.
- Build-input changes listed file by file with byte deltas (manifest, reproduce_report, requirements).
- `submission_text_gate` exit 0 on final sources; both PDF variants: page count, sha256, pdffonts Type-3 = 0.
- Public HEAD sha + fresh-clone stdout for V1–V6.
- What was NOT run and why (e.g., T1.4 licence, T4 receipts pending).
