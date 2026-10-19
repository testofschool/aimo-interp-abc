# Problem-only controls for robustness prediction in AIMO-Interp

## Abstract

We audit public labels used to develop robustness predictors for the AIMO Interpretability Challenge. On the competition-checkpoint training data, a descriptive problem-mean decomposition accounts for 0.7822 of observed maximum-drop variance across 76 repeated-configuration rows. Among labelled Small-track problems represented by multiple checkpoints, 11/11 have concordant labels. A problem-only logistic control using log character length and digit count achieves leave-one-problem-out balanced accuracy 0.6855 and plain accuracy 0.7674, with wide problem-clustered intervals. These observations motivate explicit problem-only controls; they establish neither a model-internal signal nor performance on unseen private competition problems. Public sample panels show different associations and weak control transfer. Private-validation and final-test results remain unmeasured. We provide a hash-pinned CPU reproduction package and distinguish observed calculations, contextual baseline reports, and experiments that were not executed.

## 1. Task, data, and scope

The challenge asks whether a model answers a mathematical problem robustly under meaning-preserving perturbations. Its Small track evaluates Qwen3.5-4B, Skywork-OR1-Math-7B, Olmo-3-7B-Think, and DeepSeek-R1-0528-Qwen3-8B; the Main track adds gpt-oss-120b with several reasoning efforts. Competition ranking uses plain accuracy on held-out problem-model instances. We also report balanced accuracy because prevalence differs across public panels. [S1, S2]

The pinned `train-main-v2` table has 94 rows over 36 problems, including 80 labelled rows over 33 problems and 14 unlabelled rows. Our public Small evaluation cohort is 43 labelled rows over 22 problems, with 31 robust and 12 non-robust labels. This is public training data, not the private scoring set. The dataset card states the labelled-row rule verbatim:

`is_robust = true` iff `max_drop <= 0.10`

`is_robust = false` iff `max_drop >= 0.25`

The intervening band carries null labels. This public rule does not disclose the private-label procedure: the current website says the exact evaluation criterion is unpublished. Public samples contain additional configurations and closed API models. The starter README says low-suffixed sample names and closed API models are never passed during the Competition phase; sample findings below are development caveats. [S1, S2, S3]

## 2. Problem identity and observed label agreement

Our descriptive R-squared is one minus within-problem squared error divided by total squared error, using the same rows to estimate each problem mean and its residuals. This is an in-sample decomposition, not cross-validated prediction. Unlabelled rows are included because their continuous drops are observed. The registered repeated-configuration cohort has 76 rows over 18 problems; 3 of these problems have only gpt-oss effort variants. Calling all of them multi-model would be inaccurate.

| Observed panel | Rows or pairs | Problems | Descriptive R-squared |
|---|---:|---:|---:|
| Train, repeated configurations | 76 | 18 | 0.7822 |
| Train, multi-checkpoint problems | 70 | 15 | 0.7369 |
| Small only, distinct checkpoints | 39 | 14 | 0.7811 |
| Public sample-full configurations | 80 | 10 | 0.1813 |

The multi-checkpoint training sensitivity retains effort configurations as separate rows. Sample-full has 8 model/configuration identifiers; we take the maximum recorded family drop per identifier-problem pair. Some underlying checkpoints overlap with competition checkpoints, while aliases, decoding configurations, problem panels, and perturbation coverage differ. This contrast limits a universal problem-property interpretation but is not a controlled generalization test.

| Label agreement analysis | Concordant / repeated groups | Bernoulli reference |
|---|---:|---:|
| Train, original labelled configurations | 15 / 16 | 5.94 |
| Train, labelled Small checkpoints | 11 / 11 | 4.89 |
| Train, no-gap sensitivity, worst effort | 10 / 15 | 3.59 |
| Sample-full, proxy labels | 1 / 10 | 0.25 |

A group is concordant when all included binary labels agree. The reference sums the probability of all-positive or all-negative labels at each observed group size, assuming independent Bernoulli draws at pooled panel prevalence. It is not a p-value. The no-gap sensitivity labels every training row robust iff its drop is at most 0.10, then collapses gpt-oss efforts by minimum label. Any non-robust effort makes that checkpoint non-robust. Both cohort and collapse rule change; this is not identical agreement under the original labels. Sample-full proxy labels use the public threshold band and are not private competition labels.

