// ISM-SB-1 subsonic bomber study OML — B1 #38
// Units: mm. Proportion sketch only — not structural authority.
// No stores / munitions geometry.

fuselage_length = 520;
fuselage_d = 48;
wing_span = 360;
wing_root = 90;
wing_tip = 28;
wing_sweep = 28;
wing_z = 22;

module fuselage() {
    hull() {
        translate([40, 0, fuselage_d / 2])
            sphere(d = fuselage_d * 0.7, $fn = 36);
        translate([fuselage_length - 60, 0, fuselage_d / 2])
            scale([1.4, 0.7, 0.7])
                sphere(d = fuselage_d * 0.85, $fn = 36);
    }
}

module wing(side = 1) {
    translate([200, 0, wing_z])
        rotate([0, 0, side * wing_sweep])
            linear_extrude(height = 8, center = true)
                polygon([
                    [0, 0],
                    [wing_root, 0],
                    [wing_root * 0.55, side * wing_span / 2],
                    [wing_root * 0.55 - wing_tip, side * wing_span / 2]
                ]);
}

module empennage() {
    translate([fuselage_length - 80, 0, fuselage_d * 0.9])
        cube([40, 4, 70], center = true);
    translate([fuselage_length - 70, 0, fuselage_d * 0.55])
        cube([35, 90, 4], center = true);
}

echo("B1 #38: subsonic bomber study OML — inert airframe only");
fuselage();
wing(+1);
wing(-1);
empennage();
