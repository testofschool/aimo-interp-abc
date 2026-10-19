#!/usr/bin/env python3
"""Fetch exact public organizer parquet bytes; stop on any hash mismatch.

Python standard library only. No authentication, token store or HF client is used.
Run from the reproduction repository root:
    python3 -I tools/fetch_data.py --output-dir data
    python3 -I tools/fetch_data.py --output-dir data --verify-only

The repository should publish this fetcher and manifest, not the parquet files.
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


FILES = (
    {
        "filename": "train-main-v2.parquet",
        "repo_id": "aimo-interp/train-main-v2",
        "revision": "fa8af758c6519fc97a9d0bd9017feb6f12232b52",
        "path": "data/train-00000-of-00001.parquet",
        "bytes": 11372,
        "sha256": "e18eb44207e7987781ec2ff214793196038442bdc1466fdf5498f3e87ec58285",
    },
    {
        "filename": "val-sample.parquet",
        "repo_id": "aimo-interp/val-sample",
        "revision": "1ae454ec1fad9727084eda8f9f3c9ae2239b21de",
        "path": "data/validation-00000-of-00001.parquet",
        "bytes": 23788,
        "sha256": "3919cb3d951bb360a120be3397e926f48b7819bcd97e12cfee4c01e76618560f",
    },
    {
        "filename": "sample-full.parquet",
        "repo_id": "aimo-interp/aimo-interp-challenge-sample-full",
        "revision": "c0ffb7e678294cc8819d50d979ba28ba49bd02d0",
        "path": "data/validation-00000-of-00001.parquet",
        "bytes": 94757,
        "sha256": "2989ab6a018f2779a821209f414bd0049c9ef1c2488f589ff2d3bf4ed16942ff",
    },
    {
        "filename": "augmented-sample-math-agg.parquet",
        "repo_id": "aimo-interp/augmented-sample-math-agg",
        "revision": "f972ced0705096f8d7ca7fac30825900b8b7fb6a",
        "path": "data/validation-00000-of-00001.parquet",
        "bytes": 50071,
        "sha256": "b785750259a3f4524cbaf988f51660197cbdfca19d8f45cc35347d4ef29aa4db",
    },
)


class FetchError(RuntimeError):
    pass


def verify(path, entry):
    if not path.is_file() or path.is_symlink():
        raise FetchError(f"STOP: missing, non-regular or symbolic-link file: {entry['filename']}")
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
            size += len(block)
    if size != entry["bytes"] or digest.hexdigest() != entry["sha256"]:
        raise FetchError(f"STOP: size/hash mismatch: {entry['filename']}; existing file preserved")


def url_for(entry):
    repo = urllib.parse.quote(entry["repo_id"], safe="/")
    revision = urllib.parse.quote(entry["revision"], safe="")
    path = urllib.parse.quote(entry["path"], safe="/")
    return f"https://huggingface.co/datasets/{repo}/resolve/{revision}/{path}"


def download(entry, destination):
    request = urllib.request.Request(
        url_for(entry), headers={"User-Agent": "aimo-interp-pinned-public-data/1.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            if response.status != 200:
                raise FetchError(f"STOP: HTTP {response.status}: {entry['filename']}")
            size = 0
            with destination.open("xb") as stream:
                for block in iter(lambda: response.read(1024 * 1024), b""):
                    size += len(block)
                    if size > entry["bytes"]:
                        raise FetchError(f"STOP: downloaded size mismatch: {entry['filename']}")
                    stream.write(block)
    except urllib.error.HTTPError as exc:
        raise FetchError(f"STOP: HTTP {exc.code}: {entry['filename']}") from None
    except (urllib.error.URLError, TimeoutError, OSError):
        # Do not print redirect URLs, credentials, environment values or headers.
        raise FetchError(f"STOP: download failed: {entry['filename']}") from None
    verify(destination, entry)


def fetch(output_dir, verify_only=False):
    output_dir = output_dir.resolve()
    missing = []
    # Validate all existing paths before downloading or replacing anything.
    for entry in FILES:
        path = output_dir / entry["filename"]
        if path.exists() or path.is_symlink() or verify_only:
            verify(path, entry)
        else:
            missing.append(entry)
    if missing:
        output_dir.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".aimo-download-", dir=output_dir))
        try:
            for entry in missing:
                download(entry, staging / entry["filename"])
            # Commit only after every missing download has passed verification.
            for entry in missing:
                destination = output_dir / entry["filename"]
                if destination.exists() or destination.is_symlink():
                    raise FetchError(f"STOP: destination appeared during download: {entry['filename']}")
            for entry in missing:
                destination = output_dir / entry["filename"]
                # Hard-link creation refuses to overwrite a destination that races
                # with the existence check. Both paths are on the same filesystem.
                os.link(staging / entry["filename"], destination)
        finally:
            shutil.rmtree(staging)
    for entry in FILES:
        verify(output_dir / entry["filename"], entry)
    return {
        "status": "PASS",
        "files": len(FILES),
        "downloaded": len(missing),
        "sha256": {entry["filename"]: entry["sha256"] for entry in FILES},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("data"))
    parser.add_argument("--verify-only", action="store_true", help="check all local files; never use network")
    args = parser.parse_args()
    try:
        result = fetch(args.output_dir, args.verify_only)
    except (FetchError, OSError) as exc:
        message = str(exc) if isinstance(exc, FetchError) else "STOP: local filesystem operation failed"
        print(message, file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
