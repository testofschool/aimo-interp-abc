# Can a small validation leaderboard rank robustness predictors? Identifiability limits in AIMO-Interp

## Abstract

On the frozen AIMO-Interp public validation board (14 Small and 21 Main items, inferred from the score grid), no score below perfect is separable from the independent fair-coin null after per-owner selection and across-owner Benjamini–Hochberg correction: 59 of 61 Small owners and 40 of 41 Main owners are not rejected, including an owner with a 12/14 Small result. The snapshot predates the organizers' 21 October removal of two perfect-score submissions attributed to iterative profiling of problems and labels. [S13] We do not identify which owners were affected. Our hash-pinned analysis adjusts each owner's best visible score for its number of scored submissions under an independent-submission model. Only perfect observed owner results reject the declared null; non-rejection leaves chance performance, method equivalence and pairwise ranking unresolved. A single pre-specified predictor needs at least 76 independent correctness items at true accuracy 0.65, or 169 at 0.6, to sustain power 0.8 at level 0.05 before selection correction. We offer this as a design target for future validation boards, not as a statement about the unpublished final set. Paired, problem-clustered method comparisons need separate sizing. A supporting public-label audit finds no mixed labels among 11 Small problems with multiple checkpoints. We provide CPU reproduction rather than additional model runs. Both reference baselines were scored once each through the organizers' temporary evaluation queue during the Codabench outage [S13]; these runs are not on the leaderboard. The always-robust rule scored 7/14 (submission id bde5e370-4dba-4f19-8291-4a998bfecdcd, 2026-10-24 19:01:28 KST) and the length-and-digit control scored 7/14 (submission id 0c736e59-8248-4dee-8e4f-2df037c552d7, 2026-10-24 19:03:37 KST); each equals the fair-coin expectation and is not separable from it under the declared null.

## 1. Task and the evidence a leaderboard supplies

The AIMO Interpretability Challenge asks whether a model will answer a mathematical problem robustly under meaning-preserving perturbations. A predictor receives a problem and access to a specified model, then produces a binary robustness decision. The Small track uses a fixed set of open checkpoints; Main adds a larger checkpoint with multiple reasoning-effort configurations. The scored outcome is plain accuracy on held-out problem–model instances. A leaderboard is therefore an evaluation instrument for generalization to those instances, while an interpretability claim also needs evidence about what signal a method uses. A high development score and a model-specific explanation are separate claims. [S1, S2, S3, S12]

The public dataset card says that the validation set is close to balanced. On 9 October, the organizers warned that several highly ranking submissions relied on balanced labels and called this overfitting. That warning motivates examining a fair-coin reference; it does not establish exact balance within each problem or model. An earlier public technical report makes the stronger per-problem and per-model balance claim, which remains attributed to that report. The organizer website says that the exact private evaluation criterion is unpublished. Binomial calibration requires the separate independence assumptions declared below. [S1, S2, S7, S13]

The organizers have stated that validation-board problems are absent from final evaluation, which will use unpublished AIMO sets. [S13] Our question is whether this frozen validation board can separate plausible improvements in accuracy from score variation and repeated selection under the declared model. A board with few items can still detect an extreme outcome. It can simultaneously have little power for a useful but moderate improvement, especially when owners can try several methods and retain the best score. The relevant unit for the selection adjustment is the owner within each track, rather than each displayed score row. Neither an isolated significant owner nor a collection of non-significant owners is itself an ordering of methods.

Our main contribution is an executable, snapshot-specific assessment of that evidential limit. We specify how the score grid is reconstructed, how invalid predictions and duplicate rows enter the denominator, how an owner's best visible result is adjusted, and what sample size detects stated effects under the same null. We then connect this result to a supporting label audit: a training set dominated by problem identity cannot by itself teach the contrast that a balanced per-problem test is designed to measure. That latter observation overlaps prior public work and remains supporting context rather than our lead novelty claim. For organizers and later evaluations of robustness predictors, the single-predictor planning rule is at least 76 independent correctness items for true accuracy 0.65 (169 for 0.6), sustaining power 0.8 at level 0.05 against the fair-coin reference before any selection correction. Method comparisons should use paired, problem-clustered outcomes and be sized separately. We offer this as a design target for future validation boards, not as a statement about the unpublished final set.

