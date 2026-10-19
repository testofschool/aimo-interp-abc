# Current state: v4 CPU checks complete; owner decision pending

`HANDOFF_v4.md` is the current supplied execution specification. The method track
is folded, the White-Box Award is out, and no paid follow-on job is allowed while
`tools/reopen_gate.py` returns CLOSED. Q1 and the S=16 synthetic X2 gate replay
both return CLOSED / exit 1; P5 matches all four dataset hashes; P6 returns PASS,
6/6, exit 0. Additional jobs: 0; additional spend: $0. Historical recorded J0
spend remains $0.412497; billing was not fetched again in this CPU run.

See `EXECUTION_REPORT_v4.md`, `RUN_STATUS.json`, and `results/v4/` for exact outputs,
provenance and limitations. The six-claim gate does not independently verify the
external-data sweep or every numerical statement. The supplied v4 packet is
preserved separately in `../handoff-v4-source/`; four conflicting older files were
retained in this repository, including its strengthened scoring/submission gates.

The original F12 Small ZIP remains the entry candidate, SHA256
`30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd`.
Owner O1 (account/board receipt) and O2 (keep the report or close completely) are
pending. The previous report is a historical draft; no new report or external
submission has been completed. The text-only control does not load the passed
model, so the all-True unknown-model fallback criterion is inapplicable under
`DELTA_v2.2.md`; the guarded derivative remains unselected.

The remaining README is the historical v2/J0 preparation record. Its pending
method plans are superseded by v4 and are not launch authorization.

---

# AIMO Small Track control-first A/B/C

Current work is **incomplete**. The supplied control has been reproduced locally;
E1′/E2′/E3′ have no measured OOF results. One owner-authorized J0 measurement job
completed 20/20 feature rows with 9 billed minutes / $0.412497; follow-on paid
jobs are not authorized. No competition
submission has been made. Read `RUN_STATUS.json` and `EXECUTION_NOTES.md`.

The original source files are preserved. The supplied Small ZIP remains
`30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd`.

## Observed local checks

- Text-length control: 43 rows / 22 problems; balanced accuracy 0.6855,
  problem-bootstrap CI [0.4648, 0.9375], accuracy 0.7674.
- The recovered recipe fits all 80 labelled rows excluding the complete held-out
  problem, then evaluates 43 Small rows. Reproduced scores agree within 4.45e-16.
- Exact original ZIP passed official pinned host-Python `run_local.py --small`
  twice: coverage 1.0, invalid 0, public-sample accuracy 0.5416667. Predictions
  were byte-identical. This is a host contract check, not GPU image parity.
- Supplied control fails the unknown-model all-True fallback requirement.
- A separate, unselected guarded control preserves 624 known-model comparisons
  and passes the unknown-model fallback checks. Its two host sample runs score
  0.375 because all sample model IDs use fallback; the original remains unchanged.
- Submission gate rejects incorrect labels, duplicate keys and invalid scores;
  numerical threshold remains best control +0.07 = 0.755483870967742.

## Reproduce local evidence

Use Python 3.12; local dependencies are distinct from the competition GPU image.

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements-local.txt
.venv/bin/python -I -m unittest discover -s tests -v
.venv/bin/python tools/reproduce_control.py
.venv/bin/python tools/rebuild_control_bundles.py
.venv/bin/python -I tools/grouped_eval.py controls/text_length.csv
.venv/bin/python -I tools/grouped_eval.py --constant-baselines data/train-main-v2.parquet --small
```

`reproduce_control.py` independently refits the estimator with fold membership
evidence and numeric parity checks. `rebuild_control_bundles.py` rebuilds both
original ZIPs byte-for-byte from inference source and supplied artifact. These
are separate checks; cross-platform BLAS fits need not be bit-identical.

The official harness is pinned to
`de794053debe75a711400696e66b60937cebbb1b`:

```sh
git clone https://github.com/aimo-interp/getting-started.git upstream/getting-started
git -C upstream/getting-started checkout --detach de794053debe75a711400696e66b60937cebbb1b
.venv/bin/python upstream/getting-started/scripts/import_hf_dataset.py --output-dir data/val-sample
.venv/bin/python upstream/getting-started/scripts/run_local.py bundles/solution-text-length-control-small.zip --small --input-dir data/val-sample/input --reference-dir data/val-sample/reference
```

This obtains the public development sample using existing HF authentication if
needed. Do not publish sample reference files or credentials in submission ZIPs.

## Measured feature evaluation

Feature extraction and J0 definitions live in `experiments/e1p/` and `jobs/`.
Review the job plan before any paid launch. With actual complete JSONL feature
records, fixed-recipe evaluators are:

```sh
.venv/bin/python tools/train_challengers.py E1p --features results/features.jsonl --extraction-manifest results/manifest.json
.venv/bin/python tools/train_challengers.py E1p_ablate --features results/features.jsonl --extraction-manifest results/manifest.json
.venv/bin/python tools/train_challengers.py E3p --features results/features.jsonl --extraction-manifest results/manifest.json
.venv/bin/python -I tools/submit_gate.py results/E1p/oof.csv results/E1p_ablate/oof.csv
```

These commands cannot create scores from missing features. E3 needs every other
model's measured features for each evaluated problem. The owner corrected E2 to
train49 (43 labelled + 6 unlabelled), evaluate43; its cohort hold is released.
`experiments/e2p/` records its CPU-only contract and remaining UNRUN work.
Gate PASS alone does not establish
OOF provenance, runtime parity, offline cache availability or a public submission.
J0's collector is deliberately bound to 20 rows. `jobs/full_features/` now prepares
the separate 96-identity collection path for all 24 Small texts and four models.
Its plan is non-dispatchable: allocating a full job still requires actual J0
measurements, complete budget forecasts and review. J0's five texts cannot train
the 43-row OOF. `tools/project_runtime.py` reads complete real J0 receipts only;
the measured J0 projection is saved in `results/j0/runtime_projection.json`.
E1's current 50×4 recipe projects to 4,021.21 seconds, exceeding the registered
3,600-second bar before other overhead. Full A/B/C cost remains UNMEASURED/HOLD.
The helper distinguishes E3's other-three-model
600-extraction workload from the frozen runner's redundant 800-extraction upper
bound. Neither forecast clears total cost or runtime acceptance.

`tools/run_gate_smoke.py` creates one fixed seed-0 synthetic fixture and returns
the actual rejection code 1. Its score is not scientific OOF. The separate guarded
ZIP can be rebuilt using `tools/build_guarded_control.py`; see
`results/guarded_control/README.md` for limitations and the unchanged original.

## Report evidence and limitations

`research/live_audit/` contains primary-source snapshots and exact fetch metadata.
Other-model permission is confirmed; the organizer's cache statements conflict.
`research/spec_audit.md` records this and other handoff discrepancies. Scientific
negative results require actual execution; unrun experiments remain UNRUN.
The concordance audit corrects val-sample from 1/6 to 0/5 after deduplication;
sample-full's 1/10 uses derived labels. E3 therefore remains on hold independently
of E1. See `research/live_audit/F13_CONCORDANCE.md`.

`report/` and `output/pdf/` contain an audited five-page working draft with
unchanged official NeurIPS 2026 style. Actual GPU results, author review, the
final report and submission receipts remain outstanding. `research/COMPLETION_AUDIT.md`
tracks completion requirements separately from local preparation.

AI assistance disclosure: Claude authored the supplied handoff/control materials.
OpenAI Codex prepared the current execution audit, code and local verification,
with parallel agents for independent audit, primary-source verification and
feature-runner implementation. Felix has not yet reviewed a final report.
