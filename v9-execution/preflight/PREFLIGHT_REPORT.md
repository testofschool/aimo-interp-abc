# v10 T-PRE: live public preflight

Recorded October 27, 2026 KST (raw UTC timestamps in JSON). Read-only public checks; no credentials, login, POST, submission, push, private-data download, or leaderboard outcome inspection.

## Executor and tools

The actual executor is the Mac Studio workspace under `/Users/felix`, hardware model `Mac13,1`, macOS26.6.2, RAM64GiB. It is not the handoff's M5 `/Users/kangjungmin` environment. Starting HEAD was `33328fed2a38255f8a85b9d6ae1d54672c44e3bf` on `v8.3`, not the old542f44b. This records the starting observation; the parent may subsequently switch to v10.

All requested commands exist: git, python3, zip, curl, gh, pdftotext, pdfinfo, pdffonts, brew. Poppler26.04.0 is available, so no tool fallback/install was needed. Default Python is3.10.11. `TOOLS_MACHINE.json` preserves exact executable paths and version output.

Free disk at observation:11,248,704KiB (~10.73GiB), volume99%used. This is a measured resource limit, not a failed ZIP-preparation gate. No model inference/training was launched.

OpenReview package: default Python import failed with ModuleNotFoundError. Project `.venv` import timed out after20s; that does **not** prove absence. No package was installed by this subtask. A working SDK route must be established before H4/T-POST.

## Network

| Check | Method | HTTP | curl exit |
| --- | --- | --- | --- |
| CB1_HEAD | HEAD | 200 | 0 |
| HOST_GITHUB | HEAD | 200 | 0 |
| HOST_HF | HEAD | 200 | 0 |
| HOST_OPENREVIEW | HEAD | 301 | 0 |
| HOST_ANON | HEAD | 200 | 0 |
| CB2_COMPETITION | GET | 200 | 0 |
| OR1_INVITATION | GET | 200 | 0 |
| OFFICIAL_SITE | GET | 200 | 0 |

The OpenReview root301 is a responding host, and the actual invitation GET returned200. Anonymous hosting root200 is not G-MIRROR; the specific repository mirror was not checked here. Response cookie/auth header lines were removed before public retention; all GET JSON/HTML bodies are unchanged. `NETWORK.json` records hashes and sanitation counts.

## Pre-registered values

- **CB1 MATCH:** Codabench homepage HEAD200.
- **CB2 MATCH:** competition16180, Current phase30038 “Competition phase”, end2026-11-01T11:55Z = **Nov1 20:55KST**, limits10/day and300/person, Small task36241 and Main task36237. The phase advertises4200s execution time. Account-specific testofschool participation, approval, remaining quota, and actual submission usability remain **UNVERIFIED**. Anonymous `used_submissions=0` is not the user's quota.
- Phase metadata sets `hide_prediction_output=false`, but competition `enable_detailed_results=false`. Neither proves that per-item predictions will be downloadable. The preregistration must preserve the unavailable-predictions branch; no outcome/artifact was fetched.
- **OR1 MATCH:** tmdate1793023952361. Due **Nov6 21:59KST**, expiry22:29KST. CC BY-SA4.0. Optional supplementary ZIP≤50MB exists.
- **OR2 MATCH:** all14required/hidden-constant fields and4optional fields match the handoff. `venue`/`venueid` are hidden constants. PDF requires an anonymized main body≤5pages. The authors instruction permits one technical report per first author and checks IDs against one Codabench user. The ID field evaluates only the first two IDs. Queue UUID regex compatibility is not organizer acceptance or user-ID linkage.
- **GS1 MATCH:** de794053debe75a711400696e66b60937cebbb1b.
- **P1 MATCH:** a429a9e71b65e804481394f8b3a5f6799a9a6987.
- **D1 website corroborated:** Rule4's report deadline is November5AoE, giving the handoff's earlier **Nov6 20:59KST**. Keep that earlier deadline despite the portal's later hour. Current website also independently says≤5mainpages and one submission per first author. The generic site competition deadline is not substituted for the observed earlier phase closure.

No public pre-registered CB/OR/GS/P1 value mismatched. The machine/starting-revision assumption differs from the M5 handoff and must be handled explicitly without discarding the available Studio canon. Actual official scores S1 and GS2 artifact bytes were not part of this subtask and remain for H1 / bundle audit respectively.

## Authoritative receipts

- `CB2_COMPETITION.body`: raw public competition JSON; no leaderboard rows requested.
- `OR1_INVITATION.body`: full live official invitation JSON.
- `OFFICIAL_SITE.body` and `.txt`: raw official site and text extraction.
- `GS1_ls_remote.txt`, `P1_ls_remote.txt`.
- `PUBLIC_PREFLIGHT.json`, `NETWORK.json`, `TOOLS_MACHINE.json`.

Sources: https://www.codabench.org/api/competitions/16180/ ; https://api2.openreview.net/invitations?id=NeurIPS.cc/2026/Workshop/AIMOInterp_Challenge/-/Submission ; https://aimo-interp.github.io/ ; the two public Git remotes named in the handoff. These checks do not close H0–H5.
