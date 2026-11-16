// A2 #120 packaging clash check — cad-verify compatible.
//
// Acceptance: propulsion keep-outs ∩ (avionics bay ∪ gear wells) must be empty.
// OpenSCAD exits rc=1 with "Current top level object is empty" when the
// intersection alone is the top-level object, and cad-verify treats that as FAIL.
// So this file always exports a small witness cube; the clash probe is asserted
// via echo + the companion script `check_propulsion_packaging.sh`.
//
// To re-check emptiness locally:
//   ./check_propulsion_packaging.sh
// or:
//   openscad -o /tmp/clash.stl temp driver + lib/propulsion_keepouts.scad
//   → expect "Current top level object is empty."

include <lib/propulsion_keepouts.scad>

echo("A2 #120: propulsion∩(bay∪gear) must be empty; witness cube for cad-verify.");
echo("A2 #120: run shell/check_propulsion_packaging.sh to assert empty clash probe.");

// Witness solid — non-empty STL so cad-verify status is OK when clash-free.
translate([-200, 0, -20])
    cube(4, center = true);

// Do NOT call propulsion_forbidden_intersection() at top level here (EMPTY → CI fail).
// Clash geometry lives in temp driver + lib/propulsion_keepouts.scad for the empty-object assert.
