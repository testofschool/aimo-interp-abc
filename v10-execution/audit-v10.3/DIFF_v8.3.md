# v8.1 to v8.3 content and layout differences

Frozen anonymous PDF SHA256: `2edf06ab6764af045e470acdc77f115700d9cf85303a11d174c80e273c182e51`. No PDF/source edit or rebuild in this audit.
Approved reference layout-text SHA256: `b740a790bfca2bb0400ea3dc2f5dc84da20a92616b3d12f33d552031ad31dc0a`.

## Declared changes

- E4: replace pending baseline prose with the two supplied temporary-queue observations (each7/14, UUID, KST timestamp), explicitly not on the leaderboard; compare only with the declared fair-coin null. Final-test performance remains UNMEASURED.
- E11: sections1–3 remain the five-page main body; old§5 becomes unnumbered Limitations, followed by AI Use Statement and References; old§4/§6 move to AppendicesA/B. Tables retain their contents; cross-references and page reflow change.
- E12: anonymous author metadata, anonymous repository URLs, Korea→KST and anonymous self-source masking; named original remains reference material.
- Citation[11] moves to the removal sentence and its supplied queue provenance is stated.

## Four previously disclosed lexical changes, verbatim

1. previously disclosed E4 lexical normalization, beyond literal queue replacement

Old: `We provide CPU reproduction and frozen reference baselines whose private-validation results remain unmeasured.`

New: `We provide CPU reproduction rather than additional model runs.`

2. previously disclosed reference provenance addition beyond moving [11]

Old: (no prior sentence)

New: `The 24 October temporary-evaluation-queue notice is documented in the supplied v8.3 handoff; the recorded queue responses accompany the archive.`

3. previously disclosed anonymous self-source privacy normalization under E12

Old: `6f81bc3b31472dfeb1179b25c31fd7bb128dd19f`

New: `[withheld for anonymous review]`

4. E4 false-pending receipt cleanup, explicitly disclosed

Old: `Private-validation receipts are pending.`

New: `The recorded queue receipt JSONs accompany the reproduction archive.`

## Fidelity evidence and limits

The v10.2 section-aware checks retained in H2_CHECKS.json passed14/14 and found no undisclosed source semantic delta. Its full whitespace PDF diff has36 blocks because moves, line reflow, headers/footers and the disclosed changes remain visible. This count is not a count of scientific changes.
The original supplied audit script reports sentence differences as informational with ok=True and truncates added/removed lists to40. That field is not used as a fidelity PASS. Full PDF text diff and section-aware evidence accompany this bundle.
The v10.3 amendment correctly removes the mtime false alarm and reads old§5 as the unnumbered Limitations. These interpretations do not approve the PDF; H2 remains pending.
