# v5 current primary-source verification

Checked 2026-10-19. This directory is a read-only public-source evidence cache. No competition submission, report submission, external message, paid job, or publication was made. Raw HTTP bodies, URL, status, UTC retrieval time, byte count, and SHA256 are in `raw_manifest.json`; `SOURCE_MANIFEST.md` provides a compact integrity table. HTML-to-text and section extracts are derivatives, not separately fetched sources.

## Authority resolution

Ruling target: Which current rules, label definitions, baseline protocols, and related-work overlaps may the v5 report assert?

Candidate layers: Codabench competition terms/configuration; current official website rules and FAQ; current/pinned getting-started README and solution-specific documentation; organizer GitHub issue replies; original competition proposal; dataset card; eventual report-submission portal and Discord instructions.

The Codabench terms explicitly direct rule readers to the website. The website FAQ identifies the website as the current rule reference, getting-started as interface/environment authority, and proposal as background; when specifics differ, the website and repository are current. Competition-phase sources must be distinguished from warmup sources and old public samples. The train-main-v2 card governs its public train labels; it does not publish the hidden label implementation.

Current getting-started `main` resolves to `de794053debe75a711400696e66b60937cebbb1b`. Pinned/main top-level READMEs are byte-identical. Pinned/main uncertainty-profiling READMEs are byte-identical. Pinned/main train-main-v2 cards are byte-identical. These are current checks, not assumptions from the previous audit.

**Grades:** All statements below are raw-verified documentary statements unless explicitly marked otherwise. Competitor measurements are the authors' reported results, not independently rerun experiments. Discord, authenticated report form, and OpenReview upload instructions were not inspected; their state is unverified.

## Report, evaluation, and review requirements