## 2. A conditional analysis of the visible leaderboard

### Snapshot, units and score reconstruction

We freeze the public private-validation leaderboard snapshot dated October 19, 2026, fetched on October 20 KST. The reproduction package stores the raw JSON pages, their hashes and the immutable analysis inputs. Snapshot date means the dated archive used for this calculation, not that every submitted run occurred on that date. The analysis refuses to compute after a snapshot hash mismatch. This avoids quietly replacing a published denominator when the online board changes. [S10]

The integer item counts are inferred from the score grid. For each track, the parser searches for the smallest item count compatible with the displayed accuracy and coverage after rounding, together with the integer invalid-prediction count. It represents a scored submission by its integer number of correct items divided by that denominator, counting invalid predictions as wrong. The smallest compatible counts are 14 and 21. This finite-grid assumption is explicit: the chosen unweighted integer score model and smallest-fit rule cannot reveal undocumented weighting or resampling. The exact item counts should ultimately be confirmed by the evaluator's item-level scoring contract.

The parser de-duplicates repeated score rows before counting submissions. A submission scored on both tasks contributes once to each relevant track. An observed submission has conflicting score sets; the declared resolution uses its zero-coverage set. Zero-coverage rows remain part of the parsing record but do not enter owner counts or the distribution of scored best results. This resolution does not change the reported survivor counts. The analysis uses owner identifiers only to group submissions; participant handles remain confined to the hashed raw snapshot.

After these rules, Small contains 249 scored submissions from 61 owners and Main contains 132 from 41. The units matter: a repeated row is not a new attempt, while several distinct submissions by one owner create a selection opportunity. A method may change between submissions, so the owner-level result describes the best visible outcome selected from that owner's attempts. It does not estimate the accuracy of a stable, pre-specified algorithm.

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

We apply the Benjamini–Hochberg step-up rule separately within Small and Main at false-discovery-rate target 0.05. Sorting the adjusted p-values across the M scored owners, the rule finds the largest rank r satisfying the threshold below and rejects ranks 1 through r. Bonferroni at level 0.05 is reported as a sensitivity check. [S11]

$$
p_{\mathrm{adj},(r)}\leq q\,r/M.
$$

The conventional false-discovery-rate guarantee requires valid owner p-values and suitable dependence conditions, such as independent owners. Public methods can share code, data, observations and leaderboard feedback. We do not observe those dependencies. Bonferroni avoids the across-owner dependence requirement when its input p-values are valid, but still inherits the binomial item model and the independent-submission adjustment. Equal counts under the two corrections are useful sensitivity evidence within this model; they do not remove its assumptions.

### Results and the later removal announcement

| Track | Inferred items | Scored owners | BH survivors | Bonferroni survivors | Perfect-score owners |
|---|---:|---:|---:|---:|---:|
| Small | 14 | 61 | 2 | 2 | 2 |
| Main | 21 | 41 | 1 | 1 | 1 |

Only 2 Small owners and 1 Main owners survive either correction, and each has a perfect observed score. A further sensitivity replaces the within-owner adjustment by the union bound, min(1, m p), followed by across-owner Bonferroni. It gives 2 Small and 1 Main survivors. For a fixed family of attempts and owners with valid single-submission binomial p-values, this bound allows arbitrary dependence among attempts and among owners. With score-adaptive stopping, the observed-count result is descriptive unless p-value validity holds conditional on the observed family and counts. The next Small owner has 12/14 correct across 5 scored submissions, with independent-submission adjusted tail probability 0.0319. The next Main owner has 17/21 across 6 submissions, with adjusted tail probability 0.0214. These next-best results fail the across-owner rule despite looking strong as raw accuracy fractions.

