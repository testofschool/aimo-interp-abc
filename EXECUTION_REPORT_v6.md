# v6 execution report — CPU only

T1–T3 completion corrections and T6 pass actual anonymous fresh-clone/new-venv public V1–V6. The current corrected scientific/build HEAD and observed readback are recorded in PUBLICATION.md. Owner submissions are UNMEASURED; T5 is scheduled, not executed.

## Tracks

| Track | Observed state | Evidence |
|---|---|---|
| T1 identifiability | PASS, 22/22 frozen checks; 150 total registry claims | results/v6/identifiability_validation.json, results/report_numbers.json |
| T1 optional historical transfer | PASS, 10/10 checks; MIT checked before computation; omitted from manuscript | results/v6/optional_transfer_validation.json |
| T2 report | PASS local numeric/text/source/render checks; both variants 8 body + 1 references pages | report/render_qa_v6.json, report/REGEN_FIDELITY_v6.md |
| T3 gates | PASS frozen fixtures and regression cases; no actual owner receipts | results/v6/gate_fixture_receipts.json, research/GATES_v6.md |
| T4 owner | PENDING; no Codabench/OpenReview clicks or Discord access | OWNER_CHECKLIST_v6.md |
| T5 future rescrape | SCHEDULED_NOT_RUN, October 31 at 20:00 KST, target by 21:00 KST | results/v6/schedule.json |
| T6 publication | See PUBLICATION.md for observed public state and fresh-clone gates | results/v6/publication/ |

The original dirty `aimo-abc` checkout was preserved. Work is in the clean v6 public-repository clone under `v6-execution/work`, based exactly on public v5 HEAD `9274840b6faacaa7ad0e321172071eedb822d9de`. The inherited document was used as the supplied execution specification; it did not authorize account submissions, paid runs or messages.

## Initial immutable inputs

| Input | Expected | Observed | State |
|---|---|---|---|
| `Public main HEAD` | `9274840b6faacaa7ad0e321172071eedb822d9de` | `9274840b6faacaa7ad0e321172071eedb822d9de` | MATCH |
| `report/aimo-interp-report-v5.pdf` | `1ec9bfb0ac7e48c78ef13ae8ee78d9acdce953bd12bac1038a3bee08719194cf` | `1ec9bfb0ac7e48c78ef13ae8ee78d9acdce953bd12bac1038a3bee08719194cf` | MATCH |
| `bundles/solution-text-length-control-small.zip` | `30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd` | `30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd` | MATCH |
| `bundles/solution-always-true-small.zip` | `4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a` | `4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a` | MATCH |
| `data/train-main-v2.parquet` | `e18eb44207e7987781ec2ff214793196038442bdc1466fdf5498f3e87ec58285` | `e18eb44207e7987781ec2ff214793196038442bdc1466fdf5498f3e87ec58285` | MATCH |
| `research/PREREG_v6.json` | `cd0ee93fbb536f9de02f626164b40915eb3be7ed95b69b5b154f0fd3fed81a36` | `cd0ee93fbb536f9de02f626164b40915eb3be7ed95b69b5b154f0fd3fed81a36` | MATCH |

All 38 attached manifest entries were checked before delegation; the following table enumerates every attached hash, including the eight leaderboard pages and both supplied gates.

