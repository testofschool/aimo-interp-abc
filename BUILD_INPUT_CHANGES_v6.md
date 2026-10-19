# v6 build-input changes

Compared against the exact public v5 HEAD `9274840b6faacaa7ad0e321172071eedb822d9de`. The original dirty working repository was not reset or committed. Full hashes: `results/v6/build_input_changes.json`.

| File | Action | Before bytes | After bytes | Delta |
|---|---|---:|---:|---:|
| `data/leaderboard/2026-10-19/comp.json` | ADD | 0 | 10002 | +10002 |
| `data/leaderboard/2026-10-19/lb1.json` | ADD | 0 | 34412 | +34412 |
| `data/leaderboard/2026-10-19/lb2.json` | ADD | 0 | 32636 | +32636 |
| `data/leaderboard/2026-10-19/lb3.json` | ADD | 0 | 33836 | +33836 |
| `data/leaderboard/2026-10-19/lb4.json` | ADD | 0 | 33130 | +33130 |
| `data/leaderboard/2026-10-19/lb5.json` | ADD | 0 | 33365 | +33365 |
| `data/leaderboard/2026-10-19/lb6.json` | ADD | 0 | 33333 | +33333 |
| `data/leaderboard/2026-10-19/lb7.json` | ADD | 0 | 33433 | +33433 |
| `data/leaderboard/2026-10-19/lb8.json` | ADD | 0 | 33095 | +33095 |
| `data/manifest.json` | MODIFY | 7141 | 9961 | +2820 |
| `report/ALLOWED_LITERALS.txt` | MODIFY | 740 | 885 | +145 |
| `report/OWNER_PRIVATE_VAL_UNMEASURED.md` | ADD | 0 | 692 | +692 |
| `report/REPORT_OUTLINE.md` | MODIFY | 16448 | 34848 | +18400 |
| `report/create_source.py` | MODIFY | 8564 | 9978 | +1414 |
| `report/main-anonymous.tex` | ADD | 0 | 48012 | +48012 |
| `report/main.tex` | MODIFY | 30228 | 48013 | +17785 |
| `requirements-local.txt` | UNCHANGED | 190 | 190 | +0 |
| `research/PREREG_v6.json` | ADD | 0 | 1373 | +1373 |
| `research/claims.json` | MODIFY | 13615 | 25944 | +12329 |
| `research/identifiability_expected_v6.json` | ADD | 0 | 955 | +955 |
| `research/live_audit/neurips2026_author_kit.zip` | UNCHANGED | 20259 | 20259 | +0 |
| `tests/fx_badsha.json` | ADD | 0 | 396 | +396 |
| `tests/fx_early.json` | ADD | 0 | 518 | +518 |
| `tests/fx_match.json` | ADD | 0 | 518 | +518 |
| `tests/fx_mismatch.json` | ADD | 0 | 519 | +519 |
| `tests/fx_missing.json` | ADD | 0 | 16 | +16 |
| `tests/test_owner_private_renderer.py` | ADD | 0 | 7791 | +7791 |
| `tests/test_v6_gates.py` | ADD | 0 | 5066 | +5066 |
| `tools/codabench_receipt_scope.py` | ADD | 0 | 5526 | +5526 |
| `tools/fetch_data.py` | UNCHANGED | 6323 | 6323 | +0 |
| `tools/leaderboard_identifiability.py` | ADD | 0 | 16758 | +16758 |
| `tools/optional_mixed_label_transfer.py` | ADD | 0 | 3872 | +3872 |
| `tools/prereg_codabench_gate.py` | ADD | 0 | 2729 | +2729 |
| `tools/render_report.py` | MODIFY | 2745 | 6853 | +4108 |
| `tools/report_numbers.py` | MODIFY | 11995 | 12555 | +560 |
| `tools/reproduce_report.py` | MODIFY | 4259 | 7491 | +3232 |
| `tools/submission_text_gate.py` | ADD | 0 | 1526 | +1526 |
| `tools/test_leaderboard_identifiability.py` | ADD | 0 | 4298 | +4298 |

`requirements-local.txt`, the original dataset fetcher and official author kit are byte-identical. Python 3.13 was used because the host default Python 3.10 cannot install the existing numpy pin; no dependency pin was changed. Mandatory new leaderboard computations use the already pinned scipy/pandas.

The two supplied gates, PREREG_v6 and five fixture inputs are byte-identical to the attachment. A separate conservative owner-evidence wrapper addresses semantic/schema limitations while keeping that supplied reference intact. No new GPU job, language-model prediction or paid service was used.

Generated JSON/Markdown, two PDFs, final page images and logs, provenance, expected-value tables, publication receipts and current-state documentation are output artifacts rather than build inputs. Their exact file membership is listed in RELEASE_FILES.json. Historical v5 files retain their own versioned statements.

Completion-audit correction: T1.1 requires every attached snapshot JSON, including competition metadata comp.json. Its exact pinned bytes and manifest entry were added after the initial public release. It does not enter leaderboard parsing or numeric calculations. The usage document was also aligned with the already-qualified fixed-family/adaptive-stopping condition in the report. No numerical or PDF bytes changed.

The inherited exact label rules were restored in the report. The existing renderer now enforces the owner paragraph scope with a hash-pinned fallback; seven synthetic rendering cases are integrated into V6. Source/PDF hashes were regenerated and visually rechecked; statistical numeric outputs remain identical.
