#!/usr/bin/env bash
set -euo pipefail

name="${GREETING_NAME-World}"
if [[ "$name" == *$'\n'* || "$name" == *$'\r'* ]]; then
  printf '%s\n' 'name must be a nonempty, single-line string' >&2
  exit 1
fi
name="${name#"${name%%[![:space:]]*}"}"
name="${name%"${name##*[![:space:]]}"}"
if [[ -z "$name" ]]; then
  printf '%s\n' 'name must be a nonempty, single-line string' >&2
  exit 1
fi
: "${GITHUB_OUTPUT:?GITHUB_OUTPUT must be set}"
greeting="Hello, $name!"
printf 'greeting=%s\n' "$greeting" >> "$GITHUB_OUTPUT"
printf '%s\n' "$greeting"
