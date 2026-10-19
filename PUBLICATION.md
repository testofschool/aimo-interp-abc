# Public release and fresh-clone verification

Repository: https://github.com/testofschool/aimo-interp-abc

Verified: 2026-10-20 00:12:01 KST. The approved source commit is
`6fef8753b2e21b0c53098e77fdbc6e72ad4d4251`. Anonymous GitHub API readback returned HTTP 200,
`private: false`, and default branch `main`. Git credentials were disabled for
`ls-remote` and the new public clone. A separate Python 3.12 environment installed
the pinned requirements and fetched all four exact organizer files from HF.

| Check | Result |
|---|---|
| Original V1 | PASS 13/13, exit 0 |
| Original V2 | PASS 17 placeholders, exit 0 |
| Final V1 | PASS 87/87, exit 0 |
| Final V2 | PASS 89 placeholders, exit 0 |
| V3 | PASS all 12 registered values |
| V4 | CLOSED, expected exit 1 |
| Text-control ZIP rebuilds | Both byte-identical |
| Standalone TeX regeneration | Identical SHA256 |
| Delivered PDF | Identical SHA256, 5 pages |

The tested PDF SHA256 is
`1ec9bfb0ac7e48c78ef13ae8ee78d9acdce953bd12bac1038a3bee08719194cf`.
The tested TeX SHA256 is
`95e9dde2250115e4a2475325a8719aa29527ac0992305257ab5ee2d1f3fa242b`.
No scientific manuscript, numeric registry, inference artifact, or executable
source changed after these checks. This follow-up commit adds publication-state
documentation and raw readback receipts. `RELEASE_FILES.json` inventories the
current payload; raw public-clone output is pasted below and retained separately.

```text
V1_original actual exit 0
{
 "result": "PASS",
 "checked": 13,
 "mismatches": []
}
V2_original actual exit 0
{"result": "PASS", "placeholders": 17, "out": "/var/folders/14/76vt1lk92056gjht3hr6xwq00000gn/T/aimo-report-ft7m0yrg/original.md"}
V1_final actual exit 0
{
 "result": "PASS",
 "checked": 87,
 "mismatches": []
}
V3 PASS: 12 registered values
V2_final actual exit 0
{"result": "PASS", "placeholders": 89, "out": "/var/folders/14/76vt1lk92056gjht3hr6xwq00000gn/T/aimo-report-ft7m0yrg/final.md"}
V4 actual exit 1
{"result": "CLOSED", "reason": "no self-made labels supplied; method track stays folded"}
ALL_CPU_GATES_PASS; V4_CLOSED_EXPECTED
```

The public clone, command argv, exit codes and stdout/stderr files are under
`results/v5/publication/`. The initial system-Python API read had a local CA-store
error; the verified run used the existing Python 3.12 environment with certificate
verification enabled. No repository or scientific input change was required.

The R3 public release/reproduction requirement is complete. The overall v5
submission remains incomplete: owner author review, Codabench uploads and native
scores/screenshots, final-test nomination, final OpenReview rules and submission
receipt remain outstanding. Private validation/test stay UNMEASURED. New GPU
jobs and spend for publication/reproduction: zero.
