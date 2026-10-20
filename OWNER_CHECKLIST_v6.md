# Owner handoff — v6

Public CPU analysis and report release are separate from account submissions.
Codex does not click Codabench/OpenReview or message organizers or participants.

1. Before 2026-11-01 20:55 KST (11:55 UTC), upload the two unchanged Small bundles:
   `bundles/solution-text-length-control-small.zip` (SHA256
   `30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd`) and
   `bundles/solution-always-true-small.zip` (SHA256
   `4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a`).
2. Record each bundle, hash, Small track, numeric submission ID, native terminal
   status, accuracy, timezone-aware submitted_at, and screenshot path in
   `results/v6/codabench_receipts.json`. The screenshot path is relative to that
   JSON's directory. Preserve real service screenshots with time. No live
   receipt file has been created by this release.
3. Run `python3 -I tools/prereg_codabench_gate.py research/PREREG_v6.json results/v6/codabench_receipts.json`
   and `python3 -I tools/codabench_receipt_scope.py`. The frozen gate's prose is
   diagnostic; use only actual recorded scores in the paper. Neither two
   matching nor mismatching aggregate scores prove per-problem composition.
4. Read Discord #announcements September 15/16 balance/rebuild notice and current
   report hour/timezone, OpenReview anonymity and final-test nomination instructions.
   Paste the exact text with message date/link in `research/discord_2026-10.md`.
   The organizer issue states that final-test submissions require nomination;
   ordinary uploads do not establish nomination.
5. Review both PDF variants. The author block is Jung Min Kang, independent.
   Verify final page/anonymity/file/deadline instructions in the actual submission
   invitation before choosing the variant. Its public API is now readable, but
   explicit PDF anonymity/page-limit instructions remain UNVERIFIED; retain both
   variants. The current portal duedate is November 1, 2026 at 17:00 KST (08:00
   UTC), while the official website still gives November 15 and a November 1-15
   report window. This is CONFLICT_UNRECONCILED. The portal's 17:30 KST expiration
   is not its due date. Open the exact invitation linked in
   `research/v6_sources/PORTAL_CHECK_2026-10-20.md`, preserve its displayed deadline
   and PDF author instructions, and compare with the current Discord announcement.
   Do not rely on November 15 as a confirmed portal cutoff.
6. Perform the OpenReview final click and preserve its receipt. Teams considered
   for awards commit to up to three reviews during November 15–30, 2026.

October 31 rescrape: scheduled in this chat for 20:00 KST, target completion by
21:00 KST. This is future work, not a completed second snapshot. Automation ID:
`aimo-v6-leaderboard-rescrape`. No future score or kill-rule outcome is asserted.

Sources: [official website](https://aimo-interp.github.io/) and
[organizer issue 10](https://github.com/aimo-interp/getting-started/issues/10).

Owner confirmed on October 20 that submissions and announcement checks have not
yet been performed. Scores remain UNMEASURED; no receipt is implied by this checklist.
