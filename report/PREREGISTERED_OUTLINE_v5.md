# Robustness labels in AIMO-Interp are mostly problem identity: required problem-only controls for interpretability claims

## 1. Claim
On the competition models' public training labels, problem identity explains {{r2_problem_train_multi}} of the variance in max accuracy drop across {{r2_problem_train_multi_rows}} multi-model rows, and every multi-model problem among the Small-track rows carries one label ({{conc_train_small_only.concordant}} of {{conc_train_small_only.multi}}; {{conc_train_small_only.expected_independent}} expected under independence). The effect survives without dropping the ambiguous 0.10-0.25 band ({{conc_train_nogap_p10.concordant}} of {{conc_train_nogap_p10.multi}}; {{conc_train_nogap_p10.expected_independent}} expected).

## 2. Consequence: a problem-only control
A two-feature problem-text control (log length, digit count) reaches leave-one-problem-out balanced accuracy {{control_lopo_small_bacc}} on the {{small_rows}} Small rows ({{small_problems}} problems), against an organizer-reported prefill probe at 58.37 percent accuracy (different rows; not a head-to-head).

## 3. Does it survive unseen problems?
Trained on train-main-v2 and applied to other organizer sets it falls to {{control_transfer_train_to_agg_bacc}} and {{control_transfer_train_to_val_bacc}}. Codabench private-val rows for the control and always-true: [CODABENCH ROWS — owner uploads].

## 4. Label construction caveats (unscored public samples)
On the public 141-row sample, labels are fixed by row format ({{agg_format_crosstab.list_rows_robust}} list rows robust, {{agg_format_crosstab.string_rows_nonrobust}} string rows non-robust; format flag {{agg_format_flag_bacc}}, majority {{agg_majority_acc}}). These samples are never scored (README), so this is a caveat for baselines trained on them, not a test-set claim.

## 5. What we tried outside the competition data (negative)
External difficulty, self-generated labels, public generation dumps — see kill log; numbers to be keyed before inclusion.

## 6. Recommendation
Report every interpretability method against problem-only controls under problem-grouped CV, with plain and balanced accuracy.
