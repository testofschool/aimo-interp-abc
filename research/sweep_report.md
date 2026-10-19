# Direction sweep — AIMO-Interp: which experiment carries the Small-Track entry, the White-Box ablation and the writeup

Success line (given): A+B+C: valid Small-Track entry visible on Codabench by 2026-11-01, White-Box ablation in report, report submitted by 2026-11-15
Swept at: 2026-10-19T13:46:15+09:00

| Candidate | kind | payer | mechanism | substitute | reach | input | kill |
|---|---|---|---|---|---|---|---|
| C1 E1 final-prompt-token hidden-state probe | proposal | ? | ? | △ | ? | ✓ | dead |
| C2 E2 uncertainty-profiling extended to 4 models | proposal | ? | ? | △ | ? | ✓ | wounded |
| C3 E3 problem-level majority target | proposal | ? | ? | ? | ? | ✓ | wounded |
| S1 submit an organizer baseline as-is (valid entry, no new method) | substitute | ? | ? | ? | ? | ✓ | — |
| W1 do not enter; wait for the 11-15 reports/next AIMO round | wait | ? | ? | ? | ? | ? | — |

**Verdict: NO_PROPOSAL_BEATS_BASELINE**

- survivor C2 E2 uncertainty-profiling extended to 4 models: unknown = ['payer', 'mechanism', 'reach']; test first = substitute
- survivor C3 E3 problem-level majority target: unknown = ['payer', 'mechanism', 'substitute', 'reach']; test first = payer
- baseline S1 submit an organizer baseline as-is (valid entry, no new method): unknown = ['payer', 'mechanism', 'substitute', 'reach']; fails = none
- baseline W1 do not enter; wait for the 11-15 reports/next AIMO round: unknown = ['payer', 'mechanism', 'substitute', 'reach', 'input']; fails = none
- eliminated C1 E1 final-prompt-token hidden-state probe: killed: E1 is the organizers' trained-probe baseline almost verbatim; ablation vs a problem-text control would likely show no substantial effect

Escapes named by killers (designer-authored candidates excluded from the count):
- [converged] short decode (<=512 tokens) / prefill features instead of 4096-token generation — named by C1, C2
- [single-source] writeup on negative result: probe vs problem/text-only control under leave-problem-out; label concordance is split-dependent — named by C1, C3
- [single-source] model-specific perturbation-response feature (hidden-state divergence original vs paraphrase) — named by C1
- [single-source] continuous max_drop target + pool train-main-v2, val-sample, sample-full with model one-hot; submit only if nested LOPO >= 0.76 — named by C2
- [single-source] beat a problem-text control (length+digits LOPO bacc 0.6855) before any claim; report the control if nothing beats it — named by C1, C3

**Pick: S1**
- Riskiest assumption: no experiment (E1 white-box, E2 short-decode uncertainty, E3 problem-level) beats the measured text-length control (LOPO bacc 0.6855 on 43 Small rows) by one public case (0.07)
- Cheapest test: tools/submit_gate.py on each experiment's leave-problem-out oof.csv against controls/always_true.csv + controls/text_length.csv
- Pass: an experiment exits 0 -> it replaces the control as the Small-Track entry; if it is white-box and also exits 0 against its own ablation, it is the White-Box claim / Fail: all exit 1 -> the text-length control stays the Small-Track entry and the report is a negative-results writeup (eligible per issue #10) / Stop: no new experiment starts after 2026-10-29 23:59 KST; HF Jobs spend capped at 25 USD
- Registered 2026-10-19T13:50:32+09:00, check by 2026-10-30T23:59:00+09:00