| Statement supported by raw sources | Governing source | Limits / consequence |
|---|---|---|
| Negative-result and measurement-audit reports are eligible for writeup consideration. | [Organizer reply, issue 10, 2026-09-21](https://github.com/aimo-interp/getting-started/issues/10#issuecomment-5765789797) | Eligibility is not acceptance or prize selection. |
| A Codabench submission is not required for writeup eligibility; the same reply expects public train, private validation, and test evaluations through Codabench. | [Same organizer reply](https://github.com/aimo-interp/getting-started/issues/10#issuecomment-5765789797) | Preserve both clauses. No validation/test measurements exist merely because the report is eligible. A limitation paragraph does not itself waive the stated evaluation expectation. |
| Technical reports must document the submission and open implementation; instructions must permit score reproduction, including training data, training code, and bundle. | [Current official rules](https://aimo-interp.github.io/#rules) (`website.html`, lines 1627–1629) | A build-only check does not establish score reproduction. |
| Reports are due by November 15, 2026; the published report window is November 1–15. Award-considered teams commit to review up to three reports during November 15–30, 2026. | [Current official rules/timeline](https://aimo-interp.github.io/) | No exact report deadline time zone or hour was established from these sources. Do not invent an AoE/UTC/KST cutoff. |
| The organizer described an approximately nine-page NeurIPS format, submission through OpenReview, and full disclosure of AI assistance; at that date no official template was available. | [Organizer reply, 2026-09-21](https://github.com/aimo-interp/getting-started/issues/10#issuecomment-5765789797) | This is a tentative format clarification, not inspected final portal instructions. Preparing a NeurIPS draft within nine pages is reasonable; final portal/page-count details remain unverified. |
| Final-test runs require nominations and are not automatic carry-forwards; instructions were to be announced on Discord. | [Organizer reply, 2026-10-02](https://github.com/aimo-interp/getting-started/issues/10#issuecomment-5960678018) | Owner nomination status and current Discord directions were not inspected. |
| Competition phase closes 2026-11-01 11:55 UTC (20:55 KST). | [Current Codabench competition API](https://www.codabench.org/api/competitions/16180/), phase 30038 `end` | API configuration is current; report deadline is separate. |
| Public leaderboard results are provisional; final evaluation uses new, unpublished problems. | [Current official standings notice](https://aimo-interp.github.io/) | Neither public-train cross-validation nor a public sample establishes hidden generalization. |

Owner verification needed before submission: open the organizers' current report-submission announcement and actual OpenReview form, read the final page limit, anonymity/author rules, artifact URL requirements, file rules, exact time-zone cutoff, AI disclosure field, and final-test nomination procedure; preserve the actual form/receipt. No options or final portal URLs were inferred from another venue.

## Labels and baseline protocols

The public train-main-v2 card gives this exact rule on labelled rows:

```
is_robust = true  iff max_drop <= 0.10
is_robust = false iff max_drop >= 0.25
```

[Pinned card](https://huggingface.co/datasets/aimo-interp/train-main-v2/blob/fa8af758c6519fc97a9d0bd9017feb6f12232b52/README.md) states 94 rows, 36 problems, 59 robust, 21 nonrobust, and 14 unlabelled; train labelled prevalence is about 74%, whereas validation is close to balanced. Its `license: other` field does not establish unrestricted parquet redistribution. Linking HF IDs and recording data hashes avoids making an unsupported license claim.

The current official FAQ says hidden robustness uses every applied perturbation, with a clearly degraded perturbation sufficient for nonrobustness; its exact criterion is not published. Therefore the train card thresholds can be quoted as the public train rule and must not be presented as an independently verified private scoring implementation.

The [pinned top-level README](https://github.com/aimo-interp/getting-started/blob/de794053debe75a711400696e66b60937cebbb1b/README.md) lists the four Small checkpoints and gpt-oss-120b for Main. It states `:low` sample names and closed-API model names are not passed in the Competition phase. Public-sample and aggregate-corpus audits are useful caveats, but they are not measured competition cases.

[Proposal section 1.6](https://arxiv.org/html/2607.13899#S1.SS6) reports sample-validation stratified ten-fold accuracy up to 58.37 (±7.5) for the probe and 69.23% (±10.13) for the uncertainty classifier. These are paper-reported sample results, not a matched evaluation against this report's Small train LOPO control. Do not mix their plain accuracy with a balanced-accuracy claim.

The [pinned uncertainty README](https://github.com/aimo-interp/getting-started/blob/de794053debe75a711400696e66b60937cebbb1b/solutions/uncertainty-profiling/README.md) describes a separate legacy aggregate-data artifact using problem-grouped five-fold `StratifiedGroupKFold`, model/threshold selection by out-of-fold balanced accuracy, and a Random Forest artifact with balanced accuracy 0.6262, plain accuracy 0.6879, MAE 0.3429, threshold 0.5760. Its training data is augmented-sample-math-agg pinned at f972ced0705096f8d7ca7fac30825900b8b7fb6a. Its cohort and selection protocol differ from the public train-main-v2 control; the numbers provide context, not evidence of a head-to-head win.

## Verified related-work overlap

Repository pins were resolved using current GitHub commit APIs; source text was then fetched at immutable SHA URLs. These are sources about their authors' work, not organizer policy. No novelty or exhaustive competitor-absence claim is made.

| Author / current pin | Verified overlap | Source and qualification |
|---|---|---|
| Haeyoung Park (`byeolki`), `3b678f62432dda6e2c3124b670fc4bcaed9453ab` | Already observes same-problem label concordance and warns a shared prompt probe may read problem difficulty; gives a surface-feature control. | [Experiment results](https://github.com/byeolki/aimo-interp/blob/3b678f62432dda6e2c3124b670fc4bcaed9453ab/experiments/01-layer-probe/RESULTS.md), lines 66–70: its older cohort has 34 official Small rows and nine multi-model problems with no differing labels. [Report abstract and section 2](https://github.com/byeolki/aimo-interp/blob/3b678f62432dda6e2c3124b670fc4bcaed9453ab/report/report.html) repeat the concern and report validation results. Its 34-row/nine-group cohort must not be merged with the current 43-labelled-row/eleven-group computation. |
| `coderdailyone`, `48643c30e7a01cabd63f337711e79d962c7f8826` | Already tries problem-text features, reports local balanced accuracy about 0.69, and weak public leaderboard transfer. | [README](https://github.com/coderdailyone/aimo-interp-challenge/blob/48643c30e7a01cabd63f337711e79d962c7f8826/README.md) and [PLAN lines 99–120](https://github.com/coderdailyone/aimo-interp-challenge/blob/48643c30e7a01cabd63f337711e79d962c7f8826/PLAN.md): text CV 0.694, reported submission 914154, result 8/19 compared with constant 10/19. This is the author's recorded legacy MATH-to-AIMO attempt, not a current matched private-val comparison. |
| XUHANG REN (`renxuhangrt-dotcom`), `e527debcfc1b4b92c3e25b529bf196a17a84b417` | Already reports pre-registered hidden-state probe stress tests, private evaluation, and OOD collapse. | [README](https://github.com/renxuhangrt-dotcom/aimo-interp-probe-stress-tests/blob/e527debcfc1b4b92c3e25b529bf196a17a84b417/README.md), [E10 result JSON](https://github.com/renxuhangrt-dotcom/aimo-interp-probe-stress-tests/blob/e527debcfc1b4b92c3e25b529bf196a17a84b417/outputs/aimo_v6_gpu_ready/validation_e10_ood_small/validation_result.json), and [preregistration](https://github.com/renxuhangrt-dotcom/aimo-interp-probe-stress-tests/blob/e527debcfc1b4b92c3e25b529bf196a17a84b417/outputs/aimo_v6_gpu_ready/E10_PREREGISTRATION.md): 10 selected public sample problems, accuracy 0.20 versus always-false 0.80, balanced accuracy 0.50. Labels are derived from legacy sample max-decay, not current private labels. We verified the raw reported artifacts, not GPU replay. |
| Issue 10 participant (Ou YangKuang) | Already describes a negative-results measurement audit and an experiment stopped after a preregistered power review. | [Original issue](https://github.com/aimo-interp/getting-started/issues/10). Organizer confirms eligibility; this does not establish that the participant's report was selected or accepted. |

Suggested bounded related-work sentence: Park reports same-problem label concordance on an earlier official Small cohort; coderdailyone reports text-feature cross-validation that failed to transfer to leaderboard cases; Ren reports a preregistered public-sample OOD failure. The present report quantifies its pinned cohort and supplies model-free controls, with hidden validation/test left unmeasured until native receipts exist.

## Conflicts and authority-preserving resolutions

1. **Proposal versus current labels/runtime.** Proposal background and legacy sample rules differ from current website/train card/interface. Preserve each source's dataset/phase; current website/repository govern operational claims. Public train card rules remain scoped to that data.
2. **Nine pages versus older one–two-page proposal.** The later organizer reply tentatively describes nine pages. Final submission-system instructions were not inspected, so neither is a verified final portal limit.
3. **Cache availability conflict remains.** Current top-level README and site list cached checkpoints, whereas [organizer issue 11 reply](https://github.com/aimo-interp/getting-started/issues/11#issuecomment-6241088781) says nothing is cached while allowing custom models/probes/weights. This unresolved worker-availability claim does not affect a model-free bundle.
4. **Top-level interface versus uncertainty subdirectory.** Current top-level README says sample aliases are never passed; the unchanged uncertainty README still documents the legacy qwen3-8b:low alias. Treat the latter as artifact provenance, not current namespace authority.
5. **Competitor Discord claims versus inspected sources.** Park's result note attributes per-problem/model balancing to Discord. That layer was not inspected. The current train card says near-balanced validation overall; this does not independently prove per-problem balancing.
6. **Handoff overstatement.** HANDOFF_v5's competitor-absence sentence and SWEEP4's description of another report as approved/covering the same thesis are not independently established. Use specific overlap citations and eligibility wording; do not repeat those stronger claims.

## Measurement hygiene

No exhaustive source-absence claim was needed. The only bounded token check is recorded in `token_checks.json`: counts for `OpenReview`, `template`, and `nine-page` in the fetched official website, with `Report`, `Reviewing`, and `November` controls. A zero here means only that those tokens are absent from that fetched page, not that no final announcement or submission form exists. Current Discord and final OpenReview form remain **not investigated**, not absent.

Prior records inspected first: full HANDOFF_v5, source-authority-gate, SWEEP4/sweep4 report from the v5 ZIP, existing `research/live_audit/FACT_STATUS.md`, issue bodies, raw source manifest, and TRAIN_CHALLENGERS_REVIEW. Memory registry query for AIMO/Interpretability/competitor names returned no relevant hit and supplied no factual premise.