| Attached file | Expected SHA256 | Observed SHA256 | State |
|---|---|---|---|
| `attach/data/leaderboard/2026-10-19/comp.json` | `a512a7140918428d302e180f3d5c92af13eef94876d77d87a964d280a91a7cfc` | `a512a7140918428d302e180f3d5c92af13eef94876d77d87a964d280a91a7cfc` | MATCH |
| `attach/data/leaderboard/2026-10-19/lb1.json` | `fc7338524b81410324f3e3588aee42ff8a0bb67e5b3ad36b24a6903986d066c2` | `fc7338524b81410324f3e3588aee42ff8a0bb67e5b3ad36b24a6903986d066c2` | MATCH |
| `attach/data/leaderboard/2026-10-19/lb2.json` | `7fcb939214bfb1e673975cf1f3f9de100a074ba5c459da067af90ccc2ef1a4cd` | `7fcb939214bfb1e673975cf1f3f9de100a074ba5c459da067af90ccc2ef1a4cd` | MATCH |
| `attach/data/leaderboard/2026-10-19/lb3.json` | `ac33b9f4cd4e1e626f19a71b397d5a1a8a756f3fd78ef37e91c7477568a705df` | `ac33b9f4cd4e1e626f19a71b397d5a1a8a756f3fd78ef37e91c7477568a705df` | MATCH |
| `attach/data/leaderboard/2026-10-19/lb4.json` | `22331c134be761029c5adefe18a08620f5a8ee84c70a6e4ca205779307abdc1e` | `22331c134be761029c5adefe18a08620f5a8ee84c70a6e4ca205779307abdc1e` | MATCH |
| `attach/data/leaderboard/2026-10-19/lb5.json` | `89822694e89aaa4c5743ee2a84113b97386dbfa9a2ae13dc090a72df35b382a4` | `89822694e89aaa4c5743ee2a84113b97386dbfa9a2ae13dc090a72df35b382a4` | MATCH |
| `attach/data/leaderboard/2026-10-19/lb6.json` | `cc94df6dcee715c110332b8df677e917151501cbeb76fec21cdcd4448c34043e` | `cc94df6dcee715c110332b8df677e917151501cbeb76fec21cdcd4448c34043e` | MATCH |
| `attach/data/leaderboard/2026-10-19/lb7.json` | `e909516e2644adca80b744d2a10a88b788fbf6b7bce2a96be8e3e921d8765464` | `e909516e2644adca80b744d2a10a88b788fbf6b7bce2a96be8e3e921d8765464` | MATCH |
| `attach/data/leaderboard/2026-10-19/lb8.json` | `fa507d52739648f820ecb253f6ab1c5f1f6d08a2415d609628d2ad61fb1bea9f` | `fa507d52739648f820ecb253f6ab1c5f1f6d08a2415d609628d2ad61fb1bea9f` | MATCH |
| `attach/evidence/MEASURED.md` | `4d76554c487054de392fdeeae74b758566f49e06b0e0750df9a65789867283af` | `4d76554c487054de392fdeeae74b758566f49e06b0e0750df9a65789867283af` | MATCH |
| `attach/evidence/SOLUTION.json` | `15b73ae541d4b0cf3beae154cfdb694f6475d182e12e279c36103e66098af51f` | `15b73ae541d4b0cf3beae154cfdb694f6475d182e12e279c36103e66098af51f` | MATCH |
| `attach/evidence/SWEEP.json` | `691401a3b6191248076cad7b57debd0aa1b4a4e91060fbed744aa57126028563` | `691401a3b6191248076cad7b57debd0aa1b4a4e91060fbed744aa57126028563` | MATCH |
| `attach/evidence/SWEEP_REPORT.md` | `f84be373bd6372b141c88bf3d60e1b61f3346e3ed2a8c58db86f5ed9b5472116` | `f84be373bd6372b141c88bf3d60e1b61f3346e3ed2a8c58db86f5ed9b5472116` | MATCH |
| `attach/evidence/independent_audit/a1.py` | `46df4f7671b45cf6c278853ab9ccea57055a0574687442fb4c95a26335c01f1a` | `46df4f7671b45cf6c278853ab9ccea57055a0574687442fb4c95a26335c01f1a` | MATCH |
| `attach/evidence/independent_audit/a2.py` | `781baa3972776ae1a651f2d16d196b8c18154050314f99e6c9e397fbdbce6edf` | `781baa3972776ae1a651f2d16d196b8c18154050314f99e6c9e397fbdbce6edf` | MATCH |
| `attach/evidence/independent_audit/a3.py` | `744a37f7fa64b14b0466e1f01dde5119a8913577f84ade874e01bf024956422b` | `744a37f7fa64b14b0466e1f01dde5119a8913577f84ade874e01bf024956422b` | MATCH |
| `attach/evidence/independent_audit/a4.py` | `286b48d9f9448ed13236d6480ae73f96fdbdd7c6248823465daa142db09b3470` | `286b48d9f9448ed13236d6480ae73f96fdbdd7c6248823465daa142db09b3470` | MATCH |
| `attach/evidence/independent_audit/rows.json` | `2a05d8f403a5aa75604d2fd08d1ed4cfd46882b97661dfef44f885722ccd248d` | `2a05d8f403a5aa75604d2fd08d1ed4cfd46882b97661dfef44f885722ccd248d` | MATCH |
| `attach/evidence/independent_audit/subs.json` | `f0f21f530be954a220766fb8aaec9402396d838a20aca3a53027eac87539a27e` | `f0f21f530be954a220766fb8aaec9402396d838a20aca3a53027eac87539a27e` | MATCH |
| `attach/evidence/m2_leaderboard.json` | `f4b8a695aaaad70460ee0d314192c76efff225164407ac5f4b6b0a4cbd12ac79` | `f4b8a695aaaad70460ee0d314192c76efff225164407ac5f4b6b0a4cbd12ac79` | MATCH |
| `attach/evidence/m3_control.json` | `7f1bdccd3c12abd7125c178e8f577cce26436f4ff22f4715318325088c5716b4` | `7f1bdccd3c12abd7125c178e8f577cce26436f4ff22f4715318325088c5716b4` | MATCH |
| `attach/evidence/m4_owner_adjusted.json` | `29f1b633aea4c4b0fd3a89d4026130707bab809e2a4ec0b0b9ea482200942f5b` | `29f1b633aea4c4b0fd3a89d4026130707bab809e2a4ec0b0b9ea482200942f5b` | MATCH |
| `attach/research/PREREG_v6.json` | `cd0ee93fbb536f9de02f626164b40915eb3be7ed95b69b5b154f0fd3fed81a36` | `cd0ee93fbb536f9de02f626164b40915eb3be7ed95b69b5b154f0fd3fed81a36` | MATCH |
| `attach/tests/fx_badsha.json` | `d0c55179b917fd86d7d6dc093480e2eb6e6a2f8bde49ddfc7e515374cca48bc4` | `d0c55179b917fd86d7d6dc093480e2eb6e6a2f8bde49ddfc7e515374cca48bc4` | MATCH |
| `attach/tests/fx_early.json` | `37b72149e1b793f259facc7d1aa69566afba0ca325505a59eb309b35cd41fa82` | `37b72149e1b793f259facc7d1aa69566afba0ca325505a59eb309b35cd41fa82` | MATCH |
| `attach/tests/fx_match.json` | `9252b4c06e5dd796a53763f34afe0a2addfbc78c3bcb15e28615f80fd4eea9b6` | `9252b4c06e5dd796a53763f34afe0a2addfbc78c3bcb15e28615f80fd4eea9b6` | MATCH |
| `attach/tests/fx_mismatch.json` | `79171847c4fa0f88595b7ccac620a044b303bbb85263fa37f5f49d2bb0986329` | `79171847c4fa0f88595b7ccac620a044b303bbb85263fa37f5f49d2bb0986329` | MATCH |
| `attach/tests/fx_missing.json` | `1fd26fc6d9fc27bb3fe73faa4580768fc0c6221efc8311485b7d6d01809cae73` | `1fd26fc6d9fc27bb3fe73faa4580768fc0c6221efc8311485b7d6d01809cae73` | MATCH |
| `attach/tests/out_badsha.json` | `c189db124d0f0c70874b2eaca85a095bbd918e05a590ac4328205bc16a7d24bc` | `c189db124d0f0c70874b2eaca85a095bbd918e05a590ac4328205bc16a7d24bc` | MATCH |
| `attach/tests/out_early.json` | `c8fe0e04174a8a559cf37f26c58bd078573d79338fee74ff5bba1fd7f5977fc6` | `c8fe0e04174a8a559cf37f26c58bd078573d79338fee74ff5bba1fd7f5977fc6` | MATCH |
| `attach/tests/out_match.json` | `54cc5bf217d225b60e69218170f85636fb61c78c208d30e8d3b938a7b9bf3817` | `54cc5bf217d225b60e69218170f85636fb61c78c208d30e8d3b938a7b9bf3817` | MATCH |
| `attach/tests/out_mismatch.json` | `4a430647cb0b8fcbf9db60f93b21f9187ec9728e9e863e6ed55b0e39f8891d49` | `4a430647cb0b8fcbf9db60f93b21f9187ec9728e9e863e6ed55b0e39f8891d49` | MATCH |
| `attach/tests/out_missing.json` | `370e38273865cfc391dac1ebc3ce6e965ea6599d56aa7bbf4c5e5fa3a03cb716` | `370e38273865cfc391dac1ebc3ce6e965ea6599d56aa7bbf4c5e5fa3a03cb716` | MATCH |
| `attach/tools/m2_leaderboard.py` | `7f8756f2f03cb96ead3346940a3de690f3bacdaee0498470291c299a0413865c` | `7f8756f2f03cb96ead3346940a3de690f3bacdaee0498470291c299a0413865c` | MATCH |
| `attach/tools/m3_control.py` | `f3ad21750ac6a577f009b049102bb8e3c4aa82f578f8c08b1149dab3bb059bfc` | `f3ad21750ac6a577f009b049102bb8e3c4aa82f578f8c08b1149dab3bb059bfc` | MATCH |
| `attach/tools/m4_owner_adjusted.py` | `15d86a948609dd7555661898ffcaa6d08366a515e7bf39a68e58acd97757db29` | `15d86a948609dd7555661898ffcaa6d08366a515e7bf39a68e58acd97757db29` | MATCH |
| `attach/tools/prereg_codabench_gate.py` | `07b09da4e05af061f3457268e0ac10e0a45b2bdd28484477345fad8337ff1d9d` | `07b09da4e05af061f3457268e0ac10e0a45b2bdd28484477345fad8337ff1d9d` | MATCH |
| `attach/tools/submission_text_gate.py` | `030bfa77ad2c9b1bfb1fda8e7c026a574f6feb98ed6f84daa0bd453f11c772d2` | `030bfa77ad2c9b1bfb1fda8e7c026a574f6feb98ed6f84daa0bd453f11c772d2` | MATCH |

