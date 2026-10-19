# Can a small validation leaderboard rank robustness predictors? Identifiability limits in AIMO-Interp

## Abstract

How much evidence does a small public leaderboard provide about robustness prediction? We analyze a hash-pinned AIMO-Interp leaderboard snapshot using its observed score grid. The smallest compatible item counts are {{lb_small_items}} for Small and {{lb_main_items}} for Main. Under an explicit independent fair-coin item null and an independent-submission model, we adjust each owner's best visible score for its number of scored submissions, then apply Benjamini–Hochberg across owners. Only {{lb_small_bh_survivors}} of {{lb_small_owners_scored}} Small owners and {{lb_main_bh_survivors}} of {{lb_main_owners_scored}} Main owners reject that conditional null; every surviving owner has a perfect score. Non-rejection does not establish chance performance, method equivalence, or a pairwise ranking. Exact one-sided binomial power at true accuracy {{power_alternative_acc060}} is {{power_at_14_acc060}} and {{power_at_21_acc060}} on the respective grids. Power first reaches {{power_target}} at {{power_n80_first_acc060}} items for accuracy {{power_alternative_acc060}} and {{power_n80_first_acc065}} for {{power_alternative_acc065}}; discreteness makes the sustained thresholds larger. We recommend at least {{power_n80_sustained_acc065}}–{{power_n80_sustained_acc060}} independent items for those stated effects before accounting for leaderboard selection. A supporting public-label audit finds no mixed labels among {{train_small_multi_model_problems}} Small problems with multiple checkpoints. We provide CPU reproduction, parsing and sensitivity contracts, and distinguish observed leaderboard statistics from unmeasured private results for our own controls.

## 1. Task and the evidence a leaderboard supplies

The AIMO Interpretability Challenge asks whether a model will answer a mathematical problem robustly under meaning-preserving perturbations. A predictor receives a problem and access to a specified model, then produces a binary robustness decision. The Small track uses a fixed set of open checkpoints; Main adds a larger checkpoint with multiple reasoning-effort configurations. The scored outcome is plain accuracy on held-out problem–model instances. A leaderboard is therefore an evaluation instrument for generalization to those instances, while an interpretability claim also needs evidence about what signal a method uses. A high development score and a model-specific explanation are separate claims. [S1, S2, S3]

The public dataset card says that the validation set is close to balanced. An earlier public technical report states that validation and test are balanced per problem and per model, and describes an always-robust result on the Small validation set. We attribute that stronger balance statement to the prior report; we do not infer exact balance from the phrase “close to balanced.” The organizer website also says that the exact private evaluation criterion is unpublished. These sources motivate a fair-coin reference, but they do not establish the independence assumptions required for a binomial test. Our statistical claims below are conditional on a declared null and scoring model. [S1, S2, S7]

The scientific question is whether the public validation board can separate plausible improvements in accuracy from score variation and repeated selection. A board with few items can still detect an extreme outcome. It can simultaneously have little power for a useful but moderate improvement, especially when owners can try several methods and retain the best score. The relevant unit for the selection adjustment is the owner within each track, rather than each displayed score row. Neither an isolated significant owner nor a collection of non-significant owners is itself an ordering of methods.

Our main contribution is an executable, snapshot-specific assessment of that evidential limit. We specify how the score grid is reconstructed, how invalid predictions and duplicate rows enter the denominator, how an owner's best visible result is adjusted, and what sample size detects stated effects under the same null. We then connect this result to a supporting label audit: a training set dominated by problem identity cannot by itself teach the contrast that a balanced per-problem test is designed to measure. That latter observation overlaps prior public work and is not our lead novelty claim. The report concerns evaluation design and uncertainty; it does not propose a new robustness predictor.

## 2. A conditional analysis of the visible leaderboard

### Snapshot, units and score reconstruction

We freeze the public private-validation leaderboard snapshot dated October 19, 2026, fetched on October 20 in Korea. The reproduction package stores the raw JSON pages, their hashes and the immutable analysis inputs. Snapshot date means the dated archive used for this calculation, not that every submitted run occurred on that date. The analysis refuses to compute after a snapshot hash mismatch. This avoids quietly replacing a published denominator when the online board changes. [S10]

