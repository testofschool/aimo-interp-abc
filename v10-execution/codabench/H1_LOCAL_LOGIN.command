#!/bin/zsh
set -eu
aimo_task_root="$(cd -- "$(dirname -- "$0")/../.." && pwd)"
exec "$aimo_task_root/v10-execution/orvenv/bin/python" "$aimo_task_root/tools/codabench_v101_upload.py" --run
