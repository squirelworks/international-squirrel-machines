// A4 #122 — adjacent store clearance (cad-verify compatible).
// Witness cube; emptiness via check_stores_clearance.sh.

include <lib/stores_clearance.scad>

echo("A4 #122: adjacent store ∩ at max deflection must be empty; witness for CI.");
echo("A4 #122: run shell/check_stores_clearance.sh");

translate([-200, 20, -20])
    cube(4, center = true);
