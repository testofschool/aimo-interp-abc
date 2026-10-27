# Independent review of the exact patched audit

**The revised audit genuinely returned FAIL (exit1), solely `FORBIDDEN_0: {"Codex":1}`.** Its SHA-256 exactly matches the supplied `375a982380f2e0eb43bfe9d85b1c91d1cf0fade81c02613bf0fb902ba46b582c`. This review read the executor's raw result and independently located the word in the actual PDF; it did not execute or modify the checker.

The matched source is page6, **AI Use Statement**:

> The tools were Anthropic Claude and OpenAI Codex, including independent AI agents used for cross-checks.

`Codex` occurs once in the complete PDF; `handoff` occurs zero times. The script adds `Codex` to a global FORBIDDEN list at lines12–14 and scans the whole normalized text at lines81–83. Consequently the result is the literal operation of the new rule, rather than evidence of an unexpected paper edit or an author identity leak. The AI statement remains the previously disclosed tool-use statement and was outside the user's exact two-edit scope. **Do not remove or obscure it to manufacture PASS.**

Current PDF SHA-256 is `8c78e829da9988fc2ef37532c8880f9ee031812382a2de6017dcf46b470b98aa`; it exactly equals the PDF blob committed in `9d4530995fb44d93575b598f31c2da761db072a5`. The raw script result remains FAIL. The independent two-edit fidelity/visual PASS is a separate finding and does not override this checker result.

Unchanged logic limits: SHA row55 is observational/unconditional; Author metadata does not affect IDENTITY_0 at76; subprocess statuses at28/30/74/87 are unchecked; E4 checks78–79 use global presence; sentence-diff95 is unconditionally true and can echo named-reference text. Line81 also uses a case-insensitive predicate with a case-sensitive displayed count. These limits are documented rather than silently repaired.

**H2 remains pending.** The existing H1 authentication wait was not inspected, altered, cancelled or resumed. This review performed no PDF/checker edits, authentication, POST, push or commit. Detailed evidence and exact line references are in `independent_review.json`; executor stdout and provenance remain unchanged alongside it.
