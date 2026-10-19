# Optional historical mixed-label calculation

The pinned participant repository has an MIT LICENSE. It was read before using
`data/self_labels.jsonl`; exact commit, license/data hashes and paths are in
`source_audit.json`. Raw data were fetched outside the public release checkout
and are not redistributed. `results/v6/mixed_label_transfer.json` records the CPU
calculation; `optional_transfer_validation.json` compares all requested values.

The calculation uses the full original 150-problem pool. The prior authors later
excluded some problems as leakage-prone (see their October 12 RESULTS update),
so this historical sensitivity is omitted from the main report and from V1–V6.
No private competition result or generalization improvement is inferred.

The attached analysis source is preserved byte-identically as
`tools/optional_mixed_label_transfer.py` (SHA256 in the validation receipt).
For optional reproduction, obtain the original file from the immutable commit,
check its SHA256 against `source_audit.json`, read LICENSE, then run:

```sh
.venv/bin/python -I tools/optional_mixed_label_transfer.py tools /absolute/path/to/verified/self_labels.jsonl data/train-main-v2.parquet /tmp/optional-transfer.json
```

The optional script itself does not enforce input hashes; the preceding explicit
hash check is required. The mandatory report scripts enforce hashes internally.
The public result JSON contains aggregate statistics only.
