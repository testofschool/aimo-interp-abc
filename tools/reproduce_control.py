#!/usr/bin/env python3
"""Refit the submitted text control from pinned public data, without network.

Install requirements-local.txt, obtain the pinned public parquet, then run:
  python tools/reproduce_control.py --data-dir data --out results/reproduction/control.json

Final fitting uses every labelled row. Small-only public evaluation is a separate
cohort. Refit parity is numerical; deterministic ZIP packaging is checked against
the unchanged submitted source/artifact, not against BLAS-bitwise fitted bytes.
"""
import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import platform
import re
import zipfile

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parents[1]
DATASET_ID = "aimo-interp/train-main-v2"
TRAIN_SHA256 = "e18eb44207e7987781ec2ff214793196038442bdc1466fdf5498f3e87ec58285"
BUNDLE_SHA256 = "30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd"
ARTIFACT_SHA256 = "e78784044aa5acefb48e956e27d84b15065c26f83d295663834808424dcd180d"
ORIGINAL_RECIPE_SHA256 = "cab8d45d75d228fe6bf7b5cdd11490fbcbd7b10af19811684bbb4e5035c2596e"
TOLERANCE = 1e-10
MEMBERS = {"solution.py", "artifacts/text_length.joblib", "small.txt"}


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_pinned(path, expected):
    with Path(path).open("rb") as handle:
        raw = handle.read(20 * 1024 * 1024 + 1)
    require(sha256(raw) == expected, "pinned input SHA-256 mismatch: " + Path(path).name)
    return raw


def features(problems):
    # Recovered original feature recipe; digits use Python's Unicode-aware \d.
    return np.asarray([[math.log1p(len(p)), len(re.findall(r"\d", p))] for p in problems])


def estimator():
    return LogisticRegression(class_weight="balanced", max_iter=2000)


def training_table(raw):
    table = pd.read_parquet(io.BytesIO(raw))
    require({"problem", "model_id", "is_robust"}.issubset(table.columns), "training schema mismatch")
    require(table.problem.map(lambda value: isinstance(value, str)).all(), "non-string public problem")
    labelled = table.dropna(subset=["is_robust"]).copy()
    require(len(labelled) > 0 and set(labelled.is_robust.unique()) == {False, True}, "binary labels required")
    return table, labelled


def deterministic_zip(payloads):
    """Use the published packaging recipe with fixed timestamp/order/mode."""
    require(set(payloads) == MEMBERS, "unexpected Small bundle members")
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, raw in sorted(payloads.items()):
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 2175008768
            archive.writestr(info, raw, compresslevel=9)
    return output.getvalue()


def compare_models(refit, submitted, problems):
    require(type(submitted) is LogisticRegression, "unexpected submitted estimator")
    require(submitted.coef_.shape == refit.coef_.shape, "coefficient shape mismatch")
    require(submitted.intercept_.shape == refit.intercept_.shape, "intercept shape mismatch")
    require(int(submitted.n_features_in_) == 2, "feature dimensionality mismatch")
    require(np.array_equal(submitted.classes_, refit.classes_), "class order mismatch")
    require(submitted.get_params() == refit.get_params(), "estimator parameter mismatch")
    x = features(problems)
    refit_probability = refit.predict_proba(x)[:, 1]
    submitted_probability = submitted.predict_proba(x)[:, 1]
    values = {
        "coefficient_max_abs_difference": float(np.max(np.abs(refit.coef_ - submitted.coef_))),
        "intercept_max_abs_difference": float(np.max(np.abs(refit.intercept_ - submitted.intercept_))),
        "probability_max_abs_difference": float(np.max(np.abs(refit_probability - submitted_probability))),
        "prediction_rows": len(problems),
        "threshold_prediction_equal": bool(np.array_equal(refit_probability >= 0.5, submitted_probability >= 0.5)),
        "refit_coef": refit.coef_.tolist(), "submitted_coef": submitted.coef_.tolist(),
        "refit_intercept": refit.intercept_.tolist(), "submitted_intercept": submitted.intercept_.tolist(),
        "classes": submitted.classes_.tolist(), "tolerance": TOLERANCE,
    }
    for key in ("coefficient_max_abs_difference", "intercept_max_abs_difference", "probability_max_abs_difference"):
        require(math.isfinite(values[key]) and values[key] < TOLERANCE, key + " exceeds tolerance")
    require(values["threshold_prediction_equal"], "public threshold predictions differ")
    return values


