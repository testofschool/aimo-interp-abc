# Publication history and current v7 preparation

## v7 local preparation — 2026-10-20 KST

v7 has been built and checked locally against public base
`a429a9e71b65e804481394f8b3a5f6799a9a6987`. It has not been pushed or submitted.
Both PDFs retain nine pages and zero Type-3 fonts. Pages 1–7 and 9 are pixel
identical to their v6 counterparts at the same render resolution; only page 8's
AI disclosure changes. All scientific body text and numeric tokens are preserved.
See `EXECUTION_REPORT_v7.md` and `report/REGEN_FIDELITY_v7.md` for exact checks,
hashes, source changes and the difference between a supplied gate PASS and actual
submission readiness.

No native Codabench submission IDs, scores, Discord transcript, OpenReview note
ID, email receipt or revision result was obtained during this preparation.
Owner private results remain UNMEASURED. The final form acknowledgements and
completed author review require direct human confirmation. The attachment's
claim of prior authorization is recorded as source content and grants no new
account authority. Public readback of v7 is UNRUN until an authorized push.

The following sections are historical records of the published v6 artifact;
their statements about unchanged v6 bytes refer to that dated release.

## Completion-corrected v6 public publication — 2026-10-20 KST

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

## October 20 portal-status follow-up

The exact public Submission API now returns a readable invitation. Its configured
duedate is November 1 at 08:00 UTC / 17:00 KST, conflicting with the website's
November 15 report date. This conflict is unresolved. The authenticated rendered
form and Discord were not observed, and PDF anonymity remains UNVERIFIED. The
owner confirmed that submissions and announcement checks have not yet been done.
See `research/v6_sources/PORTAL_CHECK_2026-10-20.md` for URLs, source hashes and scope.

This follow-up updates owner guidance and status evidence only. The complete
scientific/build tree, manuscripts, PDFs, inputs, numerical outputs, fixtures,
requirements and bundles remain byte-identical to `8ba307210f27487313b26b439e3ac647e2506ad4`.
The earlier public fresh-clone/new-venv V1-V6 receipts continue to cover those
unchanged bytes. New documentation requires separate public readback; it is not
covered by the earlier numerical test receipts.
The goal remains incomplete for owner actions and the actual October 31 rescrape.