The integer item counts are inferred from the score grid. For each track, the parser searches for the smallest item count compatible with the displayed accuracy and coverage after rounding, together with the integer invalid-prediction count. It represents a scored submission by its integer number of correct items divided by that denominator, counting invalid predictions as wrong. The smallest compatible counts are {{lb_small_items}} and {{lb_main_items}}. This finite-grid assumption is explicit: the chosen unweighted integer score model and smallest-fit rule cannot reveal undocumented weighting or resampling. The exact item counts should ultimately be confirmed by the evaluator's item-level scoring contract.

The parser de-duplicates repeated score rows before counting submissions. A submission scored on both tasks contributes once to each relevant track. An observed submission has conflicting score sets; the declared resolution uses its zero-coverage set. Zero-coverage rows remain part of the parsing record but do not enter owner counts or the distribution of scored best results. This resolution does not change the reported survivor counts. The analysis uses owner identifiers only to group submissions; participant handles remain confined to the hashed raw snapshot.

After these rules, Small contains {{lb_small_scored_submissions}} scored submissions from {{lb_small_owners_scored}} owners and Main contains {{lb_main_scored_submissions}} from {{lb_main_owners_scored}}. The units matter: a repeated row is not a new attempt, while several distinct submissions by one owner create a selection opportunity. A method may change between submissions, so the owner-level result describes the best visible outcome selected from that owner's attempts. It does not estimate the accuracy of a stable, pre-specified algorithm.

### Null, selection adjustment and multiplicity

For a single pre-specified submission, let K be its number of correct items among N. Our reference null makes item correctness independent with common probability one half. The one-sided exact upper-tail probability for an observed count k is

$$
p(k,N)=\Pr_{K\sim\operatorname{Bin}(N,1/2)}(K\geq k)
=\sum_{j=k}^{N}\binom{N}{j}2^{-N}.
$$

The fair-coin null is a calibration model. It is not a claim that actual submissions guess, nor a randomization test justified solely by class balance. A deterministic constant predictor under exact fixed balance, for example, has a different conditional score distribution. Correlated problem–model outcomes, unequal item difficulties or an imperfectly balanced label composition can also invalidate the binomial calibration. The analysis should therefore be read as “what this small grid can establish under this transparent reference,” rather than as unconditional evidence about the private task distribution.

For an owner with m scored submissions and best single-submission tail probability p, we compute the probability of observing at least one equally extreme result under independent, identically calibrated submission scores:

$$
p_{\mathrm{adj}}=1-(1-p)^m.
$$

This is the independent-submission selection adjustment. It grows with the number of opportunities to obtain a high score. For independent counts obeying the stated binomial null, it is exact at attainable score thresholds; with merely valid discrete p-values it is conservative. We do not fit a distribution of latent owner skill. The calculation is fully determined by the best score, the track denominator and the visible scored-submission count.

We apply the Benjamini–Hochberg step-up rule separately within Small and Main at false-discovery-rate target {{power_fdr_q}}. Sorting the adjusted p-values across the M scored owners, the rule retains the largest rank r satisfying the threshold below and rejects the preceding ranks. Bonferroni at level {{power_alpha}} is reported as a sensitivity check. [S11]

$$
p_{\mathrm{adj},(r)}\leq q\,r/M.
$$

The conventional false-discovery-rate guarantee requires valid owner p-values and suitable dependence conditions, such as independent owners. Public methods can share code, data, observations and leaderboard feedback. We do not observe those dependencies. Bonferroni avoids the across-owner dependence requirement when its input p-values are valid, but still inherits the binomial item model and the independent-submission adjustment. Equal counts under the two corrections are useful sensitivity evidence within this model; they do not remove its assumptions.

### Results and what the perfect scores establish

| Track | Inferred items | Scored owners | BH survivors | Bonferroni survivors | Perfect-score owners |
|---|---:|---:|---:|---:|---:|
| Small | {{lb_small_items}} | {{lb_small_owners_scored}} | {{lb_small_bh_survivors}} | {{lb_small_bonferroni_survivors}} | {{lb_small_perfect_owners}} |
| Main | {{lb_main_items}} | {{lb_main_owners_scored}} | {{lb_main_bh_survivors}} | {{lb_main_bonferroni_survivors}} | {{lb_main_perfect_owners}} |