## Frozen identifiability values

| Key | Expected | Observed | State |
|---|---:|---:|---|
| `lb_small_items` | 14 | 14 | MATCH |
| `lb_main_items` | 21 | 21 | MATCH |
| `lb_small_owners_scored` | 61 | 61 | MATCH |
| `lb_main_owners_scored` | 41 | 41 | MATCH |
| `lb_small_bh_survivors` | 2 | 2 | MATCH |
| `lb_main_bh_survivors` | 1 | 1 | MATCH |
| `lb_small_bonferroni_survivors` | 2 | 2 | MATCH |
| `lb_main_bonferroni_survivors` | 1 | 1 | MATCH |
| `lb_small_next_padj` | 0.0319 | 0.0319 | MATCH |
| `lb_main_next_padj` | 0.0214 | 0.0214 | MATCH |
| `power_n80_first_acc060` | 158 | 158 | MATCH |
| `power_n80_sustained_acc060` | 169 | 169 | MATCH |
| `power_n80_first_acc065` | 69 | 69 | MATCH |
| `power_n80_sustained_acc065` | 76 | 76 | MATCH |
| `power_at_14_acc060` | 0.12 | 0.12 | MATCH |
| `power_at_14_acc065` | 0.22 | 0.22 | MATCH |
| `power_at_21_acc060` | 0.2 | 0.2 | MATCH |
| `power_at_21_acc065` | 0.36 | 0.36 | MATCH |
| `train_small_rows` | 43 | 43 | MATCH |
| `train_small_problems` | 22 | 22 | MATCH |
| `train_small_multi_model_problems` | 11 | 11 | MATCH |
| `train_small_mixed` | 0 | 0 | MATCH |

