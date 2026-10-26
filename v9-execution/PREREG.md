# Pre-score protocol: organizers' trained probe versus frozen text control

**Effective preregistration time:** the Git commit time of this file, recorded by the executor before any new upload. This working document alone is not evidence of a committed preregistration. Record the actual commit hash/time separately after committing it, avoiding a self-referential hash. The commit must precede bundle 3's new official submission and result. If a prior official probe result was already seen or that condition is violated, label the comparison exploratory; do not backdate it or upload a duplicate to manufacture a clean timeline.

## Scope fixed before scores

Competition 16180, official Small Model Track, task 36241. The expected score-grid contract is 14 equally weighted binary correctness items. Verify the actual scoring contract and denominators from native metadata/outputs before inference. If the new official board does not support this contract, record the mismatch and do not reinterpret a rounded percentage as a known 14-item denominator.

The immutable candidates are:

1. Always-robust rule: `solution-always-true-small.zip`, SHA-256 `4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a`.
2. Length-and-digit text control: `solution-text-length-control-small.zip`, SHA-256 `30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd`.
3. **The organizers' trained probe, unmodified**, from getting-started commit `de794053debe75a711400696e66b60937cebbb1b`. Its final ZIP hash and member inventory are recorded in `ZIPS.json` before upload; the probe artifact must have SHA-256 `8607478c7408922a6490adb7bda34d6a7d95403b7aa62f80dd3f2649139ccdeb` and size 54,729,307 bytes.

Bundles 1–2 already have known temporary-queue observations of 7/14 each. These are prior information, not new official Codabench results. The expected official 7/14 values are expectations, not measurement inputs. No official probe outcome is used to choose the test, feature set, pairing rule, threshold, or reporting direction. Never tune against these scores. Submit each prepared immutable ZIP at most once through the authorized official path; check existing submissions first. Report failures and mismatches as well as successes. H0 authorizes bundle 3 only after Felix says `v9 진행`; local packaging does not authorize its upload.

## Original request and operational clarification

The handoff asks for “probe (3) vs text control (2), paired exact McNemar on per-item predictions if Codabench exposes them, else an exact two-sided binomial comparison of the two accuracies; α = 0.05,” followed by a paired-item 80% power calculation.

**Pre-score clarification:** the two methods face the same board, so two accuracy totals are not two known-independent binomial samples. We will not silently use an unpaired independent-sample model. The following fixed paired reference and aggregate-only bounds make the requested exact-binomial fallback explicit. This is a clarification made before results, not a post-score test selection. The original single-predictor fair-coin planning code is not a paired method-comparison power calculator and will not be reused as one.

## One primary comparison, two-sided α = 0.05

The only confirmatory comparison is bundle 3 versus bundle 2 on the same scoring items. Bundle 1 and fair-coin tails are contextual secondary observations, not additional confirmatory tests. Let `b` be probe-only correct items and `c` control-only correct items. Under the declared conditional symmetry reference,

`B | (b+c=m) ~ Binomial(m, 1/2)`.

Use the exact symmetric two-sided p-value

`p = min(1, 2 * sum_{j=0}^{min(b,c)} choose(m,j) / 2^m)`;

when `m=0`, use `p=1`. Reject this reference only if `p <= 0.05`. Always report the direction and size `(b-c)/N`, the two totals, `b,c,m`, the exact p-value, and the result whether favorable, null, or unfavorable. This is an iid matched-item calibration; shared problems/models can violate it. With only this tiny board, no unconditional population/generalization or cluster-robust guarantee is claimed.

### Pairing route, in fixed order

