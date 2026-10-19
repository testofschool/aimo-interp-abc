# Completion-corrected v6 publication — refresh pending

Current local corrections have passed complete CPU and PDF checks. They have not yet been asserted as publicly reproduced. The previous public release and readback below are historical evidence for their own bytes.

## Historical initial v6 public readback — 2026-10-20 KST

Observed public scientific release HEAD: `e2fa9b64d1466be4b8b4069b20f7678d69aaabfb` ([commit](https://github.com/testofschool/aimo-interp-abc/commit/e2fa9b64d1466be4b8b4069b20f7678d69aaabfb)). Commit author is `felix <gangjeongmin23@gmail.com>`. The remote was checked against the exact pinned v5 HEAD before the v6 push.

## Public reproduction

A new unauthenticated clone was made with credential helpers, extra HTTP headers, global/system Git configuration and interactive authentication disabled. Its HEAD matched `git ls-remote`. A new Python 3.13 environment installed unchanged dependency pins. All four organizer parquet files were absent before a real network fetch; all four newly downloaded hashes matched. No local parquet copy was substituted for that check.

The new clone passed the following checks. Raw stdout/stderr and exact invocations are preserved in `results/v6/publication/`; `public-cpu-gates.json` contains individual gate output.

| Check | Result |
|---|---|
| V1_original | PASS |
| V2_original | PASS |
| V1_final | PASS |
| V3 | PASS |
| V2_final | PASS |
| V4 | PASS (expected exit 1 / CLOSED) |
| V5 | PASS |
| V6_source_regeneration | PASS |
| V6 | PASS |
| owner_receipt_scope | PASS |

The fixture unit suite and leaderboard regression suite also passed. Missing owner receipts produce UNMEASURED in a separate owner-evidence scope check; they do not turn into a private score or a failed public-label analysis. These are CPU/macOS checks, not GPU-container parity or external service evaluation.

## Final PDF artifacts

| Variant | Body + references | SHA256 | Type-3 fonts |
|---|---:|---|---:|
| named | 8 + 1 | `0cd3fdf4dd40b39a80b5244fc7d8131f2956c278d1944c6951eebe2e0290600f` | 0 |
| anonymous | 8 + 1 | `64007f693861ccf0151e42e0805fccc65a638036ec26b76a7a440a7f5c13c112` | 0 |

Both shipped PDFs in the public clone matched the locally reviewed final bytes. `pdftoppm` rendered all nine pages of each directly from the public clone; page counts, fonts and hashes are recorded in `receipt.json`. All eighteen final pages had already been visually reviewed, and source regeneration in V6 produced byte-identical named/anonymous TeX and provenance. The report/fidelity pair remains the next regeneration canon.

## Receipt-only follow-up and final HEAD

This record and the public readback receipts are published in a follow-up commit. That commit changes documentation and receipts only. It must not change any manuscript, PDF, numeric registry/output, input manifest, gate, tool, fixture, author kit, requirement or bundle from the tested scientific release above. The final remote HEAD and this invariant are read back after that push; the local final-head receipt is retained outside the published tree to avoid a self-referential commit hash. The final user report identifies that observed HEAD.

## Pending work

T4 is owner work: two Small bundle uploads and real score/screenshots, exact Discord instructions and final-test nomination, final OpenReview form/anonymity rules and final click/receipt. None was performed by Codex. Both bundles remain byte-identical, with private-val/final-test outcomes UNMEASURED.

T5 is scheduled for October 31 at 20:00 Asia/Seoul, target completion by 21:00. It has not run; no second snapshot or kill-rule outcome is claimed. The automation ID is `aimo-v6-leaderboard-rescrape`.

New GPU jobs and paid-service spend are both zero. Historical v5 publication receipts remain under `results/v5/publication/`.