The snapshot predates the organizers' 21 October announcement that they removed two perfect-score submissions attributed to iterative profiling of problems and labels. Affected owners remain unidentified: the supplied announcement omits submission IDs linking those removals to this frozen snapshot. On 16 October, the organizers had announced automatic re-evaluation of top submissions under a per-problem protocol. These announcements supply context rather than evidence about the cause or validity of a particular frozen score. [S13] A perfect score is extreme under this null; model-internal signals, leakage avoidance and generalization each require separate evidence.

Conversely, a non-rejected owner may have useful accuracy. Low power, multiplicity and a small number of visible trials can all prevent rejection. The survivor count measures visible owners separated from the stated reference under this analysis; counting valid methods or ordering predictors requires additional evidence. Ranking two predictors requires paired item outcomes, an estimand for their accuracy difference, and uncertainty accounting for selection. Aggregate best scores leave those ingredients unresolved.

## 3. Exact power and an item-budget design target

### Single-submission planning calculation

We first plan for a single pre-specified submission without owner selection or an across-owner correction. For each candidate sample size N, the rejection threshold c(N) is the smallest integer correct count whose exact fair-coin upper tail is at most 0.05. Under an alternative accuracy a with independent items, power is the probability of reaching that count:

$$
c(N)=\min\{k:p(k,N)\leq\alpha\},\qquad
\pi(N,a)=\Pr_{K\sim\operatorname{Bin}(N,a)}\{K\geq c(N)\}.
$$

When every attainable upper-tail probability exceeds the level constraint, power is zero. Using the exact integer threshold preserves the conservative behavior of a discrete test. It also makes power non-monotone in N near the target: adding an item sometimes increases the required correct count. A normal approximation or a single first-crossing value hides this sawtooth behavior.

| Grid | Rejection count | Actual null rejection probability | Power at accuracy 0.6 | Power at accuracy 0.65 |
|---|---:|---:|---:|---:|
| Small, N = 14 | 11 | 0.0287 | 0.12 | 0.22 |
| Main, N = 21 | 15 | 0.0392 | 0.2 | 0.36 |

At true accuracy 0.6, the single-submission test has power 0.12 on the Small grid and 0.2 on Main. At 0.65, these rise to 0.22 and 0.36. These probabilities describe repeated independent evaluations under the model; submission-specific confidence levels require a separate calculation. They explain why a moderate gain can remain unresolved on a tiny leaderboard even before correcting a best-of-many search.

### First crossing and sustained power

We report both the first N reaching target power 0.8 and the first N after which every larger sample size stays at or above that target. The latter is a more robust planning recommendation. The executable search certifies the sustained threshold by exact enumeration followed by an analytic tail bound for all larger N, rather than treating a finite search horizon as proof of a permanent crossing.

| True accuracy | First N with target power | Sustained N with target power |
|---|---:|---:|
| 0.6 | 158 | 169 |
| 0.65 | 69 | 76 |

The first crossings are 69–158 items for the stated alternatives. We recommend the sustained values, at least 76 items to detect accuracy 0.65 or 169 to detect 0.6, under independent-item planning. A nearby larger sample should not be assumed adequate from the first crossing alone. The released tool computes exact power at each candidate sample size and records the threshold certification, so the calculation can be inspected without reinterpreting rounded table entries.

These are lower-complexity planning scenarios than the observed leaderboard analysis. They test one method against a fixed reference; they do not guarantee power after owner selection, false-discovery correction, pairwise comparisons or model development on validation feedback. A final evaluation that chooses among many methods must allocate its error budget to that selection process or reserve an untouched confirmation set. We offer this as a design target for future validation boards, not as a statement about the unpublished final set or a universal minimum for ranking a field.

### Evaluation design implications

