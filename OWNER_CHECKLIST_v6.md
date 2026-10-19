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
   invitation before choosing the variant. It is not publicly readable in this
   audit; retain both variants. Website context says November 15, 2026 for reports,
   but the final hour/timezone is unverified.
6. Perform the OpenReview final click and preserve its receipt. Teams considered
   for awards commit to up to three reviews during November 15–30, 2026.

October 31 rescrape: scheduled in this chat for 20:00 KST, target completion by
21:00 KST. This is future work, not a completed second snapshot. Automation ID:
`aimo-v6-leaderboard-rescrape`. No future score or kill-rule outcome is asserted.

Sources: [official website](https://aimo-interp.github.io/) and
[organizer issue 10](https://github.com/aimo-interp/getting-started/issues/10).
