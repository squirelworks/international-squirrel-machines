#!/usr/bin/env bash
# SS-BO-01 — brownout forces neutral (host stub)
set -euo pipefail
cd "$(dirname "$0")/.."
make test
echo "SS-BO-01 covered by tests/test_safe_state.c brownout case"
