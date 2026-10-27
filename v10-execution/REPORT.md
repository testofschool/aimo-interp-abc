# v10 local execution — H1 / H2 handoff

The user directly adopted v10 and answered H0 **“v9 진행”**. This record is local preparation, with no new competition upload, GitHub push, OpenReview note or external message. The actual executor is the Mac Studio, not the M5 named in the attachment.

## T-PRE

- Native git, Python, zip, curl, gh and Poppler are available. Mac Studio has 64 GiB RAM; the recorded free disk was about 10.7 GiB.
- CB1, CB2, OR1/OR2, GS1 and P1 matched the supplied values. Competition 16180 Small task 36241 closes **2026-11-01 20:55 KST**. H1 completion target is **20:00 KST** that day. Public reachability does not establish account approval or unused quota.
- OpenReview tmdate **1793023952361**, anonymous body ≤5 pages, one report per first author, same Codabench user, only the first two listed IDs evaluated. Optional supplementary ZIP is 50 MB. Earlier binding report deadline remains **2026-11-06 20:59 KST**; this workflow stops external edits at **20:00 KST**.
- OpenReview SDK **2.9.1** imports in an isolated environment. No client, login, credential lookup or attachment upload has run. H4 must use private local password/MFA input; SDK defaults can read environment credentials and echo an OTP.
- Full observations: [public preflight](../v9-execution/preflight/PUBLIC_PREFLIGHT.json), [machine/tools](../v9-execution/preflight/TOOLS_MACHINE.json), [SDK preparation](SDK_SETUP.json).

## T-ZIP and preregistration

PREREG is committed at **773b39e1a2ca0f1c4001e0ae1459e7d567e56c80**, **2026-10-27 01:03:42 KST**, before any official upload/result in this run. This is a local commit, not a public preregistration service. Existing official submissions must be checked first; prior outcome exposure changes the analysis label to exploratory.

| Upload order | Locally readable file | Bytes | SHA-256 |
|---|---|---:|---|
| 1 | `v9-execution/upload-order/solution-always-true-small.zip` | 519 | `4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a` |
| 2 | `v9-execution/upload-order/solution-text-length-control-small.zip` | 1,387 | `30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd` |
| 3 | `v9-execution/bundle3-trained-probe-small.zip` | 27,662,500 | `852fff17372ebdcf967549a4270339a2e792372c1b5496da968b2df884ccc67b` |

Files 1–2 are exact Git 144ce58 blob copies, without recompression. Placeholder originals were preserved. File 3 contains unmodified organizers’ code/artifact at de794053, with the required empty root `small.txt`. CRC and member bytes match; no pickle or model was executed. The organizer clone and third-party binary remain local, ignored by Git.

H1: Felix signs into **testofschool**, opens official competition 16180 → Small Model Track, checks existing official receipts first, uploads each unsubmitted file once in order and at least two minutes apart, then provides ID/status/score/completion time. Never submit these again to the temporary queue. If authorized prediction output is available, retain its native receipt and item IDs for the paired analysis.

## Analysis clarification fixed before outcomes

The two queue results (7/14 each) are known prior information and disclosed in [PREREG.md](../v9-execution/PREREG.md). Official scores remain **UNMEASURED**.

The primary comparison is official trained probe 3 versus text control 2, exact matched McNemar at α=.05. If only aggregate same-board totals are available, feasible paired-table p-value bounds replace the handoff’s undefined independent-binomial fallback. With verified binary prediction coverage and exact counts, prediction disagreements can identify discordant correctness counts without accessing private labels. When a joint distribution is not identified, paired N80 remains UNMEASURED. No non-significant result establishes equivalence or black-box sufficiency; these distinct systems are a comparative control, not a causal white-box signal ablation. The planned 240-instance final set is distinct from the current validation board and does not itself refute v8.3’s conditional claims.

Independent mathematical review found no blocker; synthetic tests **18/18 PASS**. See [review record](../v9-execution/PREREG_REVIEW.json). Actual results will enter the report only through the numeric pipeline after receipts arrive.

## T-CANON and T-BUILD83

