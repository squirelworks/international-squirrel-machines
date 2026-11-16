#!/usr/bin/env bash
# SS-WD-01 — watchdog holds safe (host stub)
set -euo pipefail
cd "$(dirname "$0")/.."
make test
echo "SS-WD-01 covered by tests/test_safe_state.c watchdog case"