Only {{lb_small_bh_survivors}} Small owners and {{lb_main_bh_survivors}} Main owners survive either correction, and each has a perfect observed score. A further sensitivity replaces the within-owner adjustment by the union bound, min(1, m p), followed by across-owner Bonferroni. It gives {{lb_small_union_bonferroni_survivors}} Small and {{lb_main_union_bonferroni_survivors}} Main survivors. For a fixed family of attempts and owners with valid single-submission binomial p-values, this bound requires no independence among attempts or among owners. With score-adaptive stopping, the observed-count result is descriptive unless p-value validity holds conditional on the observed family and counts. The next Small owner has {{lb_small_next_best_correct}}/{{lb_small_items}} correct across {{lb_small_next_submissions}} scored submissions, with independent-submission adjusted tail probability {{lb_small_next_padj}}. The next Main owner has {{lb_main_next_best_correct}}/{{lb_main_items}} across {{lb_main_next_submissions}} submissions, with adjusted tail probability {{lb_main_next_padj}}. These next-best results fail the across-owner rule despite looking strong as raw accuracy fractions.

A perfect score is an extreme event under this null regardless of the procedure that produced it. Significance therefore cannot establish that the procedure used a model-internal signal, avoided leakage, or generalizes to new problems. The snapshot records {{lb_small_perfect_organizer_rerun_submissions}} perfect Small submission through the queue named `aimo_organizer_rerun`. We report this as an observed queue label and make no inference about how that run was produced or why it used that queue. The analysis assigns no causal interpretation or accusation to a score or a queue.

Conversely, a non-rejected owner may have useful accuracy. Low power, multiplicity and a small number of visible trials can all prevent rejection. Our survivor count is neither the number of valid methods nor the number of methods better than random in the target population. It is a count of visible owners separated from the stated reference under the stated analysis. The surviving owners are also not ordered against each other by a significance test. Ranking two predictors requires their paired item outcomes, an estimand for their accuracy difference, and uncertainty accounting for selection; aggregate best scores do not supply those ingredients.

## 3. Exact power and an actionable item budget

### Single-submission planning calculation

We first plan for a single pre-specified submission without owner selection or an across-owner correction. For each candidate sample size N, the rejection threshold c(N) is the smallest integer correct count whose exact fair-coin upper tail is at most {{power_alpha}}. Under an alternative accuracy a with independent items, power is the probability of reaching that count:

$$
c(N)=\min\{k:p(k,N)\leq\alpha\},\qquad
\pi(N,a)=\Pr_{K\sim\operatorname{Bin}(N,a)}\{K\geq c(N)\}.
$$

If no count satisfies the level constraint, power is zero. Using the exact integer threshold preserves the conservative behavior of a discrete test. It also makes power non-monotone in N near the target: adding an item sometimes increases the required correct count. A normal approximation or a single first-crossing value hides this sawtooth behavior.

| Grid | Rejection count | Actual null rejection probability | Power at accuracy {{power_alternative_acc060}} | Power at accuracy {{power_alternative_acc065}} |
|---|---:|---:|---:|---:|
| Small, N = {{lb_small_items}} | {{lb_small_critical_correct}} | {{lb_small_actual_alpha}} | {{power_at_14_acc060}} | {{power_at_14_acc065}} |
| Main, N = {{lb_main_items}} | {{lb_main_critical_correct}} | {{lb_main_actual_alpha}} | {{power_at_21_acc060}} | {{power_at_21_acc065}} |

At true accuracy {{power_alternative_acc060}}, the single-submission test has power {{power_at_14_acc060}} on the Small grid and {{power_at_21_acc060}} on Main. At {{power_alternative_acc065}}, these rise to {{power_at_14_acc065}} and {{power_at_21_acc065}}. These probabilities describe repeated independent evaluations under the model; they are not confidence levels for any named submission. They explain why a moderate gain can remain unresolved on a tiny leaderboard even before correcting a best-of-many search.

### First crossing and sustained power