def reproduce(train, bundle, refit_artifact=None, rebuilt_bundle=None):
    require(sklearn.__version__ == "1.8.0" and joblib.__version__ == "1.5.3", "use pinned requirements-local.txt runtime")
    train_raw = read_pinned(train, TRAIN_SHA256)
    bundle_raw = read_pinned(bundle, BUNDLE_SHA256)
    with zipfile.ZipFile(io.BytesIO(bundle_raw)) as archive:
        require(len(archive.namelist()) == len(MEMBERS) and set(archive.namelist()) == MEMBERS, "ZIP member mismatch")
        payloads = {name: archive.read(name) for name in MEMBERS}
    require(sha256(payloads["artifacts/text_length.joblib"]) == ARTIFACT_SHA256, "artifact SHA-256 mismatch")
    # No pickle is loaded until both complete input files and the member are pinned.
    artifact = joblib.load(io.BytesIO(payloads["artifacts/text_length.joblib"]))
    require(isinstance(artifact, dict) and "model" in artifact, "artifact schema mismatch")
    table, labelled = training_table(train_raw)
    model = estimator().fit(features(labelled.problem), labelled.is_robust.astype(int))
    parity = compare_models(model, artifact["model"], table.problem)
    small = labelled[labelled.model_id != "openai/gpt-oss-120b"]
    metadata = {key: value for key, value in artifact.items() if key != "model"}
    generated_metadata = {"features": "log1p(len(problem)), count(digits)",
                          "trained_on": f"{DATASET_ID} labelled rows ({len(labelled)})", "sha_train": TRAIN_SHA256[:8]}
    require(metadata == generated_metadata, "training metadata differs from measured cohort")
    packed = deterministic_zip(payloads)
    require(packed == bundle_raw, "deterministic packaging differs from submitted ZIP")
    recipe = {"training_selector": "dropna(is_robust); fit all remaining rows with integer labels",
              "features": generated_metadata["features"], "estimator": model.get_params(),
              "scaling": "No fitted scaler or standardization; direct log1p-length and digit-count features."}
    result = {
        "status": "PASS", "dataset_id": DATASET_ID,
        "train_path": str(Path(train).resolve()), "train_sha256": sha256(train_raw), "train_bytes": len(train_raw),
        "rows": {"public_total": len(table), "labelled_fit": len(labelled), "unlabelled_excluded": int(table.is_robust.isna().sum()),
                 "fit_distinct_problems": int(labelled.problem.nunique()), "small_labelled": len(small),
                 "small_distinct_problems": int(small.problem.nunique())},
        "label_counts": {str(int(label)): int(count) for label, count in labelled.is_robust.value_counts().items()},
        "training_model_rows": {str(name): int(count) for name, count in labelled.model_id.value_counts().items()},
        "bundle_path": str(Path(bundle).resolve()), "bundle_sha256": sha256(bundle_raw), "bundle_bytes": len(bundle_raw),
        "artifact_sha256": ARTIFACT_SHA256, "artifact_metadata": metadata, "recipe": recipe,
        "recipe_sha256": sha256(json.dumps(recipe, sort_keys=True, separators=(",", ":")).encode()),
        "recipe_hash_scope": "UTF-8 canonical JSON of selector, feature formula, estimator parameters and scaling",
        "reproducer_sha256": sha256(Path(__file__).read_bytes()),
        "recovered_original_source_sha256": ORIGINAL_RECIPE_SHA256,
        "parity": parity,
        "packaging": {"identical_to_submitted_zip": True, "sha256": sha256(packed), "bytes": len(packed),
                      "scope": "Repackages unchanged pinned submitted source/artifact; numerical refit is checked separately."},
        "runtime": {"python": platform.python_version(), "sklearn": sklearn.__version__, "joblib": joblib.__version__,
                    "numpy": np.__version__, "pandas": pd.__version__},
        "scope": "Public-data final-fit and packaging reproduction; no OOF, private-validation or final-test result is produced.",
    }
    if refit_artifact is not None:
        target = Path(refit_artifact)
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = io.BytesIO()
        joblib.dump({"model": model, **generated_metadata}, raw, compress=0, protocol=4)
        target.write_bytes(raw.getvalue())
        result["refit_artifact"] = {"path": str(target.resolve()), "sha256": sha256(raw.getvalue()),
                                    "bytes": len(raw.getvalue()), "bitwise_equality_to_submitted_not_required": True}
    if rebuilt_bundle is not None:
        target = Path(rebuilt_bundle)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(packed)
        result["rebuilt_bundle_path"] = str(target.resolve())
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--bundle", type=Path, default=ROOT / "bundles/solution-text-length-control-small.zip")
    parser.add_argument("--out", type=Path, required=True, help="JSON proof output; no scientific registry is modified")
    parser.add_argument("--refit-artifact", type=Path)
    parser.add_argument("--rebuilt-bundle", type=Path)
    args = parser.parse_args(argv)
    try:
        outputs = [path.resolve() for path in (args.out, args.refit_artifact, args.rebuilt_bundle) if path is not None]
        inputs = {(args.data_dir / "train-main-v2.parquet").resolve(), args.bundle.resolve(), Path(__file__).resolve()}
        require(len(outputs) == len(set(outputs)) and not inputs.intersection(outputs), "output paths may not overwrite inputs or each other")
        result = reproduce(args.data_dir / "train-main-v2.parquet", args.bundle, args.refit_artifact, args.rebuilt_bundle)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2) + "\n")
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
