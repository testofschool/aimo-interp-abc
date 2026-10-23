# Portal audit — read-only, 2026-10-24

Applied [source-authority-gate](/Users/felix/.codex/skills/source-authority-gate/SKILL.md). Candidate layers: official website/rules, live OpenReview form schema, organizer issue clarification and supplied announcements transcript. The live form governs field syntax, license and portal deadlines; writeup-prize eligibility also needs the organizer clarification. Leaderboard prizes and writeup prizes differ. No account reads, credentials, Discord API, submission, sending, push or automation occurred.

## OpenReview

[Live invitation API](https://api2.openreview.net/invitations?id=NeurIPS.cc/2026/Workshop/AIMOInterp_Challenge/-/Submission) returned HTTP 200, 10,485 bytes; SHA256 fc1e071245f12c4c8da4f3f2f83135a012d8ccf7158f5c00413d0ca386be3c39. P4′ matches exactly: tmdate 1792785352965; due 1793969940000 = **2026-11-06 21:59 KST**, expiry 1793971740000 =22:29 KST. License is exactly CC BY-SA 4.0. Grade: raw-verified.

Current required fields: title, authors, reciprocal_reviewers, keywords, abstract, pdf, leaderboard_submission_ids, submission_track, ai_assistance, ai_use_statement, reciprocal_reviewing_acknowledgement, rules_compliance, venue, venueid. Optional: voluntary_reviewers, TLDR, white_box_award. P5's legacy list is incomplete on its own; submission_track and voluntary_reviewers are the changes already recorded in P4′. Current effective P5 matches. Allowed tracks: Main track; Small models track. note.id remains optional. Full field descriptions and single-value acknowledgements are preserved in openreview_schema_extracted.json.

Reciprocal reviewer is assigned three papers; late or missing reviews can cause desk rejection and no awards. Nomination IDs remain required, and only the first two IDs are evaluated/ranked for prizes. The string none matches the regex syntactically; organizer acceptance of it is **UNVERIFIED**.

Deadline conflict is preserved: [official website](https://aimo-interp.github.io/) and transcript say November 5 23:59 AoE, which converts to November 6 **20:59 KST**, one hour earlier than portal due. Existing D-010 fixes portal binding; this audit does not reopen that decision.

## Codabench

[Home](https://www.codabench.org/), [competition 16180](https://www.codabench.org/competitions/16180/) and [public API 16180](https://www.codabench.org/api/competitions/16180/) each failed from this Mac before HTTP: curl 28, HTTP 000, zero response bytes, connect timeout approximately 10.005 seconds. Each call used max-time 20 seconds/connect-timeout 10 seconds. This is a bounded reachability observation, not proof of a universal outage. Phase dates, tasks, limits, participant approval and quota are UNVERIFIED/NOT_READ. The supplied transcript reports a planned workaround; no shipped workaround was independently verified. Grade: unverified for live phase state.

## Organizer clarification and remaining conflicts

[Issue 10 organizer comment](https://github.com/aimo-interp/getting-started/issues/10#issuecomment-5765789797) explicitly says no Codabench submission is required for writeup-prize eligibility. It immediately adds that writeup should report public-train, private-validation and test-set evaluations. Both clauses are preserved in raw/API evidence. The comment does not authorize a literal none nomination value. Grade: raw-verified clarification; fallback unresolved.

Page limit is **UNDETERMINED**. The official-site text count for page is 0 with working controls report=6 and deadline=3 (limit=2;9-page=0). Current OpenReview group instructions are empty; the form says AI Use Statement does not count toward a page limit, without a numeric cap. September 21 issue 10 provisionally suggested a standard 9-page paper and said an official format was not available yet. No inbox was consulted. Resolve with an organizer confirmation of numeric main-text cap and reference exclusions if needed.

## Proposal citation

[AIMO Interpretability Challenge, arxiv v1](https://arxiv.org/abs/2607.13899v1), submitted 15 July 2026, matches the supplied 14-author citation in count/order. The [latest v2](https://arxiv.org/abs/2607.13899), revised 20 October 2026, has 18 authors including Robert Belanec, Maria Matveev, Jan Mazak and Markus Schepers. Supplied citation can retain organizer/v1 provenance; do not represent its author list as current v2 metadata. Title/year/DOI match. Grade: raw-verified metadata only.

All exact source URLs, timestamps, bytes, hashes, transport results, field descriptions, and metadata appear in PORTAL_AUDIT.json, raw files, headers, stderr and .meta.json companions.
