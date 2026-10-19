# Direction sweep — AIMO-Interp round 3: does any data source outside the competition's own data give a working method? (owner: if not, fold)

Success line (given): a method that beats the text control by >=0.07 with a detectable effect, else fold (owner, 2026-10-19 23:02 KST)
Swept at: 2026-10-19T23:13:48+09:00

| Candidate | kind | payer | mechanism | substitute | reach | input | kill |
|---|---|---|---|---|---|---|---|
| X1 label-free external difficulty score (Omni-MATH TF-IDF ridge) | proposal | ? | ✕ | ? | ✓ | ✓ | dead |
| X2 self-generated labels: 40 problems x 4 models, K=2, S=16 (~$12-14) | proposal | ? | ✕ | ? | ? | ✓ | dead |
| X3 public generation dumps -> predicted base accuracy | proposal | ? | ✕ | ? | ? | ✕ | dead |
| S1 keep the valid text-control entry + report (no new method) | substitute | ? | ? | ? | ? | ✓ | — |
| W1 fold: stop all further work and spending | wait | ? | ? | ? | ? | ? | — |

**Verdict: NO_SURVIVOR_STAY_WITH_BASELINE**

- baseline S1 keep the valid text-control entry + report (no new method): unknown = ['payer', 'mechanism', 'substitute', 'reach']; fails = none
- baseline W1 fold: stop all further work and spending: unknown = ['payer', 'mechanism', 'substitute', 'reach', 'input']; fails = none
- eliminated X1 label-free external difficulty score (Omni-MATH TF-IDF ridge): premise 'mechanism' fails: tuned on gpt-oss rows threshold 5.21 -> Small bacc 0.554; fixed thresholds 0.457-0.624, all below control 0.686 / killed: no threshold set without target labels beats the text control
- eliminated X2 self-generated labels: 40 problems x 4 models, K=2, S=16 (~$12-14): premise 'mechanism' fails: true drop 0 -> labelled non-robust 0.075-0.180; band 0.26-0.28; true 0.30 drop caught 0.698 / killed: at S=16, K=2 most non-robust positives would be sampling noise
- eliminated X3 public generation dumps -> predicted base accuracy: premise 'mechanism' fails: oracle base_accuracy AUROC 0.733 (24 deduplicated pairs); 8 of 15 non-robust have base accuracy 1.0 / premise 'input' fails: dump is Skywork-OR1-7B, not Skywork-OR1-Math-7B; Olmo dump is greedy single sample; Qwen3.5-4B dump has 30 problems / killed: even oracle base accuracy predicts robustness weakly

Escapes named by killers (designer-authored candidates excluded from the count):
- [converged] model-specific labels with many samples per item (S>=48) on the exact 4 checkpoints, validated against the 43 official rows — named by X2, X3
- [converged] a model-dependent signal on top of difficulty (base pass rate or internals) — named by X1, X3

**Pick: S1**
- Riskiest assumption: no affordable data source yields reliable target-model labels (S>=48, 4 exact checkpoints, >=150 rows, >=0.80 agreement with the 43 official rows)
- Cheapest test: tools/reopen_gate.py --labels <file> exits 0
- Pass: gate exit 0 -> reopen the method track with a new sweep / Fail: gate exit 1 -> method track stays folded; keep the text-control entry / Stop: no paid method job while the gate is CLOSED; the decision re-checks only if the owner adds budget >= $45 before 2026-10-27
- Registered 2026-10-19T23:14:33+09:00, check by 2026-10-27T23:59:00+09:00
