# V6 gate scope and receipt audit

The two supplied tools, `research/PREREG_v6.json`, and five `tests/fx_*.json`
fixtures are copied byte-for-byte from the v6 attachment. Their hashes are
recorded in `results/v6/gate_fixture_receipts.json`. The recorded fixture runs
are synthetic tests, not owner submissions or private-validation evidence.
No `results/v6/codabench_receipts.json` has been fabricated.

`tools/reproduce_report.py` keeps the V1–V4 checks and expected values intact.
V4 remains an expected exit 1 with `CLOSED`; it does not reopen a method track.
V5 regenerates the hashed leaderboard analysis and compares 22 fixed values
(the 20 required handoff values plus the two Bonferroni counts) both with the
analysis output and with the report-number pipeline. V6 requires the frozen
text gate to return `CLEAN` for `report/main.tex`, `report/main-anonymous.tex`,
and `report/REPORT_DRAFT.md`. It regenerates both TeX sources and their source
provenance from the gated Markdown in a temporary directory and requires
byte parity with the tracked files. `V6_owner_render_scope` also runs the
synthetic scoped-rendering regression suite; it never supplies owner evidence.

The separate `owner_receipt_scope` check records whether owner bundle results
may be stated. Missing receipts affect only the two bundle-specific
private-validation statements, not the public snapshot analysis or report
build. The current status is `UNMEASURED`. The gate's rendering deadline is
2026-11-01 11:55 UTC (20:55 KST). At or after that instant the rendering gate
expires, but absent or invalid receipts remain `UNMEASURED`; expiry is never
evidence for a score.

## Why the supplied receipt verdict is not report prose

The frozen receipt gate's matching verdict says two 7/14 scores license a
per-problem label-balance conclusion. That inference is invalid: matching
aggregate scores are compatible with multiple per-problem label assignments.
The constant score concerns overall prevalence; a single problem-only score
does not identify every problem's label balance. The frozen expectations
were informed by an already visible board and prior report. The report calls
them **receipt expectations**, rather than pre-registered predictions.

The frozen gate also silently overwrites duplicate bundle rows, ignores
submission IDs, accepts an accuracy outside [0, 1] as a mismatch, and does not
validate supporting screenshots or timezone-aware timestamps. A passing
fixture exit is therefore only the specified fixture behavior. In particular,
the fixture IDs `t` and future fixture timestamps are not live evidence.

`tools/codabench_receipt_scope.py` adds conservative validation without editing
the supplied gate or registration. It requires one receipt per expected
bundle, distinct numeric submission IDs, a finite accuracy in [0, 1] fitting
the registered item count at displayed precision, timezone-aware timestamps
after registration and no later than the check, and supporting screenshot
files. The existing gate additionally checks bundle hashes, tracks, finished
status, and chronology. A screenshot path is resolved relative to the
receipts JSON directory. This checks recorded evidence structure, not its
external authenticity; owner/service evidence review remains necessary.

Even when both tools accept recorded receipts, the wrapper permits only the
recorded bundle scores and always sets
`per_problem_balance_inference_allowed: false`. It never copies the supplied
`CONSISTENT` or `REFUTED_OR_PARTIAL` prose into the report. If any receipt is
missing or invalid, measured score statements remain prohibited. The wrapper
exits 0 because unrelated CPU gates must still complete. The numeric renderer
now consumes its structured state before checking numeric placeholders and
the registry. The outline has exactly one `BEGIN_OWNER_PRIVATE_VALIDATION` /
`END_OWNER_PRIVATE_VALIDATION` HTML-comment pair inside section 4. If measured
score statements are not allowed, only that block is replaced by
`report/OWNER_PRIVATE_VAL_UNMEASURED.md`; the comments are removed from the
rendered manuscript. This replacement continues after the deadline. If strict
receipts permit recorded score statements, the authored block still must pass
the numeric registry and literal gates.

The fallback file's exact SHA-256 is pinned in `tools/render_report.py`:
`e51dd37e3eefe81e0163aa20d4fe8c5b68fd9acf99c296506e14b2f448298da2`.
A changed fallback or missing, duplicated, reversed or misplaced marker pair
is an explicit configuration error. Changing the fallback file alone cannot
inject fabricated measurements. The marker requirement applies to the v6
`REPORT_OUTLINE.md` beside that canonical file; the historical markerless v5
preregistered outline and unrelated older fixture outlines remain supported.

## Verification

Run `python3 -I tests/test_v6_gates.py`. These tests verify all five supplied
fixture exits (0, 0, 1, 1, 1), the mismatch verdict prefix
`REFUTED_OR_PARTIAL`, missing evidence immediately before and at the deadline,
the restriction on balance inference, rejected weak receipts, and the text
gate across both source formats. All generated positive-test receipt files
and evidence placeholders exist only in temporary test directories and are
explicitly synthetic.

Run `python3 -I tests/test_owner_private_renderer.py` for the seven synthetic
rendering tests. They inject an unmeasured private-score claim and verify that
only its guarded block is replaced while public statistics survive, verify
the same behavior after deadline expiry, permit a candidate only with strict
synthetic receipts, retain numeric-registry rejection, reject invalid marker
structure and fallback tampering, and preserve the historical v5 outline.