1. Prefer native per-item correctness paired on stable item IDs. Require exactly the same complete item set, no duplicate/ambiguous IDs, the same score contract, and consistency with the two recorded aggregate counts. Do not align unknown output schemas or item order by guesswork.
2. If only the two methods' **valid binary predictions** are available, paired correctness discordance totals can still be recovered without private gold labels. Require matched unique stable IDs, full coverage for both, zero invalid predictions, and independently confirmed unweighted accuracy against the same binary labels. Let `m` be the number of prediction disagreements and `d=k3-k2` the difference of the validated correct counts. Then `b=(m+d)/2`, `c=(m-d)/2`. Check nonnegative integer parity and the whole 2×2 table's feasibility. Never reconstruct or publish individual private labels. If any contract condition is missing, do not use this route.
3. If only totals `k3,k2,N` are available, enumerate all feasible binary joint tables: both-correct `a` ranges from `max(0,k3+k2-N)` to `min(k3,k2)`, with `b=k3-a`, `c=k2-a`, and both-wrong `N-a-b-c`. Report the exact conditional p-value **range** `[p_min,p_max]` and every feasible aggregate table. It is sharp within that unrestricted binary-pairing set. It is not an unpaired test or recovered item outcomes. A conservative rejection is permitted only if **all** feasible pairings reject (`p_max <= 0.05`). If the range crosses α, report that the conclusion depends on unobserved pairing. If none reject, report only that no feasible pairing rejects this reference. Never replace that statement by equivalence, “black-box suffices,” or “matches.”

Do not fetch protected evaluation labels to repair missing pairing. Native prediction/receipt files can stay local with source hashes; publish only permitted aggregate results, not private problem text, labels, or credentials.

## Secondary paired power: explicit joint model, not two totals

If the joint correctness counts are actually identified, report an **exploratory plug-in design calculation** using `p10=b/N`, `p01=c/N` under iid pairs. With `q=p10+p01`, future discordances follow `M~Binomial(n,q)` and probe-only wins conditional on `M` follow `Binomial(M,p10/q)`. Sum the probabilities of the fixed exact two-sided rejection region over `M`. The helper evaluates this finite model sum numerically.

Search every integer `n=1..2000` for its **first** 80% power crossing; do not assume monotonicity or claim a sustained/permanent threshold. Record the cap and power at the first crossing. No crossing is right-censored beyond the search, not “impossible.” Equal observed discordance rates have no specified directional effect; do not manufacture an 80% discrimination count. Plug-in probabilities from 14 items are uncertain; this is conditional planning, not a validated future-sample requirement. If only accuracy totals exist and joint discordance probabilities are unidentified, report paired `N80 = UNMEASURED` with the missing input, rather than substituting the one-sample fair-coin design target.

## Scientific wording limits

These are different complete methods: the organizers' probe and the frozen text control. Their comparison alone is **not a causal ablation of the same pipeline's white-box signal**. The report may describe a pre-registered comparative control and explicitly state this limitation. Nonsignificance is not equivalence, black-box sufficiency, absence of a white-box benefit, or a prediction about final-test rankings. Official server scores must be attributed to their actual submission IDs and task; no keyword gate authenticates those facts. The v9 lead gate remains unchanged and its 7/7 outcome does not certify these statistical conditions.

## Evidence and implementation

`paired_protocol.py` implements the formulas and failure cases. Its tests use invented inputs and are never competition receipts. Root must commit this protocol and its tested helper before H1; then preserve actual official receipt times to prove chronology. Only after official IDs and scores exist should `SCORES.json` and `ABLATION.json` be populated. Do not place synthetic fixtures in those artifact names.

Primary implementation references, checked 2026-10-27:

- [Statsmodels exact McNemar API](https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html): exact mode is binomial and uses the two discordant categories.
- [Statsmodels reference implementation](https://www.statsmodels.org/stable/_modules/statsmodels/stats/contingency_tables.html#mcnemar): doubled smaller Binomial(1/2) tail, clipped at one; its general contingency-table assumptions state iid observation units.
- [SciPy binomtest API](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html): a binomial test concerns a specified Bernoulli probability and supports a two-sided alternative. It does not make two paired accuracy totals independent.

The feasible-table bounds and prediction-disagreement identity above are explicit algebraic deductions from common-N binary pairing, not claims that those packages implement an aggregate-only McNemar interface.