We report both the first N reaching target power {{power_target}} and the first N after which every larger sample size stays at or above that target. The latter is a more robust planning recommendation. The executable search certifies the sustained threshold by exact enumeration followed by an analytic tail bound for all larger N, rather than treating a finite search horizon as proof of a permanent crossing.

| True accuracy | First N with target power | Sustained N with target power |
|---|---:|---:|
| {{power_alternative_acc060}} | {{power_n80_first_acc060}} | {{power_n80_sustained_acc060}} |
| {{power_alternative_acc065}} | {{power_n80_first_acc065}} | {{power_n80_sustained_acc065}} |

The first crossings are {{power_n80_first_acc065}}–{{power_n80_first_acc060}} items for the stated alternatives. We recommend the sustained values, at least {{power_n80_sustained_acc065}} items to detect accuracy {{power_alternative_acc065}} or {{power_n80_sustained_acc060}} to detect {{power_alternative_acc060}}, under independent-item planning. A nearby larger sample should not be assumed adequate from the first crossing alone. The released tool computes exact power at each candidate sample size and records the threshold certification, so the calculation can be inspected without reinterpreting rounded table entries.

These are lower-complexity planning scenarios than the observed leaderboard analysis. They test one method against a fixed reference; they do not guarantee power after owner selection, false-discovery correction, pairwise comparisons or model development on validation feedback. A final evaluation that chooses among many methods must allocate its error budget to that selection process or reserve an untouched confirmation set. We do not turn the single-test item budget into a universal minimum for ranking a field.

### Evaluation design implications

A useful next evaluation would preserve the problem as a grouping unit and release enough item-level outcomes to distinguish within-problem model contrasts from between-problem difficulty. If several instances share one problem, adding model configurations can add less independent information than adding new problems. The item budgets above assume independent correctness indicators; positive within-problem correlation would generally reduce effective information. A design should state the number of problems, the number of model instances per problem, balance constraints, invalid-prediction handling and any weighting before treating a nominal row count as its statistical sample size.

For method comparison, a paired analysis is preferable to subtracting independent accuracy estimates, because predictors face the same instances. The evaluator can report which methods disagree and evaluate their paired accuracy difference while preserving problem clusters. A constant prediction and a problem-only control are also informative reference methods under the actual private scoring protocol. Their measured scores test practical behavior; they cannot reconstruct hidden label balance from a small aggregate score. Finally, leaderboard feedback should be limited or separated from a final holdout so that iteration does not silently consume the confirmation set.

The final-test size is unpublished in the sources we inspected. We therefore make no claim that the eventual final ranking has the same limitations as this visible validation snapshot. A larger, well-designed final set could resolve differences that the public board cannot. The recommendation is to publish its effective evaluation units and uncertainty, rather than infer its adequacy from the validation grid.

## 4. Supporting label audit and problem-only controls

### Training agreement does not identify model contrasts

The pinned training table has {{train_rows}} rows over {{train_problems}} problems, with {{train_labelled_rows}} labelled rows and {{train_unlabelled_rows}} rows in an unlabelled gap. The public rule labels an instance robust when its maximum observed drop is at most 0.10 and non-robust when it is at least 0.25. It does not specify the private-label procedure. The labelled Small subset contains {{train_small_rows}} rows over {{train_small_problems}} problems. Among its {{train_small_multi_model_problems}} problems represented by multiple checkpoints, {{train_small_mixed}} have mixed binary labels. Thus the observed training labels supply no within-problem label contrast for that repeated-checkpoint cohort. [S2]

An earlier public report already identifies problem-level shortcuts and reports exact per-problem balance in validation and test. Under exact within-problem balance, any deterministic problem-only predictor that gives the same binary answer for all model instances of a problem has accuracy exactly {{power_null_accuracy}} on that problem, and therefore overall under equal item scoring. This follows by counting correct positive and negative instances, regardless of how the predictor learned its problem-level answer. The conclusion is conditional on that balance contract and same-answer behavior; it is not a proof that every text-based system is incapable of generalization. [S7]

We retain two frozen Small bundles: a length-and-digit control and an always-robust rule. Their own private-validation results are UNMEASURED because we have no linked owner receipt recording the bundle, submission identifier, status, accuracy and time. The anticipated constant/control results are receipt expectations motivated by public evidence, not pre-registered predictions of unknown labels. Even if both receipts match those expectations, they would show consistency for those submissions rather than prove exact per-problem balance. Final-test performance of these bundles is also UNMEASURED. This owner-result limitation is separate from our observed analysis of the public board.