- Reused exact approved Studio v8.1 blob: PDF SHA **31c5ee0c…512c95**, layout-text SHA **b740a790…31dc0a**, 9 pages, Type3 0. Reference residual diff is zero because this is the same approved blob; no M5 rebuild is claimed.
- Reused completed v8.3 source/PDF from 33328fe. Anonymous SHA **2edf06ab6764af045e470acdc77f115700d9cf85303a11d174c80e273c182e51**; named SHA **c8be7a4f3c4fac8da00d1c7c05f6edef9e17f2e974e97b8a190c371eb9927cc0**. Anonymous main body 5 pages / total 10 / Type3 0.
- Exact immutable v3 **152e2a48…** rerun on anonymous bytes: **PASS 19/19**, normal mode. Source-only, fidelity and visual evidence from the unchanged original T1 are retained in `results/v8.3/`. The 32086990 gate was not executed.
- OpenReview payload gate **PASS**. Strict preflight **technical PASS / READY_FOR_AUTHOR_REVIEW**, exit 1 because new H2 has not been given. No author-confirmed flag was supplied.
- Historical numeric evidence is **164/164 PASS**. Initial independent recheck was UNRUN after bounded runtime/Git extraction timeouts, preserved in [NUMERIC_RECHECK.json](NUMERIC_RECHECK.json). Recovery then verified 17 source inputs, reused hash-verified historical snapshots and fresh pinned parquet 4/4, and ran unchanged report_numbers.py --check once: **164/164 PASS, exit 0, 21.14 s, mismatches 0**. See [NUMERIC_RECOVERY.json](NUMERIC_RECOVERY.json).
- PDF still uses the explicit temporary-queue fallback with UUIDs; their organizer acceptance as official form IDs is unverified. It does not claim official runs. Actual official receipts will replace E4 and the payload IDs.
- Byte-identical readable review copy: `v10-execution/review/aimo-interp-report-v8.3-anonymous.pdf`. H2 requires the direct statement **“v8.3 PDF 확인”** after review. No new approval receipt has been written.

## Gate controls and remaining work

The immutable v9 gate **a8a0cede…c0c4** is installed as `tools/v9_lead_gate.py`. Its literal handoff positive fixture failed WHITEBOX_RUN because the supplied fixture omitted “probe”. Adding that word to the synthetic positive fixture yielded **PASS 7/7**; removing ablation/240 yielded the expected FAIL. This fixture correction does not change the gate or establish any actual v9 measurement. [Control evidence](checks/V9_GATE_CONTROLS.json).

T-SCORE, actual v9 PDF, T-PUSH and T-POST are pending. After H2, publication follows v10; one existing note must be located through ledger plus authenticated author queries before any creation. All later revisions use its same note.id. [H4 checklist](openreview/H4_READY.md) covers single-attempt creation, uncertain-result reconciliation, TLDR trial/revert and readback of IDs/PDF hash. H3 mirror remains preferred, not established merely by a URL in the PDF.

The six-hour monitor and Nov 3 note check were updated to v10. An Oct 31 noon H1 reminder was added. No email or Discord message was sent. **H1 official IDs/scores and H2 PDF review are the current human actions.**

## Direct amendments v10.1 / v10.2

H1 is now assigned to Codex: logged-in browser A, authenticated same-origin API B, local getpass/session C, manual D only if those fail. Actual Chrome inventory includes Felix’s Codabench tab, but repeated claim/read calls timed out. The separate Playwright browser is unauthenticated (Login displayed). A/B have not produced authenticated submission history, and no upload was attempted. A local route-C helper is being prepared; passwords/cookies/CSRF/signed URLs must never be written to logs.

H2 prechecks are [H2_CHECKS.json](../v8-execution/H2_CHECKS.json) and [H2_REVIEW.md](H2_REVIEW.md). The handoff is not a typed PDF approval. Literal a/e exceptions and f disclosures are explicit: the same source/PDF were captured together after building; old numbered §5 is the E11 unnumbered Limitations. No timestamp manipulation, pointless paper renumbering or gate edit was used to hide these conditions.


Route C is now implemented and independently reviewed (helper SHA9144dc2f…20aa4da), local ZIP/prereg checks PASS and synthetic safety10/10 PASS. The interactive process86398 successfully read the public login form and reached the local getpass prompt; no password had been read at that observation. The app terminal-open request returned QUEUED and visibility was not established. H1-auth is pending local input; do not launch a second helper while this process holds the single-uploader lock. See codabench/ROUTES.json, CLI_README.md and CLI_INDEPENDENT_REVIEW.json. No official ID or score is yet available, so no SCORES.json is manufactured.

## v10.3 local audit

Directly adopted with supplemental checks. Exact originalA0 executes with pypdf and returns FAIL/exit1 solelyFORBIDDEN_0 for one truthful final-testUNMEASURED statement; A1 is MISMATCH and the original result is retained. Wrong-PDF/missing-file controls return1/2. Immutablev3 fresh normal runPASS19/19. Separate supplemental actual artifact checksPASS19/19, negativecontrols13/13, and the same checker re-executed on bundle bytesPASS19/19. No PDF/source/gate edit or rebuild. The158 receipt remainsUNVERIFIABLE; the164 raw data/claims run is verified and the PDF association is through build receipts. UpdatedH2_CHECKS and the one-minuteH2_REVIEW correcta/e while preserving prior evidence and allfourdisclosedchanges. H2/H1-auth remainpending; DesktopZIP packaging/integrity receipt follows.