Raw `val-sample` agreement is 1/6; removing duplicate model-problem pairs changes it to 0/5. Duplicate configurations can change the apparent number of repeated groups.

## 3. A problem-only control and its uncertainty

Features are log-one-plus character length and digit count of the original problem. Class-balanced logistic regression with default regularization and a fixed convergence limit is fitted using the 80 labelled Main-table rows. Each leave-one-problem-out fold excludes every row with the held-out problem string, including gpt-oss efforts. We score only the 43 labelled Small rows: pooled-checkpoint training, Small-only evaluation. The threshold is 0.5. There is no hyperparameter search or model-internal input.

| Public Small OOF predictor | Plain accuracy | Balanced accuracy | Correct rows |
|---|---:|---:|---:|
| Length and digit count | 0.7674 | 0.6855 | 33 / 43 |
| Always robust | 0.7209 | 0.5 | 31 / 43 |

The control correctly classifies 27 robust and 6 non-robust rows; its plain-accuracy improvement is small in case count. We hold OOF predictions fixed, sort the 22 problem strings, and draw that many clusters with replacement using NumPy `default_rng`, seed 0, for 4000 replicates. All rows of each selected problem travel together. We discard one-class draws; 4000 remain. Endpoints use linear-interpolated percentiles.

The 95% interval is [0.4759, 0.9378] for balanced accuracy and [0.5556, 0.9556] for plain accuracy. The paired balanced-accuracy difference from always robust is 0.1855, with interval [-0.0241, 0.4378], including zero. These intervals omit variability from retraining and method selection. They are not a formal power analysis. The inherited power note lacked executable bootstrap code; this explicit reconstruction supersedes its interval for this draft.

For context, the organizer proposal reports prefill-probe plain accuracy 58.37 percent and generation-uncertainty plain accuracy 69.23 percent under a different sample protocol. The starter uncertainty artifact separately reports balanced accuracy 0.6262 and plain accuracy 0.6879. These are not matched Small-cohort comparisons; our results do not establish that the text control matches or beats a probe. [S4, S5]

## 4. Transfer and the missing private evaluation

Fitting the control on all labelled training rows and applying it unchanged to public samples gives the following results. Samples contain different models and label conventions. Problem content can overlap across panels, so this is not a verified disjoint-problem evaluation.

| Public destination | Rows | Plain accuracy | Balanced accuracy |
|---|---:|---:|---:|
| Augmented aggregate sample | 141 | 0.2695 | 0.4913 |
| Val sample, original rows | 28 | 0.5357 | 0.5409 |

Private-validation results for the frozen Small control and always-robust Small bundle are UNMEASURED. No owner screenshot, timestamp, or bundle-to-submission linkage is available for these two methods. An account name or unrelated leaderboard score cannot identify a bundle. Final-test performance is also UNMEASURED. We make no claim that the control survives unseen competition problems. This limits the technical draft: organizer guidance requests public-train and private Codabench evaluation while saying a Codabench entry is not required for writeup-prize eligibility. [S6]

## 5. Unscored sample-panel caveats

The 141-row aggregate sample has 36 robust list-formatted rows and 105 non-robust string-formatted rows, with no opposite-label cases. A flag for whether `permutation_type` starts with an opening bracket achieves balanced and plain accuracy 1.0; majority-label plain accuracy is 0.7447. This is perfect observed association, not evidence of a causal construction mechanism. That field is not the original problem-only input available to a deployed control.

On these rows, five-fold `StratifiedGroupKFold` grouped by problem ID gives the text control mean balanced accuracy 0.6754 and mean plain accuracy 0.6865 across ten seeds; balanced accuracy ranges from 0.6159 to 0.6996. Dataset and splitter family match the organizer artifact; actual folds and full pipeline are not claimed identical. Format and majority rules show why this comparison cannot alone establish interpretability. These sample configurations are not scored competition inputs. [S3, S5]

## 6. External attempts and overlapping public work

Inherited screening considered external mathematical difficulty, self-generated perturbation labels, and public generation dumps. These were planning decisions, not completed target-checkpoint experiments in this run. The packet lacks executable Omni-MATH predictions and a fully specified Monte Carlo label-noise simulation; we omit their quantitative claims. A difficulty proxy need not predict perturbation sensitivity, and synthetic-label agreement cannot be assumed from sample count alone.

