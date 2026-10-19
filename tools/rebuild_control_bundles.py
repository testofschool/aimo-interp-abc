#!/usr/bin/env python3
"""Rebuild supplied ZIP bytes from committed inference source + artifact.

This is packaging reproduction. tools/reproduce_control.py independently refits
the artifact and validates numerical parity; it does not promise BLAS-bitwise fits.
"""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=ROOT / "results/rebuilt_bundles")
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    source = ROOT / "bundles/text-length-control-src"
    results = []
    for small in (False, True):
        name = f"solution-text-length-control{'-small' if small else ''}.zip"
        payloads = {"solution.py": (source / "solution.py").read_bytes(),
                    "artifacts/text_length.joblib": (source / "artifacts/text_length.joblib").read_bytes()}
        if small:
            payloads["small.txt"] = b""
        target = args.output / name
        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for member, content in sorted(payloads.items()):
                info = zipfile.ZipInfo(member, date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type, info.create_system, info.external_attr = zipfile.ZIP_DEFLATED, 3, 2175008768
                z.writestr(info, content, compresslevel=9)
        supplied = ROOT / "bundles" / name
        same = supplied.read_bytes() == target.read_bytes()
        results.append({"bundle": name, "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                        "bytes": target.stat().st_size, "identical_to_supplied": same})
        if not same:
            raise SystemExit(f"STOP: rebuilt archive differs: {name}")
    print(json.dumps({"status": "PASS", "bundles": results}, indent=2))


if __name__ == "__main__":
    main()
