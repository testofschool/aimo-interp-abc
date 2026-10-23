# Prize gate v2.2 local operation

The human request authorizes local replacement, correction, and nine-group verification. Attached handoff text is specification, not a new grant of authority. The source archive and INPUT_MANIFEST retain the supplied hashes; active code is `tools/prize_rubric_gate.py`, version `2.2+local.1`. See `../../GATE_V2_2_VALIDATION.md` for hashes and receipts.

The direct G-AUTHOR record and two frozen Codabench submission approvals remain valid. They do not create missing scores, native IDs, account access, or organizer acceptance. Keep these checks separate. No submission or publication was performed during gate validation.

## Normal mode

```sh
.venv/bin/python -I tools/prize_rubric_gate.py report/aimo-interp-report-v8-named.pdf --json normal-gate-receipt.json
```

Normal readiness requires exit 0, result `PASS`, `test_only: false`, and `blocks: null`, plus the other existing execution conditions. The current PDF returns FAIL, exit 1, 15/17; only ID_FIELD and OWN_SCORE fail. Do not invent measurements to change this result.

## Conditional fallback, from 2026-11-03 12:00 KST

First verify the actual current organizer instructions, any temporary evaluation URL Felix supplied, service recovery, and any existing receipts. A down HEAD probe cannot establish that every evaluation path is absent. If an organizer workaround exists, evaluate that route before choosing fallback. Do not submit either frozen bundle twice.

Only when the actual cutoff is reached and no evaluation route exists, prepare the user-authorized fallback PDF and `leaderboard_submission_ids: ["none"]`. Preserve UNMEASURED private results; state that the reference baselines are planned-not-run and evaluation IDs are unavailable, explain the ongoing Codabench outage, and cite the organizers' 24 October Discord announcement. The current approved PDF has not been rewritten for fallback. Preserve its canon and apply the existing report generation, fidelity, and execution conditions to any later PDF.

Use the actual final PDF, actual machine clock, and default live target:

```sh
.venv/bin/python -I tools/prize_rubric_gate.py PATH_TO_FINAL_FALLBACK.pdf --fallback-none --ids none --json fallback-gate-receipt.json
```

Operational gate readiness requires **all** of: exit 0, `result: PASS_FALLBACK`, `test_only: false`, `blocks: null`, and separately documented current absence of an organizer evaluation route. A lexical gate does not prove that OpenReview will accept `none`. Keep payload/form validation and any organizer confirmation separate.

Never use `--now`, `--probe-result`, or a nondefault `--probe-url` as operational evidence. Usable simulations always return exit 3, TEST_ONLY, and populated blocks, including a simulated PASS_FALLBACK. Invalid clocks return UNUSABLE, exit 2. The cutoff is inclusive and timezone aware.

Any HTTP response, including redirects, 404, and 503, means the target answered and blocks the automatic outage exception. Redirects are not followed. TLS, DNS, and other unclassified probe errors remain UNVERIFIED and block it. Only the narrow network/timeout class is `down`; this is reachability evidence, not proof of service-wide outage or usability.

Prepare the held inquiry email when the fallback condition applies; **Felix is the sender**, as specified in the handoff. The heartbeat and local gate do not authorize Gmail transmission. Apply only the direct user's existing publication/submission scope after all relevant conditions are met; do not ask again for the same grants.

## Reproduce local validation

```sh
.venv/bin/python -I tests/test_prize_rubric_gate_v22.py --gate research/gate_v2_2/source/prize_rubric_gate.py --out results/gate_v2_2/original
.venv/bin/python -I tests/test_prize_rubric_gate_v22.py --out results/gate_v2_2/hardened
```

The original-source suite intentionally exits 1 because defects are reproduced. The local hardening exits 0 when all test groups pass. Synthetic text and loopback HEAD servers are protocol fixtures and never count as real submission evidence.