### Descriptive drop variance and label concordance

For continuous maximum drop, we compute one minus within-problem squared error divided by total squared error, using each observed problem mean to estimate its residuals. This in-sample R-squared describes the public panel; it is not cross-validated prediction. Unlabelled rows are retained where continuous drops are present. Repeated configurations include effort variants, so they are not all distinct model checkpoints.

| Public panel | Rows or pairs | Problems | Descriptive R-squared |
|---|---:|---:|---:|
| Train, repeated configurations | {{r2_problem_train_multi_rows}} | {{r2_problem_train_multi_problems}} | {{r2_problem_train_multi}} |
| Train, multi-checkpoint problems | {{r2_problem_train_true_multi_rows}} | {{r2_problem_train_true_multi_problems}} | {{r2_problem_train_true_multi}} |
| Small, distinct checkpoints | {{r2_problem_small_multi_rows}} | {{r2_problem_small_multi_problems}} | {{r2_problem_small_multi}} |
| Public sample-full configurations | {{r2_problem_sample_full_pairs}} | {{sample_full_problems}} | {{r2_problem_sample_full}} |

The repeated-configuration training cohort includes {{r2_problem_train_multi_single_model_problems}} problems represented only by effort variants of the same larger checkpoint. The multi-checkpoint sensitivity retains those effort rows where other checkpoints are also present. For sample-full, we take the maximum recorded family drop per model/configuration–problem pair. Aliases, decoding configurations, problem panels and perturbation coverage differ across public panels. The large contrast in R-squared therefore limits a universal problem-property interpretation without constituting a controlled generalization experiment.

| Label agreement panel | Concordant / repeated groups | Independent-Bernoulli reference count |
|---|---:|---:|
| Train, original labelled configurations | {{conc_train_all_configs.concordant}} / {{conc_train_all_configs.multi}} | {{conc_train_all_configs.expected_independent}} |
| Train, labelled Small checkpoints | {{conc_train_small_only.concordant}} / {{conc_train_small_only.multi}} | {{conc_train_small_only.expected_independent}} |
| Train, no-gap sensitivity, worst effort | {{conc_train_nogap_p10.concordant}} / {{conc_train_nogap_p10.multi}} | {{conc_train_nogap_p10.expected_independent}} |
| Sample-full, public-rule proxy labels | {{conc_sample_full_maxdrop_rule.concordant}} / {{conc_sample_full_maxdrop_rule.multi}} | {{conc_sample_full_maxdrop_rule.expected_independent}} |

A group is concordant when all included binary labels agree. The reference count sums the probabilities of all-positive or all-negative labels at each observed group size under independent Bernoulli draws at pooled prevalence. It is descriptive, not a significance test. The no-gap sensitivity labels every training row by the lower public threshold, then collapses the larger checkpoint's effort variants by the minimum binary label. Both the cohort and collapse rule change. The sample proxy uses the public threshold band and is not a private competition label. These distinctions prevent a label-concordance table from being read as evidence about unseen private outcomes.

### A weak control with appropriately wide uncertainty

The control uses log-one-plus character length and digit count of the original problem. Class-balanced logistic regression is fitted on all labelled Main-table rows, excluding every row with the held-out problem string in each leave-one-problem-out fold. Evaluation uses only labelled Small rows. The fixed decision threshold is 0.5, with no hyperparameter search or model-internal input.

| Public Small out-of-fold rule | Plain accuracy | Balanced accuracy | Correct rows |
|---|---:|---:|---:|
| Length and digit count | {{control_lopo_small_acc}} | {{control_lopo_small_bacc}} | {{control_small_correct}} / {{small_rows}} |
| Always robust | {{always_true_small_acc}} | {{always_true_small_bacc}} | {{always_true_small_correct}} / {{small_rows}} |