The 22 checks include every required value plus both Bonferroni counts. A more conservative within-owner union bound followed by across-owner Bonferroni also retains 2 Small and 1 Main owners. All inferential statements remain conditional on valid binomial item p-values and the stated family/stopping assumptions. Minimum compatible score denominators are not independently confirmed evaluator item counts. Non-rejection does not prove chance accuracy or method equivalence; these are not paired ranking tests.

## Optional transfer values

| Historical calculation | Expected | Observed | State |
|---|---:|---:|---|
| `rows` | 393 | 393 | MATCH |
| `problems` | 150 | 150 | MATCH |
| `problems_with_gt1_label` | 145 | 145 | MATCH |
| `problems_mixed_labels` | 44 | 44 | MATCH |
| `control_lopo_bacc` | 0.5462 | 0.5462 | MATCH |
| `control_lopo_acc` | 0.4682 | 0.4682 | MATCH |
| `bootstrap.bacc_ci95.low` | 0.4689 | 0.4689 | MATCH |
| `bootstrap.bacc_ci95.high` | 0.6167 | 0.6167 | MATCH |
| `oracle_acc_on_exactly_balanced_rows` | 0.5 | 0.5 | MATCH |
| `control_acc_on_exactly_balanced_rows` | 0.5 | 0.5 | MATCH |

