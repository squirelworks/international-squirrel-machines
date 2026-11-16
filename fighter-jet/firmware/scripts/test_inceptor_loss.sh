#!/usr/bin/env bash
# SS-IN-01 — inceptor loss forces neutral (host stub)
set -euo pipefail
cd "$(dirname "$0")/.."
make test
echo "SS-IN-01 covered by tests/test_safe_state.c inceptor-loss case"
