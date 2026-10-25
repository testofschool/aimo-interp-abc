# Installed v3 versus prior local gate: diff and controls

The user selected the exact supplied v3 as the T1 basis. It was inspected and executed without modification. The old gate was read for comparison only and **was never executed** in this audit.

| File | SHA-256 |
| --- | --- |
| Prior `2.2+local.1`, comparison only | `320869903e0448ea514383288743391981e7a5b8c28eda590acfdde3a7908c43` |
| Active supplied v3 | `152e2a488eb0c3cdeadbe4195bb09ac90acab464df4326a612098dc63f5c7630` |

## Normal-mode changes

The 16-item CHECKS list changes only the REPO_URL predicate: v3 additionally accepts `anonymous.4open.science`. The other 15 predicates and negation counter are AST-equivalent. The normal PDF total rises from17 to19 by adding:

- MAIN_BODY_5_PAGES: extracts every PDF page and finds the first Limitations / AI Use Statement / References / Appendix heading.
- ANONYMIZED: checks a fixed list of known identity strings and PDF Author metadata.

These two new checks run only for `.pdf` inputs. Text input is not a substitute for the required19-check PDF validation. These are lexical/layout checks; they do not authenticate a receipt, prove the URL/mirror exists, or establish complete anonymization.

The old structured `version`, `test_only`, `test_inputs`, `evaluated_at`, `fallback_at`, `probe`, `fallback_eligible`, and `scope` fields are absent from v3 output. Use the active source hash in build receipts to identify the gate.

## Local hardening removed by supplied v3

The following are direct code-diff observations, not fresh operational fallback experiments. The current task uses normal mode and does not need fallback.

| Prior local hardening | Supplied v3 behavior |
| --- | --- |
| Clean rejection of invalid/timezone-free test clocks | ISO parse/aware-vs-naive comparison is uncaught and can traceback |
| Any alternate probe URL makes a usable run TEST_ONLY | Only `--now` or `--probe-result` sets TEST_ONLY |
| TEST_ONLY keeps blocks populated even on simulated success | blocks is null when lexical checks pass, although test exit remains3 |
| All fallback prerequisites applied globally | Fallback checks run only if an ordinary ID_FIELD/OWN_SCORE predicate first fails |
| Explicit current outage +UNMEASURED +planned-not-run +noIDs +organizer citation and recovered/workaround rejection | Broad outage/citation matching; those added local declarations/contradiction checks are absent |
| Any HTTP reply, including302/503, blocks automatic outage exception; no redirects | Follows redirects and treats HTTP≥500 or most exceptions as down |
| Narrow network/timeout down class; TLS/unknown stays unverified | Generic exception path generally yields down |
| PDF word/compound line-break flattening for fallback | Added flattening is absent |

The source remains locked to the requested v3 hash; this report does not silently reapply any old hardening.

## Executed controls

Both actual approved v8.1 PDFs were run **only with v3**, in normal mode:

| Variant | Exit | Result | Normal checks | Main body | Identity hits | Anonymous Author metadata |
| --- | --- | --- | --- | --- | --- | --- |
| Named |1|FAIL|15/19|7 pages|5|false|
| Anonymous |1|FAIL|15/19|7 pages|3|true|

Their failures are exactly ID_FIELD, OWN_SCORE, MAIN_BODY_5_PAGES, ANONYMIZED. Negations remain40. Named SHA31c5ee0c…2c95 and actual anonymous SHAb6c3fc29…05bd8 are recorded in CONTROLS.json; the handoff's older anonymous hash is not treated as the current canon.

Pure-function synthetic controls (no PDF generation or service submission) confirm five body pages→5 and six→6 when an unlimited section starts on the following page. They also expose the built-in tolerance: three nonempty body lines before Limitations on page6 still returns5, while four returns6. Therefore the final render must independently show that all actual main text ends on or before page5; gate PASS alone is insufficient.

Two lexical controls show an E4 wording conflict: exact plural `submission ids <UUID> and <UUID>` fails ID_FIELD, while singular `submission id <UUID>` passes. The locked predicate requires the singular label even though the handoff's E4 says plural. Use source-backed singular labels as an explicit reported E4 wording delta; do not edit v3 to hide the issue.

Another E11 interaction: EFFICIENT is scoped to text before AI Use Statement. The exact cost phrase `rather than additional model runs` currently occurs only in old§6. Moving§6 after references into AppendixB removes that phrase from the predicate's scope. A truthful cost clause must remain in abstract/main text/Limitations, recorded as a layout-related wording delta. GENERALIZATION remains covered by the main§1 `held-out problem` phrase.

## Evidence and limits

`CONTROLS.json` holds source hashes, exact PDF hashes, observed rows and synthetic controls. Per-variant gate JSON/stdout/stderr are saved beside it. Main-body function controls do not prove visual page quality. No queue POST, credential use, mirror creation, push or OpenReview operation was performed. Future PDF review, actual mirror readiness and latest venue requirements remain separate conditions.
