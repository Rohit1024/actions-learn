#!/usr/bin/env bash
set -euo pipefail
node "$ACTION_DIR/accept.cjs" "${RAW_LABEL-}"
