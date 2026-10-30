#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 ]]; then
  printf '%s\n' 'expected exactly one file argument' >&2
  exit 1
fi
node "$ACTION_DIR/inspect.cjs" "$1"
