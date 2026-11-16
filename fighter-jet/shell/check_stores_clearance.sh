#!/usr/bin/env bash
# A4 #122 — assert adjacent store envelopes do not intersect at max deflection.
set -euo pipefail
cd "$(dirname "$0")"
tmpdir=$(mktemp -d)
driver="$(pwd)/.probe_stores.scad"
trap 'rm -rf "$tmpdir"; rm -f "$driver"' EXIT

cat >"$driver" <<'SCAD'
include <lib/stores_clearance.scad>
all_adjacent_forbidden_intersections();
SCAD
log=$tmpdir/clash.log
set +e
openscad -o "$tmpdir/clash.stl" "$driver" >"$log" 2>&1
rc=$?
set -e
if rg -q "Current top level object is empty" "$log"; then
  echo "OK: adjacent store intersections are empty"
  exit 0
fi
echo "FAIL: expected empty adjacent-store clash probe; openscad rc=$rc" >&2
cat "$log" >&2
exit 1