Holding out whole problems prevents the same problem string from entering both sides of a fold, including effort variants. It does not remedy the absence of mixed labels or reproduce the private test composition. We hold the out-of-fold predictions fixed and bootstrap the {{small_problems}} problem clusters, drawing the same number of clusters with replacement using seed {{small_bootstrap.seed}} for {{small_bootstrap.draws}} replicates. One-class draws are discarded, leaving {{small_bootstrap.valid_draws}} valid draws. The balanced-accuracy 95% interval is [{{small_bootstrap.bacc_ci95.low}}, {{small_bootstrap.bacc_ci95.high}}]; the plain-accuracy interval is [{{small_bootstrap.acc_ci95.low}}, {{small_bootstrap.acc_ci95.high}}]. The paired balanced-accuracy improvement over always robust is {{control_small_delta_bacc}}, with interval [{{small_bootstrap.delta_bacc_ci95.low}}, {{small_bootstrap.delta_bacc_ci95.high}}], including zero. These intervals omit retraining and method-selection variation.

Applying the fitted training control unchanged to public samples yields balanced accuracy {{control_transfer_train_to_agg_bacc}} on the aggregate sample and {{control_transfer_train_to_val_bacc}} on the original validation sample rows. These samples have different configurations and label conventions, with possible problem overlap, so this is not a verified disjoint-problem transfer test. In the aggregate sample, the formatting of a perturbation-description field perfectly associates with the observed label: a field-format flag has accuracy {{agg_format_flag_bacc}}. That field is not an original problem-only feature. It demonstrates why strong results on an unscored sample panel cannot alone establish actionable interpretability or private-task performance. [S3, S5]

## 5. Limitations and sensitivity directions

The strongest limitation is calibration. Our binomial null assumes independent items with the same correctness probability. Shared problems, models and perturbations can create dependence; exact balance can itself constrain the outcome distribution of particular rules. The inferred denominators also rely on the smallest compatible unweighted score grid. We report these assumptions at the point of the main result because a small p-value under a convenient null is not an unconditional validation of a predictor.

The within-owner selection adjustment assumes independent submissions. Closely related submissions are likely to be positively correlated, so they can provide fewer effective opportunities than m independent draws. Under such positive dependence the independence adjustment can be too large and reduce the number of rejections. Other dependence patterns can have a different direction; negative dependence can make it too small relative to the union event. Score-adaptive development and stopping can invalidate both a fixed-trial model and a correction using the realized number of attempts. The union-bound sensitivity also needs a fixed family or conditional validity given the family and counts; observing all attempts alone does not establish that condition. We cannot estimate effective attempts or stopping rules from aggregate scores. The release therefore exposes the unadjusted tail, visible m and adjusted tail rather than hiding this choice in a single survivor count.

Only visible scored submissions are counted. Holding the observed best score fixed and retaining the same independent-submission null, including additional hidden attempts would increase the adjusted tail and could only reduce the reported survivors. In that restricted sensitivity analysis, the visible count is an optimistic upper bound. This is not an unconditional upper bound under unknown dependence, missing owners, an unseen higher best score or a misspecified null. The two directions must be read together: unobserved attempts can strengthen the selection penalty, while redundant positively correlated attempts can weaken it.

Across-owner dependence presents an additional issue for the Benjamini–Hochberg interpretation. Shared solutions or public discoveries can correlate owner outcomes. The matching Bonferroni count is helpful because its family-wise bound allows arbitrary dependence across valid owner p-values. It does not validate the within-owner p-values. We avoid describing the adjusted analysis as a causal measurement of leaderboard overfitting or as a diagnosis of any individual submission.

The snapshot is finite and time-specific. New submissions, scoring changes, owner visibility or an altered evaluator can change the result. The report has not measured our own frozen bundles on private validation and has no final-test outcomes. Public-training concordance, sample metadata associations and reported participant experiences support evaluation cautions; they are not substitutes for those missing results. A prior text-control report and a prior probe stress test discuss weaker public performance under distribution shift, which supplies context rather than a matched comparison to our analysis. [S8, S9]

Finally, single-method power is not ranking power. The item recommendations concern a one-sided test against the fair-coin reference at the stated effects and target. Pairwise ranking, small accuracy gaps, correlated outcomes, multiple comparisons and repeated validation feedback can require more data or a different design. We have not established that a method lacking significance is equivalent to chance, that surviving methods differ from one another, or that the public board predicts the final ordering.

