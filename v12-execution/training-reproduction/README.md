# Published text-control recipe: local reproduction proof

`tools/reproduce_control.py` is a standalone, network-free adaptation of the recovered original fitting recipe. The original source is archived at `v12-execution/audit/reproduce_control.original.py`, SHA-256 `cab8d45d75d228fe6bf7b5cdd11490fbcbd7b10af19811684bbb4e5035c2596e`; the new operator source SHA-256 is `1ca22456b36b2a934b36cc60a48f3047601517761c3fb6c3464b78a15ec4425c`. The new program does not depend on the archived Desktop source at runtime.

The public parquet is `aimo-interp/train-main-v2`, SHA-256 `e18eb44207e7987781ec2ff214793196038442bdc1466fdf5498f3e87ec58285`, 11372 bytes. Its verified local copy is `data/train-main-v2.parquet` and remains ignored by Git. A reviewer obtains those pinned bytes separately using the repository data instructions. The reproducer performs no network request, does not open private evaluation outputs and never updates report_numbers.py, claims, manuscript source or a PDF.

Final fitting uses all 80 labelled rows from 94 total rows, excluding 14 unlabelled rows. There are 33 distinct problems in that fitted cohort. The separately counted Small-only labelled cohort has 43 rows from 22 distinct problems. These counts are computed from the parquet; the fitting code contains no assertion that the cohort has a hand-entered size. No OOF claim is produced by this command.

The recipe uses LogisticRegression(class_weight="balanced", max_iter=2000) directly on log1p problem length and Unicode digit count, without a fitted scaler. The numerical tolerance was recorded before execution. Refit coefficient max difference: 8.326672684688674e-16; intercept: 4.440892098500626e-15; probability: 3.3306690738754696e-16; all must be strictly below 1e-10. Threshold predictions match on all 94 public rows. Runtime versions and all estimator settings are in PROOF.json. The emitted refitted joblib is numerically equivalent; its bytes are not represented as identical to the supplied artifact.

The deterministic packaging check is a separate measurement. It repackages the unchanged hash-pinned submitted solution/artifact with fixed member order, timestamps, permissions and compression. The output is byte-identical to the 1387-byte official bundle with SHA-256 `30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd`. This packaging result is not a claim of bitwise equality of numerical refitting or a reproduction of private scores.

Offline tests: 11 passed, 0 skipped. Cases reject corrupted data/ZIP before pickle loading, schema/label defects, coefficient/intercept/class/parameter changes, unexpected members, and outputs overwriting inputs; they check Unicode features, missing-label selection, deterministic packaging metadata and actual public-data refitting while blocking external process/network calls. Actual execution in the new pinned repository .venv returned 0 in 1.676 seconds; its 11 tests passed with no skips. An earlier 30-second subprocess timeout is recorded without asserting its cause; the subsequent import probe and actual tests/refit passed.

With the repository's pinned requirements installed, run from the repository root:

```sh
.venv/bin/python -I tools/reproduce_control.py --data-dir data --out results/reproduction/control.json
```

Optional `--refit-artifact PATH` emits a fitted model; `--rebuilt-bundle PATH` emits the byte-verified original packaging. Executed interpreter/arguments, return codes and timing summaries are in EXECUTIONS.json. The full current test stderr is committed; remaining raw stdout/stderr logs are retained locally. PROOF.json is the native measured result. Scientific final-board keys and v8.4 content remain deferred until the final-board procedure.
