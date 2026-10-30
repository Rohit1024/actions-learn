#!/usr/bin/env bash
set -euo pipefail
name=${REPORT_NAME-}
if [[ $name != *[![:space:]]* || $name == *$'\n'* || $name == *$'\r'* || ${#name} -gt 160 ]]; then
  printf '%s\n' 'name must be a nonblank single line of at most 160 characters' >&2
  exit 1
fi
if [[ -z ${GITHUB_OUTPUT-} ]]; then
  printf '%s\n' 'GITHUB_OUTPUT must be set' >&2
  exit 1
fi
printf 'summary=Ready, %s!\n' "$name" >> "$GITHUB_OUTPUT"
printf '%s\n' 'report rendered'
