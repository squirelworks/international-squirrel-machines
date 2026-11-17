// ISM-FJ-TOOL-080 — Inlet duct layup mandrel (male, study mm). Issue #106 / 4b.
// Side/under intake duct study form; not LO recipe — packaging mandrel only.

duct_l = 120;
throat_d = 28;
lip_d = 40;
wall_pad = 6;

module intake_layup_mandrel() {
    union() {
        // tapered duct body
        hull() {
            translate([0, 0, 0])
                cylinder(h = 2, d = lip_d, center = true, $fn = 48);
            translate([duct_l, 0, 0])
                cylinder(h = 2, d = throat_d, center = true, $fn = 48);
        }
        // lip flange
        translate([0, 0, 0])
            cylinder(h = wall_pad, d = lip_d + 12, center = true, $fn = 48);
        // handle / vacuum boss at throat end
        translate([duct_l, 0, 0])
            cylinder(h = 16, d = 12, center = true, $fn = 32);
    }
}

intake_layup_mandrel();
