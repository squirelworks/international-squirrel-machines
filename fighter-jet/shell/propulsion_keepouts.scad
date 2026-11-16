// ISM-FJ-1 propulsion packaging keep-outs (study mm) — A2 #120
// Scale factor 36.9 from full-scale. Packaging check only — not engine CAD.
// Library modules only — render via propulsion_keepouts_preview.scad or intersection_check.

fuselage_length = 420;
fuselage_height = 56;
function fs_x(pct) = fuselage_length * pct;

eng_len = 106;
eng_dia = 22;
eng_y_off = 14;
eng_z = fuselage_height * 0.38;
eng_x0 = fs_x(0.82);

// Ducts FS-62→FS-82: outboard and above MLG wells
duct_x0 = fs_x(0.62);
duct_dia = 14;
duct_y = 26;
duct_z = 42;

module engine_envelope(side = 1) {
    translate([eng_x0, side * eng_y_off, eng_z])
        rotate([0, 90, 0])
            cylinder(h = eng_len, d = eng_dia, $fn = 32);
}

module inlet_duct(side = 1) {
    hull() {
        translate([duct_x0, side * duct_y, duct_z])
            rotate([0, 90, 0]) cylinder(h = 1, d = duct_dia, $fn = 24);
        translate([eng_x0, side * eng_y_off, eng_z])
            rotate([0, 90, 0]) cylinder(h = 1, d = eng_dia * 0.9, $fn = 24);
    }
}

module nozzle_stub(side = 1) {
    translate([eng_x0 + eng_len - 2, side * eng_y_off, eng_z])
        rotate([0, 90, 0])
            cylinder(h = 20, d = eng_dia * 0.95, $fn = 24);
}

module propulsion_keepouts() {
    union() {
        engine_envelope(+1);
        engine_envelope(-1);
        inlet_duct(+1);
        inlet_duct(-1);
        nozzle_stub(+1);
        nozzle_stub(-1);
    }
}

module avionics_bay_volume() {
    nose_length = 90;
    translate([nose_length + 30, -40, fuselage_height - 18])
        cube([120, 80, 20]);
}

module gear_well_volumes() {
    translate([55, -12, 5]) cube([40, 24, 28]);
    translate([200, -30, 5]) cube([60, 25, 32]);
    translate([200, 5, 5]) cube([60, 25, 32]);
}

module forbidden_volumes() {
    union() {
        avionics_bay_volume();
        gear_well_volumes();
    }
}

module propulsion_forbidden_intersection() {
    intersection() {
        propulsion_keepouts();
        forbidden_volumes();
    }
}
