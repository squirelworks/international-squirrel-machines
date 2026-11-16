// A2 #120 — clash probe modules only (cad-verify LIB).
// Empty-intersection assert is driven by check_propulsion_packaging.sh, which
// writes a tiny driver scad calling propulsion_forbidden_intersection().
// Do not add top-level geometry here — OpenSCAD empty object fails cad-verify.

include <propulsion_keepouts.scad>

// Re-export for drivers / docs
module propulsion_clash_probe() {
    propulsion_forbidden_intersection();
}
