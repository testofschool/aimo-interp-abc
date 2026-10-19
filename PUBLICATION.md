# Completion-corrected v6 public publication — 2026-10-20 KST

Observed public scientific/build HEAD: `524cc98816b2cd31bafd7c4e4e25f66a093e2cf5` ([commit](https://github.com/testofschool/aimo-interp-abc/commit/524cc98816b2cd31bafd7c4e4e25f66a093e2cf5)). Author: `felix <gangjeongmin23@gmail.com>`. Prior initial v6 readback at e2fa9b6/60b21dd is retained in Git history; it did not cover these completion corrections.

## Scope of this corrected release

The completion audit copied omitted comp.json (all 9 attached JSON files now present with manifest hashes), restored the inherited exact label rules, and connected receipt scope to the renderer. Missing or invalid owner receipts now replace only the marked section 4 paragraph with the hash-pinned UNMEASURED fallback. Deadline expiry never creates a score. Usage documentation states the fixed-family/adaptive-stopping condition. Statistical numbers, formulas, dependency pins and both submission bundles are unchanged. See COMPLETION_AUDIT_v6.md for every requirement and remaining work.

## Actual fresh public readback

A separate new anonymous clone was created with credential helpers, HTTP extra headers, global/system Git configuration and interactive authentication disabled. Its HEAD matched ls-remote. A new Python 3.13 environment installed unchanged requirements. Four absent parquet files were freshly downloaded over the network and all hashes matched. All 9 published snapshot JSON files, including comp.json metadata, matched manifest hashes and sizes. The numeric analysis uses 8 leaderboard pages; metadata is not an additional scored page.

| Check | Observed result |
|---|---|
| V1_original | PASS |
| V2_original | PASS |
| V1_final | PASS |
| V3 | PASS |
| V2_final | PASS |
| V4 | PASS—expected CLOSED/exit1 |
| V5 | PASS |
| V6_source_regeneration | PASS |
| V6_owner_render_scope | PASS |
| V6 | PASS |
| owner_receipt_scope | PASS |

The integrated V6 scope suite comprises 7 synthetic cases; none is a service observation. The existing 5-case receipt suite and 7-case leaderboard regression suite also passed. The owner scope remains UNMEASURED. Full stdout/stderr, exact invocations, network-fetch receipt, snapshot completeness and CPU gate JSON are under results/v6/publication/. These are CPU/macOS reproduction checks, not GPU-container parity.

## Published PDFs

| Variant | Body + references | SHA256 | Type3 fonts |
|---|---:|---|---:|
| named | 8 + 1 | `6114f15549c07c12efce021a6521d0d72d20c53adc46079d3a4bba9558eef9ef` | 0 |
| anonymous | 8 + 1 | `f1d2a4df94c1669c6f0e2e3dc67c7dda6324b51b8ccc83b28a95a77d79d88ebb` | 0 |

Each public PDF is byte-identical to its locally reviewed final artifact. Both rendered all 9 pages from the new public clone. All 18 final pages were visually inspected, and the final source regeneration/text gates pass. Style bytes, base fonts and page geometry remain unchanged. Exact text/format differences are classified in report/REGEN_FIDELITY_v6.md.

## Receipt-only follow-up

This record and these observed readback receipts are published in a follow-up commit. That follow-up changes only current-state documentation and receipts. Every manuscript, PDF, numeric artifact, manifest, code file, fixture, requirement, author kit and bundle must remain byte-identical to the corrected scientific/build HEAD above. The final remote HEAD is read back after the follow-up; the local final-head receipt remains outside the public tree to avoid a self-referential commit hash.

## Required work still incomplete

T4: Felix must upload both unchanged Small bundles and provide linked native scores/screenshots, record exact Discord announcements, follow final-test nomination instructions and handle the final OpenReview form and submission. No actual codabench_receipts.json, discord_2026-10.md or final submission receipt exists. Own private-val/final-test results remain UNMEASURED. Codex did not perform account clicks or send messages.

T5: the October 31 rescrape and kill-rule decision have not run. A single follow-up is active for October 31 at 20:00 Asia/Seoul, target completion by 21:00; ID aimo-v6-leaderboard-rescrape. A configured schedule is not completion. The full goal therefore remains incomplete.

New GPU jobs: 0. New paid-service spend: USD 0.
