# Supplemental audit of the frozen v8.3 PDF

This sidecar is separate from the pinned `audit_v83.py` and the immutable v3 gate. It does not replace, edit or override their raw results. It creates no PDF and makes no network request. **H2/G-LOOK remains PENDING.**

Actual result: **PASS 19/19, exit 0.** Negative controls: **13/13 correctly rejected or distinguished, exit 0.** The controls are invented in-memory observations and strings, not modified PDFs or competition receipts.

The full PDF hash must be `2edf06ab6764af045e470acdc77f115700d9cf85303a11d174c80e273c182e51`. The reference layout text must have SHA-256 `b740a790bfca2bb0400ea3dc2f5dc84da20a92616b3d12f33d552031ad31dc0a`. Neither is merely reported as an unconditional PASS.

Checks cover actual page count and exact page-5/page-6 boundary; required nonempty anonymous Author; case-insensitive identity scans over text, document/XMP metadata and URI targets; absence of attachments and associated files; successful text extraction; successful `pdffonts` with valid font rows and zero Type 3; complete E4 paragraphs separately in abstract and Limitations; the preserved final-test unknown context; and section-wise fidelity against R1 after explicit known transformations.

The legitimate sentence “Final-test performance of these bundles is also UNMEASURED.” is required in context. It is not treated as a forbidden word. The original audit's blanket `UNMEASURED` failure remains the original audit's own recorded result.

Fidelity compares all section bodies and order, rather than declaring a sentence diff successful. It removes page-number/Preprint footers, normalizes whitespace/Unicode extraction forms, and ignores **alphabetic ASCII compound/display hyphens**. This is an explicitly limited text comparison, not a general proof of scientific meaning. Unicode mathematical minus U+2212 remains distinct; its negative control prevents `x−y` from collapsing to `xy`. Full byte identity separately anchors the previously reviewed artifact. No fresh all-ten-page visual review is claimed.

The four disclosed changed lines are retained verbatim in the JSON:

1. “We provide CPU reproduction rather than additional model runs.”
2. “The 24 October temporary-evaluation-queue notice is documented in the supplied v8.3 handoff; the recorded queue responses accompany the archive.”
3. “[withheld for anonymous review]”
4. “The recorded queue receipt JSONs accompany the reproduction archive.”

The reference contains named-author material and belongs to the private audit handoff. The audit bundle and raw original sentence diff should not be mistaken for an anonymous OpenReview supplement.

Run with an existing interpreter containing `pypdf` and system Poppler. No package installation is needed:

```sh
python3 -I supplemental_audit.py ANONYMOUS.pdf reference/v8.1-named-approved.txt
python3 -I negative_controls.py ANONYMOUS.pdf reference/v8.1-named-approved.txt
```

`EXECUTION.json` records the exact interpreter, commands, dependencies and hashes used in this workspace. `actual.stdout.json` is the real artifact result; `negative_controls.stdout.json` is synthetic-control evidence. Output JSON is local artifact QA, not author approval, mirror verification, external authentication or submission completion.