A useful next evaluation would preserve the problem as a grouping unit and release enough item-level outcomes to distinguish within-problem model contrasts from between-problem difficulty. If several instances share one problem, adding model configurations can add less independent information than adding new problems. The item budgets above assume independent correctness indicators; positive within-problem correlation would generally reduce effective information. A design should state the number of problems, the number of model instances per problem, balance constraints, invalid-prediction handling and any weighting before treating a nominal row count as its statistical sample size.

For method comparison, a paired analysis is preferable to subtracting independent accuracy estimates, because predictors face the same instances. The evaluator can report which methods disagree and evaluate their paired accuracy difference while preserving problem clusters. Reference baselines (a constant rule and a surface-feature control) provide contextual comparisons under the actual private scoring protocol. Paired differences require item-level outcomes. Finally, leaderboard feedback should be limited or separated from a final holdout so that iteration does not silently consume the confirmation set.

The final-test size is unpublished in the sources we inspected. We therefore make no claim that the eventual final ranking has the same limitations as this visible validation snapshot. A larger, well-designed final set could resolve differences that the public board cannot. The recommendation is to publish its effective evaluation units and uncertainty, rather than infer its adequacy from the validation grid.

## Limitations and sensitivity directions

The strongest limitation is calibration. Our binomial null assumes independent items with the same correctness probability. Shared problems, models and perturbations can create dependence; exact balance can itself constrain the outcome distribution of particular rules. The inferred denominators also rely on the smallest compatible unweighted score grid. We report these assumptions at the point of the main result because a small p-value under a convenient null is not an unconditional validation of a predictor.

Selection and multiplicity introduce three dependence sensitivities. Within an owner, closely related submissions can be positively correlated: fewer effective opportunities can make the independent-submission adjustment too large and reduce rejections; negative dependence can make it too small relative to the union event. Score-adaptive development and stopping can invalidate a fixed-trial model or a correction based on realized attempts. The union-bound sensitivity needs a fixed family or p-value validity conditional on the family and counts. Aggregate scores leave effective attempts and stopping rules unidentified, so the release exposes the unadjusted tail, visible m and adjusted tail. Counting only visible scored submissions gives a conditional upper bound on survivors when the observed best score and independent-submission null are fixed: additional hidden attempts increase the adjusted tail. Unknown dependence, missing owners, an unseen higher best score or null misspecification defeat that bound. Across owners, shared solutions and public discoveries can correlate outcomes. Bonferroni permits arbitrary across-owner dependence among valid owner p-values, while still inheriting within-owner calibration assumptions. The matching count is a sensitivity result rather than a causal measurement of overfitting or a diagnosis of individual submissions.

The snapshot is finite and time-specific. New submissions, scoring changes, owner visibility or an altered evaluator can change the result. Both reference baselines were scored once each through the organizers' temporary evaluation queue during the Codabench outage [S13]; these runs are not on the leaderboard. The always-robust rule scored 7/14 (submission id bde5e370-4dba-4f19-8291-4a998bfecdcd, 2026-10-24 19:01:28 KST) and the length-and-digit control scored 7/14 (submission id 0c736e59-8248-4dee-8e4f-2df037c552d7, 2026-10-24 19:03:37 KST); each equals the fair-coin expectation and is not separable from it under the declared null. The report has no final-test outcomes. Public-training concordance, sample metadata associations and reported participant experiences provide context for evaluation cautions. A prior text-control report and a prior probe stress test discuss weaker public performance under distribution shift, which supplies context rather than a matched comparison to our analysis. [S8, S9]

Finally, the item recommendations concern single-method power for a one-sided test against the fair-coin reference at the stated effects and target. Pairwise ranking, small accuracy gaps, correlated outcomes, multiple comparisons and repeated validation feedback can require more data or a different design. Chance equivalence for non-rejected methods, differences among survivors and agreement with the final ordering each require their own evidence.

## AI Use Statement

