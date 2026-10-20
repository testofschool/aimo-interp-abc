# Public Submission invitation check — October 20, 2026

Status: **CONFLICT_UNRECONCILED** for the report deadline; **UNVERIFIED** for PDF
anonymity and final page instructions. Both existing PDF variants remain.

The exact venue Submission invitation is the governing layer for its form and
configured cutoff; the organizer website is a separate rules layer. The v2 API
now returns one invitation. The API response includes `fromCache=true`; the
invitation web route embeds matching schema, while its unauthenticated visible
shell shows Loading/Login. No authenticated rendered form was observed.

| Observed invitation field | Epoch milliseconds | UTC | Asia/Seoul |
|---|---:|---|---|
| duedate | 1793520000000 | 2026-11-01 08:00 | 2026-11-01 17:00 |
| expdate | 1793521800000 | 2026-11-01 08:30 | 2026-11-01 17:30 |

The [official website](https://aimo-interp.github.io/) still gives November 15 for
reports and a November 1-15 window. The table reports the portal configuration;
it does not settle organizer intent or withdraw the website rule. Expiration is
distinct from the due date.

The API requires author profiles and a PDF, with `maxSize=50` (unit not inferred).
Metadata authors and publication consent do not establish PDF anonymity.
Whole-token checks on the 5,229-byte invitation find anonymous/anonymity/anonymized/
blind each 0; controls author=6, authors=6, submission=16, PDF=4. These checks cover
the retrieved schema only, not Discord or an authenticated form. Silence does not
authorize an author variant.

Owner readback: open the [exact invitation](https://openreview.net/invitation?id=NeurIPS.cc%2F2026%2FWorkshop%2FAIMOInterp_Challenge%2F-%2FSubmission)
from the verified venue; preserve its displayed deadline and PDF anonymity/author
instructions, then compare the current Discord report announcement. No account
submission or organizer message was performed. The owner confirmed on October 20
that submissions and announcement checks are still pending.

Evidence was fetched at 2026-10-20 02:13 UTC / 11:13 KST. Raw responses are kept
locally; this public record redistributes provenance and factual observations.

| Primary response | Bytes | SHA256 |
|---|---:|---|
| [Exact Submission API v2](https://api2.openreview.net/invitations?id=NeurIPS.cc%2F2026%2FWorkshop%2FAIMOInterp_Challenge%2F-%2FSubmission) | 5229 | `2fb04678e3178020639a4a8ad44aff8f146294242af341b859415d30903aca8b` |
| Official website | 92354 | `46f0c2a32c47f41ab09e54ab9bd0b23b41069890db8c6aad87a3736873a00fba` |

The earlier source audit's unavailable-invitation entry is historical and is
superseded by this check for current access. Scientific results and source/PDF
bytes are unchanged. This update supplies no missing owner result or future
leaderboard snapshot and does not complete the full goal.
