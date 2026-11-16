#!/usr/bin/env bash
# A4 #122 — assert aperture ∩ keep-outs empty and R1 contained in nose.
set -euo pipefail
cd "$(dirname "$0")"
tmpdir=$(mktemp -d)
driver="$(pwd)/.probe_sensor.scad"
trap 'rm -rf "$tmpdir"; rm -f "$driver"' EXIT

run_probe() {
  local module=$1
  local label=$2
  cat >"$driver" <<SCAD
include <lib/sensor_aperture_keepouts.scad>
${module}();
SCAD
  local log=$tmpdir/${module}.log
  set +e
  openscad -o "$tmpdir/${module}.stl" "$driver" >"$log" 2>&1
  local rc=$?
  set -e
  if rg -q "Current top level object is empty" "$log"; then
    echo "OK: $label is empty"
    return 0
  fi
  echo "FAIL: expected empty $label; openscad rc=$rc" >&2
  cat "$log" >&2
  return 1
}

run_probe sensor_forbidden_intersection "aperture ∩ structural keep-outs"
run_probe radar_outside_nose "R1 outside nose interior"
echo "OK: sensor aperture packaging checks passed"