We used AI assistance for **Ideation** (screening hypotheses and research directions, literature and prior-report search, and summarizing sources), **Coding** (writing and running CPU reproduction and analysis scripts, gates and fetchers), **Analysis** (deriving and cross-checking reported statistics and independently recomputing the leaderboard analysis), and **Writing** (drafting and editing the report text and structure). The tools were Anthropic Claude and OpenAI Codex, including independent AI agents used for cross-checks. AI was not used to create or alter the source leaderboard or robustness labels, to fabricate measurements, or to write peer reviews. AI-assisted code computed the reported statistics from the released source data; those derived computations are distinguished from source observations. The author has reviewed all AI-assisted work and takes full responsibility for the final content, including AI-assisted text, claims, code, reported statistics and other artifacts.

## Source index

- **S1:** AIMO organizers. Official competition website, rules and FAQ. [Competition description](https://aimo-interp.github.io/).
- **S2:** AIMO organizers. `train-main-v2` dataset card, immutable revision fa8af758c6519fc97a9d0bd9017feb6f12232b52. [Label rules and validation description](https://huggingface.co/datasets/aimo-interp/train-main-v2/blob/fa8af758c6519fc97a9d0bd9017feb6f12232b52/README.md).
- **S3:** AIMO organizers. Getting-started README, immutable commit de794053debe75a711400696e66b60937cebbb1b. [Interface and sample scope](https://github.com/aimo-interp/getting-started/blob/de794053debe75a711400696e66b60937cebbb1b/README.md).
- **S5:** AIMO organizers. Uncertainty baseline README, immutable commit de794053debe75a711400696e66b60937cebbb1b. [Sample evaluation protocol](https://github.com/aimo-interp/getting-started/blob/de794053debe75a711400696e66b60937cebbb1b/solutions/uncertainty-profiling/README.md).
- **S7:** Prompt Probes Read Solve Rate, Not Robustness: Negative Results from the AIMO Interpretability Challenge. Public report, October 18, 2026; immutable source commit 3b678f62432dda6e2c3124b670fc4bcaed9453ab. Prior problem-level label agreement, reported evaluation balance and constant-rule result. Exact source location is preserved in the research evidence manifest.
- **S8:** Earlier public AIMO-Interp text-control report. Immutable source commit 48643c30e7a01cabd63f337711e79d962c7f8826. Text cross-validation and public-score comparison. Exact source location is preserved in the research evidence manifest.
- **S9:** Earlier public AIMO-Interp probe stress-test report. Immutable source commit e527debcfc1b4b92c3e25b529bf196a17a84b417. Distribution-shift study. Exact source location is preserved in the research evidence manifest.
- **S10:** Codabench. AIMO-Interp public private-validation leaderboard, frozen dated snapshot October 19, 2026; fetched October 20, 2026. [Public leaderboard API](https://www.codabench.org/api/phases/30038/get_leaderboard/). Hashed JSON pages and parser provenance accompany the reproduction archive: https://github.com/testofschool/aimo-interp-abc.
- **S11:** Yoav Benjamini and Yosef Hochberg. Controlling the false discovery rate: a practical and powerful approach to multiple testing. Journal of the Royal Statistical Society, Series B, 1995. [Original article](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).

- **S12:** Michal Štefánik, Philipp Mondorf, Andreas Waldis, Qianying Liu, Chuan Yang, Michal Spiegel, Josef Kuchar, Marek Kadlčík, Adam Vawda-Oomerjee, Chaoran Liu, Simon Frieder, Barbara Plank, Fazl Barez and Pontus Stenetorp. AIMO Interpretability Challenge. CoRR, abs/2607.13899, 2026. Organizer-specified proposal citation, matching arXiv v1. [Challenge proposal, version cited](https://arxiv.org/abs/2607.13899v1).
- **S13:** AIMO-Interp organizers (M. Štefánik, A. Waldis, M. Spiegel). Discord #announcements. Supplied transcript received October 24, 2026; absolute message dates include 9, 16 and 21 October, while later posts retain relative timestamps. The 24 October temporary-evaluation-queue notice is documented in the supplied v8.3 handoff; the recorded queue responses accompany the archive. Original bytes, source hash and date-provenance notes accompany the evidence manifest in the reproduction archive.

## Appendix A. Supporting label audit and problem-only controls

### Training agreement does not identify model contrasts

The pinned training table has 94 rows over 36 problems, with 80 labelled rows and 14 rows in an unlabelled gap. The dataset card states the labelled-row rule verbatim:

`is_robust = true`  iff `max_drop <= 0.10`

`is_robust = false` iff `max_drop >= 0.25`

This public rule does not specify the private-label procedure. The labelled Small subset contains 43 rows over 22 problems. Among its 11 problems represented by multiple checkpoints, 0 have mixed binary labels. Thus the observed training labels supply no within-problem label contrast for that repeated-checkpoint cohort. [S2]

An earlier public report already identifies problem-level shortcuts and reports exact per-problem balance in validation and test. Under exact within-problem balance, any deterministic problem-only predictor that gives the same binary answer for all model instances of a problem has accuracy exactly 0.5 on that problem, and therefore overall under equal item scoring. This follows by counting correct positive and negative instances, regardless of how the predictor learned its problem-level answer. The conclusion is conditional on that balance contract and same-answer behavior; it is not a proof that every text-based system is incapable of generalization. [S7]

The two frozen bundles are reference baselines (a constant rule and a surface-feature control).

Both reference baselines were scored once each through the organizers' temporary evaluation queue during the Codabench outage [S13]; these runs are not on the leaderboard. The always-robust rule scored 7/14 (submission id bde5e370-4dba-4f19-8291-4a998bfecdcd, 2026-10-24 19:01:28 KST) and the length-and-digit control scored 7/14 (submission id 0c736e59-8248-4dee-8e4f-2df037c552d7, 2026-10-24 19:03:37 KST); each equals the fair-coin expectation and is not separable from it under the declared null. Final-test performance of these bundles is also UNMEASURED. This owner-result limitation is separate from our observed analysis of the public board.

The recorded queue receipt JSONs accompany the reproduction archive.

### Descriptive drop variance and label concordance

For continuous maximum drop, we compute one minus within-problem squared error divided by total squared error, using each observed problem mean to estimate its residuals. This in-sample R-squared describes the public panel rather than cross-validated prediction. Unlabelled rows are retained where continuous drops are present. Repeated configurations include effort variants of the same model checkpoint.

| Public panel | Rows or pairs | Problems | Descriptive R-squared |
|---|---:|---:|---:|
| Train, repeated configurations | 76 | 18 | 0.7822 |
| Train, multi-checkpoint problems | 70 | 15 | 0.7369 |
| Small, distinct checkpoints | 39 | 14 | 0.7811 |
| Public sample-full configurations | 80 | 10 | 0.1813 |

The repeated-configuration training cohort includes 3 problems represented only by effort variants of the same larger checkpoint. The multi-checkpoint sensitivity retains those effort rows where other checkpoints are also present. For sample-full, we take the maximum recorded family drop per model/configuration–problem pair. Aliases, decoding configurations, problem panels and perturbation coverage differ across public panels. The large contrast in R-squared therefore limits a universal problem-property interpretation without constituting a controlled generalization experiment.

| Label agreement panel | Concordant / repeated groups | Independent-Bernoulli reference count |
|---|---:|---:|
| Train, original labelled configurations | 15 / 16 | 5.94 |
| Train, labelled Small checkpoints | 11 / 11 | 4.89 |
| Train, no-gap sensitivity, worst effort | 10 / 15 | 3.59 |
| Sample-full, public-rule proxy labels | 1 / 10 | 0.25 |

A group is concordant when all included binary labels agree. The reference count sums the probabilities of all-positive or all-negative labels at each observed group size under independent Bernoulli draws at pooled prevalence. This descriptive reference leaves significance testing to a separately justified model. The no-gap sensitivity labels every training row by the lower public threshold, then collapses the larger checkpoint's effort variants by the minimum binary label. Both the cohort and collapse rule change. The sample proxy uses the public threshold band rather than private competition labels. These distinctions confine the table to the observed public panels.

### A weak control with appropriately wide uncertainty

The control uses log-one-plus character length and digit count of the original problem. Class-balanced logistic regression is fitted on all labelled Main-table rows, excluding every row with the held-out problem string in each leave-one-problem-out fold. Evaluation uses only labelled Small rows. The fixed decision threshold is 0.5, using fixed hyperparameters and only these problem-text features.

| Public Small out-of-fold rule | Plain accuracy | Balanced accuracy | Correct rows |
|---|---:|---:|---:|
| Length and digit count | 0.7674 | 0.6855 | 33 / 43 |
| Always robust | 0.7209 | 0.5 | 31 / 43 |

Holding out whole problems prevents the same problem string from entering both sides of a fold, including effort variants. The absence of mixed labels and the difference from private test composition remain limitations. We hold the out-of-fold predictions fixed and bootstrap the 22 problem clusters, drawing the same number of clusters with replacement using seed 0 for 4000 replicates. One-class draws are discarded, leaving 4000 valid draws. The balanced-accuracy 95% interval is [0.4759, 0.9378]; the plain-accuracy interval is [0.5556, 0.9556]. The paired balanced-accuracy improvement over always robust is 0.1855, with interval [-0.0241, 0.4378], including zero. These intervals omit retraining and method-selection variation.

Applying the fitted training control unchanged to public samples yields balanced accuracy 0.4913 on the aggregate sample and 0.5409 on the original validation sample rows. Different configurations, label conventions and possible problem overlap leave disjoint-problem transfer unverified. In the aggregate sample, the formatting of a perturbation-description field perfectly associates with the observed label: a field-format flag has accuracy 1.0. That flag uses perturbation metadata outside the original problem-only feature set. Establishing interpretability or private-task performance requires evaluation beyond this unscored sample panel. [S3, S5]

## Appendix B. Reproduction and assistance

The release supplies a hash-pinned CPU pipeline rather than additional model runs, with frozen reference baselines (a constant rule and a surface-feature control). The public reproduction repository is https://github.com/testofschool/aimo-interp-abc. The v8.1 manuscript source base is `6f81bc3b31472dfeb1179b25c31fd7bb128dd19f`; the build provenance records subsequent text-only corrections. It verifies the leaderboard snapshot and parquet inputs before computing; registers measured values in a claims ledger; renders every reported measurement through checked numeric keys; and builds both author variants from one Markdown manuscript using the unchanged official NeurIPS style. The leaderboard tool records denominator fits, parsing resolutions, owner counts, corrected tails, exact power at the current grids and the sustained-threshold certification. The reproduction gates also test missing, early, mismatched and bad-hash receipt fixtures without treating them as real submissions.

The archive includes immutable dataset revisions, file hashes and a downloader. It does not redistribute third-party labelled data with unresolved licence terms. A separate publication record contains clean-clone checks, source/PDF hashes, page counts and render review. Those records establish what was executed and which artifacts can be rebuilt; compilation alone does not validate the assumptions of the statistical model. The raw leaderboard retains source identifiers for auditability, while the scientific report discusses aggregated owner counts and neutral source titles.

The practical result is a reproducible evidential boundary: under a declared calibration model, the visible validation grid separates only perfect observed outcomes after selection and multiplicity, and has low single-method power for the stated moderate effects. A larger confirmation set, item-level paired outcomes and explicit grouping/balance rules would make the board more informative about robustness predictors and about the interpretability claims attached to them.
