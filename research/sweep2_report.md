# Direction sweep — AIMO-Interp round 2: what does Codex do with the remaining 12 days and ~$24

Success line (given): A+B+C as owner set: valid Small entry by 2026-11-01 11:55Z, White-Box ablation in report, report by 2026-11-15
Swept at: 2026-10-19T22:36:18+09:00

| Candidate | kind | payer | mechanism | substitute | reach | input | kill |
|---|---|---|---|---|---|---|---|
| C1 E1'' prefill hidden-state divergence (white-box) | proposal | ? | ? | △ | ? | ✓ | dead |
| C2 E2'' prefill prompt-token uncertainty | proposal | ? | ? | ? | ? | ✓ | wounded |
| C3 Measurement-audit report: control vs baselines on matching rows, label-structure findings | proposal | ? | ✓ | ? | ? | ✓ | wounded |
| C4 Early-generation (64-128 token) hidden-state white-box | proposal | ? | ? | △ | ? | ✕ | wounded |
| S1 text-length control as the Small entry + report | substitute | ? | ? | ? | ? | ✓ | — |
| W1 stop spending; wait for results | wait | ? | ? | ? | ? | ? | — |

**Verdict: PICK**

- survivor C3 Measurement-audit report: control vs baselines on matching rows, label-structure findings: unknown = ['payer', 'substitute', 'reach']; test first = payer
- survivor C2 E2'' prefill prompt-token uncertainty: unknown = ['payer', 'mechanism', 'substitute', 'reach']; test first = payer
- baseline S1 text-length control as the Small entry + report: unknown = ['payer', 'mechanism', 'substitute', 'reach']; fails = none
- baseline W1 stop spending; wait for results: unknown = ['payer', 'mechanism', 'substitute', 'reach', 'input']; fails = none
- eliminated C1 E1'' prefill hidden-state divergence (white-box): killed: organizers already published the prefill last-token probe and it was their weakest baseline
- eliminated C4 Early-generation (64-128 token) hidden-state white-box: premise 'input' fails: small_rows 43, small_problems 22; min detectable bacc difference ~0.22-0.25

Escapes named by killers (designer-authored candidates excluded from the count):
- [converged] measure on matching rows/labels (organizer CV) before any comparison claim — named by C1, C3
- [converged] more target-model labels are required for any white-box ablation (n=43 MDE ~0.22) — named by C1, C2, C4
- [single-source] submit control + always-true before Nov 1 to get Codabench numbers for the report — named by C3

**Pick: C3**
- Riskiest assumption: the organizers will select a measurement-audit report whose numbers all regenerate from public data (payer slot untested)
- Cheapest test: every number in the draft passes tools/report_numbers.py --check research/claims.json, plus Codabench numbers for the control and always-true submitted before 2026-11-01 11:55Z
- Pass: report submitted on the organizers' channel by 2026-11-15 with check exit 0 and both Codabench rows cited / Fail: any claim the check cannot regenerate is cut from the report, not reworded / Stop: no paid GPU job beyond a single <=$3 prefill extraction for the white-box ablation section; no new method after 2026-10-29 23:59 KST
- Registered 2026-10-19T22:36:51+09:00, check by 2026-11-15T23:59:00+09:00
