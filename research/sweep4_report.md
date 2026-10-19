# Direction sweep — AIMO-Interp round 4: which lead claim for the writeup report

Success line (given): report selected for a writeup prize (owner's goal A); minimum = report submitted by 2026-11-15 with all numbers regenerating
Swept at: 2026-10-19T23:34:56+09:00

| Candidate | kind | payer | mechanism | substitute | reach | input | kill |
|---|---|---|---|---|---|---|---|
| Ra text control beats organizer baseline on its own rows | proposal | ? | ✓ | ? | ? | ✓ | dead |
| Rb labels are a property of the problem (concordance) | proposal | ? | ✓ | △ | ? | ✓ | dead |
| Rc power and data audit | proposal | ? | ✓ | △ | ? | ✓ | dead |
| Rd label-construction audit with required controls | proposal | ? | ✓ | ? | ? | ✓ | dead |
| S1 minimal report: control + numbers, no lead claim | substitute | ? | ? | ? | ? | ✓ | — |
| W1 fold completely | wait | ? | ? | ? | ? | ? | — |

**Verdict: NO_SURVIVOR_STAY_WITH_BASELINE**

- baseline S1 minimal report: control + numbers, no lead claim: unknown = ['payer', 'mechanism', 'substitute', 'reach']; fails = none
- baseline W1 fold completely: unknown = ['payer', 'mechanism', 'substitute', 'reach', 'input']; fails = none
- eliminated Ra text control beats organizer baseline on its own rows: killed: on the 141-row set a format flag scores 1.00 and majority 0.745
- eliminated Rb labels are a property of the problem (concordance): killed: frontier-model set: problem explains R2 0.18 vs 0.78 on train
- eliminated Rc power and data audit: killed: another participant's approved report covers the same thesis
- eliminated Rd label-construction audit with required controls: killed: the 141-row and frontier sets are never scored

Escapes named by killers (designer-authored candidates excluded from the count):
- [converged] scored data only: problem identity explains ~80% of max_drop; problem-only/text control matches probes under grouped CV; test whether it survives unseen problems via Codabench private val — named by Rb, Rd
- [converged] report plain accuracy and trivial baselines (majority, format) beside balanced accuracy — named by Ra, Rd

**Pick: S1**
- Riskiest assumption: a short report built on the converged escape (problem identity ~80% of max_drop on scored data; problem-only control; survival on unseen problems via Codabench) is selectable
- Cheapest test: Codabench private-val accuracy of the text control vs always-true, uploaded before 2026-11-01 11:55Z
- Pass: control >= always-true on Codabench -> section 3 reports 'survives'; else reports 'collapses' (both are publishable results) / Fail: no Codabench rows by 2026-11-01 11:55Z -> section 3 is cut and the report states the limitation / Stop: report frozen 2026-11-12 23:59 KST; no paid jobs
- Registered 2026-10-19T23:35:45+09:00, check by 2026-11-15T23:59:00+09:00