The third-party raw self-label file is not redistributed. Its pinned MIT LICENSE and content hash were checked. This historical pool includes problems the prior authors later excluded as leakage-prone; the optional aggregate is therefore omitted from the scientific manuscript and mandatory V1–V6. See research/v6_sources/OPTIONAL_TRANSFER.md.

## Gates, report and limits

Local full CPU checks passed before the final statistical wording correction; `local-final-source-gates.json` then verified changed final Markdown, both TeX sources and provenance byte parity. The definitive integrated receipt is the public fresh-clone run in PUBLICATION.md. Frozen fixture exits were match 0, mismatch 0 (REFUTED_OR_PARTIAL), badsha 1, early 1, missing 1. These are synthetic fixtures and no live receipt was created.

The frozen receipt gate overstates what two aggregate matching scores establish. Its bytes and registration are preserved; a separate conservative wrapper permits only recorded score statements and always forbids per-problem balance inference. Deadline expiry lifts the local rendering block, never measurement status. Owner results remain UNMEASURED.

| Variant | Pages | Type-3 fonts | PDF SHA256 |
|---|---:|---:|---|
| named | 9 | 0 | `6114f15549c07c12efce021a6521d0d72d20c53adc46079d3a4bba9558eef9ef` |
| anonymous | 9 | 0 | `f1d2a4df94c1669c6f0e2e3dc67c7dda6324b51b8ccc83b28a95a77d79d88ebb` |

Both final variants were rendered and all pages visually inspected. Embedded NeurIPS style bytes and base typography are unchanged; page growth from v5 five pages to v6 nine pages is the predeclared content expansion. The original v5 PDF and both ZIPs remain byte-identical. See report/REGEN_FIDELITY_v6.md and results/v6/protected_inputs.json.

## Build-input accounting and unrun work

Every changed code/manifest/registration/report source and fixture is listed with before/after byte counts in BUILD_INPUT_CHANGES_v6.md and full hashes in results/v6/build_input_changes.json. Requirements and original dataset fetcher changed by zero bytes. The host default Python 3.10 could not satisfy existing pins; the successful environment uses Python 3.13. Initial direct network source probes encountered CA/DNS errors, then immutable public Git retrieval verified the prior report and MIT LICENSE. No failed probe was represented as source content.

Not run: any new language-model inference, paid GPU, white-box method or ablation; owner account uploads, private-val/final-test evaluation, nomination, Discord announcement inspection, OpenReview final form/submission or receipt; October 31 rescrape and its future kill-rule result. The exact final report hour/timezone and anonymity policy remain unverified, so both author variants are retained. No scientific negative effect is inferred from unrun work. New GPU jobs: 0. New paid-service spend: USD 0.

## Completion-audit corrections

The full inherited handoff audit found and corrected: omitted comp.json metadata (all9 attached snapshotJSON now copied and hashed); missing exact public label rules; a receipt scope that was only reported rather than enforced at rendering; and an incomplete fixed-family qualification in usage documentation. The renderer now selects a protected UNMEASURED fallback only for the marked owner paragraph when receipts are absent/invalid, even after deadline expiry. Seven new synthetic scope tests pass and are integrated into V6. Current local full receipt: results/v6/completion-cpu-gates.json. Numeric outputs and both bundles remain unchanged. The rebuilt report remains8body+1referencespages per variant. Full-goal completion remains unproven while T4 and T5 are pending; see COMPLETION_AUDIT_v6.md.

Corrected public reproduction now passes at scientific/build HEAD `524cc98816b2cd31bafd7c4e4e25f66a093e2cf5`, including all 9 snapshot files and the 7 new scoped rendering cases. Actual new-clone/new-venv/network download and full V1–V6 stdout are in results/v6/publication/. This supersedes initial public receipts for current report/code bytes; owner evidence and October 31 execution remain incomplete.
