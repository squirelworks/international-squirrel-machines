#!/usr/bin/env bash
# A2 #120 — assert propulsion keep-outs do not intersect bay / gear wells.
set -euo pipefail
cd "$(dirname "$0")"
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT
driver=$tmpdir/probe_driver.scad
log=$tmpdir/clash.log
# Driver lives under shell/ so include <lib/...> resolves
cat >"$tmpdir/../probe_driver.scad" 2>/dev/null || true
driver="$(pwd)/.probe_driver.scad"
cat >"$driver" <<'SCAD'
include <lib/propulsion_keepouts.scad>
propulsion_forbidden_intersection();
SCAD
trap 'rm -rf "$tmpdir"; rm -f "$driver"' EXIT
set +e
openscad -o "$tmpdir/clash.stl" "$driver" >"$log" 2>&1
rc=$?
set -e
if rg -q "Current top level object is empty" "$log"; then
  echo "OK: propulsion ∩ (bay ∪ gear) is empty"
  exit 0
fi
echo "FAIL: expected empty clash probe; openscad rc=$rc" >&2
cat "$log" >&2
exit 1