## 6. Reproduction and assistance

The release supplies a hash-pinned CPU pipeline rather than additional model runs. It verifies the leaderboard snapshot and parquet inputs before computing; registers measured values in a claims ledger; renders every reported measurement through checked numeric keys; and builds both author variants from one Markdown manuscript using the unchanged official NeurIPS style. The leaderboard tool records denominator fits, parsing resolutions, owner counts, corrected tails, exact power at the current grids and the sustained-threshold certification. The reproduction gates also test missing, early, mismatched and bad-hash receipt fixtures without treating them as real submissions.

The archive includes immutable dataset revisions, file hashes and a downloader. It does not redistribute third-party labelled data with unresolved licence terms. A separate publication record contains clean-clone checks, source/PDF hashes, page counts and render review. Those records establish what was executed and which artifacts can be rebuilt; compilation alone does not validate the assumptions of the statistical model. The raw leaderboard retains source identifiers for auditability, while the scientific report discusses aggregated owner counts and neutral source titles.

AI assistance disclosure: Claude prepared the inherited research summaries, planning materials and initial outline. OpenAI Codex implemented and ran CPU analyses, expanded and revised the manuscript, checked source evidence and used independent AI agents for analysis, report preparation and gates. No new robustness labels or model predictions were generated for this report. Source claims, numerical outputs and limitations are separated so that AI-generated prose is not treated as experimental evidence.

The practical result is a reproducible evidential boundary: under a declared calibration model, the visible validation grid separates only perfect observed outcomes after selection and multiplicity, and has low single-method power for the stated moderate effects. A larger confirmation set, item-level paired outcomes and explicit grouping/balance rules would make the board more informative about robustness predictors and about the interpretability claims attached to them.

## Source index

- **S1:** AIMO organizers. Official competition website, rules and FAQ. [Competition description](https://aimo-interp.github.io/).
- **S2:** AIMO organizers. `train-main-v2` dataset card, immutable revision fa8af758c6519fc97a9d0bd9017feb6f12232b52. [Label rules and validation description](https://huggingface.co/datasets/aimo-interp/train-main-v2/blob/fa8af758c6519fc97a9d0bd9017feb6f12232b52/README.md).
- **S3:** AIMO organizers. Getting-started README, immutable commit de794053debe75a711400696e66b60937cebbb1b. [Interface and sample scope](https://github.com/aimo-interp/getting-started/blob/de794053debe75a711400696e66b60937cebbb1b/README.md).
- **S5:** AIMO organizers. Uncertainty baseline README, immutable commit de794053debe75a711400696e66b60937cebbb1b. [Sample evaluation protocol](https://github.com/aimo-interp/getting-started/blob/de794053debe75a711400696e66b60937cebbb1b/solutions/uncertainty-profiling/README.md).
- **S7:** Prompt Probes Read Solve Rate, Not Robustness: Negative Results from the AIMO Interpretability Challenge. Public report, October 18, 2026; immutable source commit 3b678f62432dda6e2c3124b670fc4bcaed9453ab. Prior problem-level label agreement, reported evaluation balance and constant-rule result. Exact source location is preserved in the research evidence manifest.
- **S8:** Earlier public AIMO-Interp text-control report. Immutable source commit 48643c30e7a01cabd63f337711e79d962c7f8826. Text cross-validation and public-score comparison. Exact source location is preserved in the research evidence manifest.
- **S9:** Earlier public AIMO-Interp probe stress-test report. Immutable source commit e527debcfc1b4b92c3e25b529bf196a17a84b417. Distribution-shift study. Exact source location is preserved in the research evidence manifest.
- **S10:** Codabench. AIMO-Interp public private-validation leaderboard, frozen dated snapshot October 19, 2026; fetched October 20, 2026. [Public leaderboard API](https://www.codabench.org/api/phases/30038/get_leaderboard/). Hashed JSON pages and parser provenance accompany the reproduction archive.
- **S11:** Yoav Benjamini and Yosef Hochberg. Controlling the false discovery rate: a practical and powerful approach to multiple testing. Journal of the Royal Statistical Society, Series B, 1995. [Original article](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
