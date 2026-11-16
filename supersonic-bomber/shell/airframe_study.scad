// ISM-XB-1 supersonic bomber study OML — #39 deepen
// Units: mm. Slender OML + inert bay volume box.
// No munitions / seeker / guidance geometry. No hypersonic TPS solids.

fuselage_length = 480;
fuselage_d = 42;
wing_span = 240;
wing_root = 120;
wing_tip = 20;
wing_sweep = 45;
wing_z = 18;

module fuselage() {
    hull() {
        translate([30, 0, fuselage_d / 2])
            scale([1.2, 0.55, 0.55])
                sphere(d = fuselage_d, $fn = 36);
        translate([fuselage_length - 50, 0, fuselage_d / 2])
            scale([1.6, 0.5, 0.5])
                sphere(d = fuselage_d * 0.75, $fn = 36);
    }
}

module wing(side = 1) {
    translate([160, 0, wing_z])
        rotate([0, 0, side * wing_sweep])
            linear_extrude(height = 6, center = true)
                polygon([
                    [0, 0],
                    [wing_root, 0],
                    [wing_root * 0.35, side * wing_span / 2],
                    [wing_root * 0.35 - wing_tip, side * wing_span / 2]
                ]);
}

module empennage() {
    translate([fuselage_length - 70, 0, fuselage_d])
        cube([50, 3, 65], center = true);
    translate([fuselage_length - 55, 0, fuselage_d * 0.5])
        cube([40, 70, 3], center = true);
}

module inert_bay_volume() {
    // BAY-MAIN keep-out — packaging only
    translate([200, -15, 6])
        cube([140, 30, 24]);
}

echo("#39: supersonic bomber study — inert bay only; no munitions/hypersonic TPS");
fuselage();
wing(+1);
wing(-1);
empennage();
inert_bay_volume();
