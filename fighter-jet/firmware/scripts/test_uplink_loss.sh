#!/usr/bin/env bash
# SS-UL-01 — uplink loss forces neutral (host stub)
set -euo pipefail
cd "$(dirname "$0")/.."
make test
echo "SS-UL-01 covered by tests/test_safe_state.c uplink-loss case"