One diagnostic is reproducible: on 24 deduplicated val-sample pairs, observed unperturbed accuracy has AUROC 0.7333 for the robust label; 8 of 15 non-robust pairs have perfect observed base accuracy. This uses organizer outcome metadata, not deployable problem-only features, on public sample configurations. No external source was validated here as replacement target-label data. No new white-box experiment or ablation was run; that absence is not evidence that white-box signals have no effect.

Public participants already discuss these risks. Byeolki reports within-problem label agreement and difficulty shortcuts on an earlier cohort. Coderdailyone reports strong text cross-validation followed by weaker public leaderboard performance. Renx reports poor probe behavior under distribution shift relative to a constant rule. We cite these overlaps without a comprehensive novelty claim. Our contribution is an explicit reproduction and sensitivity ledger for the pinned public files. [S7, S8, S9]

## 7. Reproduction, assistance, and completion checklist

Every decimal and percentage comes from a checked numeric key or sourced literal. The CPU script checks all parquet hashes before computation. The renderer verifies keys against the claims registry; standalone NeurIPS source is generated from the rendered Markdown. The release includes dataset IDs, immutable revisions, paths, hashes, and a fetcher rather than redistributing parquet with unresolved custom-license terms. A local clean clone can reproduce CPU checks after hash-verified downloads. Public-remote verification is a separate release step and remains unevidenced here.

AI assistance disclosure: Claude prepared inherited research summaries, sweep decisions, and the initial outline. OpenAI Codex expanded the draft, wrote and ran CPU reproduction code, checked public sources, and used independent AI agents to audit claims and prepare release support. No language model generated additional robustness labels for this report. Human author review remains pending; AI summaries are not experimental evidence.

Completion checklist: PDF page count, source hashes, numeric checks, and render review accompany the release artifacts. Owner actions remain: confirm author details; obtain linked Codabench rows or retain the limitation; verify the final OpenReview venue and submit by November 15, 2026; retain the receipt; and commit to reviewing up to three reports during November 15-30, 2026. Website rules govern dates and reviewing; the organizer issue gives provisional NeurIPS-format and OpenReview guidance. This draft is not a submission receipt. [S1, S6]

## Source index

- **S1:** AIMO organizers. Official competition website, rules and FAQ. [Current reference](https://aimo-interp.github.io/).
- **S2:** AIMO organizers. `train-main-v2` card, revision fa8af758c6519fc97a9d0bd9017feb6f12232b52. [Public label rules](https://huggingface.co/datasets/aimo-interp/train-main-v2/blob/fa8af758c6519fc97a9d0bd9017feb6f12232b52/README.md).
- **S3:** AIMO organizers. Starter README, commit de794053debe75a711400696e66b60937cebbb1b. [Interface and sample scope](https://github.com/aimo-interp/getting-started/blob/de794053debe75a711400696e66b60937cebbb1b/README.md).
- **S4:** AIMO organizers. Competition proposal, section 1.6. [arXiv:2607.13899](https://arxiv.org/abs/2607.13899).
- **S5:** AIMO organizers. Uncertainty baseline, commit de794053debe75a711400696e66b60937cebbb1b. [Artifact evaluation](https://github.com/aimo-interp/getting-started/blob/de794053debe75a711400696e66b60937cebbb1b/solutions/uncertainty-profiling/README.md).
- **S6:** Michal Spiegel. Organizer response, issue 10. [Scope, format, AI assistance and submission](https://github.com/aimo-interp/getting-started/issues/10#issuecomment-5765789797).
- **S7:** Byeolki. AIMO report and results, commit 3b678f62432dda6e2c3124b670fc4bcaed9453ab. [Prior label agreement](https://github.com/byeolki/aimo-interp/tree/3b678f62432dda6e2c3124b670fc4bcaed9453ab).
- **S8:** Coderdailyone. AIMO Interp Challenge, commit 48643c30e7a01cabd63f337711e79d962c7f8826. [Text control and public score](https://github.com/coderdailyone/aimo-interp-challenge/tree/48643c30e7a01cabd63f337711e79d962c7f8826).
- **S9:** Renxuhangrt. Probe Stress Tests, commit e527debcfc1b4b92c3e25b529bf196a17a84b417. [Distribution-shift study](https://github.com/renxuhangrt-dotcom/aimo-interp-probe-stress-tests/tree/e527debcfc1b4b92c3e25b529bf196a17a84b417).
