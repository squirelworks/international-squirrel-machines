// ISM-SB-1 subsonic bomber study OML + structure — #38
// Units: mm. Proportion sketch + inert bay + ghost spars/ribs/frames.
// No munitions / seeker / guidance / live-ejector geometry.

fuselage_length = 520;
fuselage_d = 48;
wing_span = 360;
wing_root = 90;
wing_tip = 28;
wing_sweep = 28;
wing_z = 22;
bay_x = 240;
bay_l = 160;
bay_w = 36;
bay_h = 28;

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

module inert_bay_volume() {
    // BAY-MAIN keep-out / mass volume — packaging only
    translate([bay_x, -bay_w / 2, 8])
        cube([bay_l, bay_w, bay_h]);
}

module wing_spars(side = 1) {
    // Ghost front/rear spars — educational layout only
    translate([200, 0, wing_z])
        rotate([0, 0, side * wing_sweep]) {
            translate([12, 0, 0])
                cube([4, abs(side) * wing_span / 2, 6]);
            translate([wing_root * 0.45, 0, 0])
                cube([4, abs(side) * wing_span / 2 * 0.85, 5]);
        }
}

module wing_ribs(side = 1) {
    for (i = [1:6]) {
        y = side * (i * wing_span / 14);
        translate([200 + 8, y, wing_z])
            rotate([0, 0, side * wing_sweep])
                cube([wing_root * 0.5, 2, 7], center = true);
    }
}

module carry_through() {
    translate([200, -fuselage_d * 0.35, wing_z - 2])
        cube([50, fuselage_d * 0.7, 8]);
}

module fuselage_frames() {
    // Station frames; skip bay cutout region
    for (x = [80, 140, 200, 420, 470]) {
        translate([x, -fuselage_d * 0.35, 4])
            difference() {
                cube([3, fuselage_d * 0.7, fuselage_d * 0.75]);
                if (x >= bay_x && x <= bay_x + bay_l)
                    translate([-1, fuselage_d * 0.15, 4])
                        cube([5, bay_w, bay_h]);
            }
    }
}

module longerons() {
    // Route around bay keep-out
    translate([60, -bay_w / 2 - 4, 10])
        cube([fuselage_length - 120, 3, 3]);
    translate([60, bay_w / 2 + 1, 10])
        cube([fuselage_length - 120, 3, 3]);
}

module gear_attach() {
    // NLG / MLG hardpoint stubs — runway only
    translate([90, 0, 2])
        cube([16, 12, 6], center = true);
    translate([280, -22, 2])
        cube([20, 10, 6], center = true);
    translate([280, 22, 2])
        cube([20, 10, 6], center = true);
}

echo("#38: subsonic bomber structural study — inert bay keep-out; no munitions");
fuselage();
wing(+1);
wing(-1);
empennage();
inert_bay_volume();
%wing_spars(+1);
%wing_spars(-1);
%wing_ribs(+1);
%wing_ribs(-1);
%carry_through();
%fuselage_frames();
%longerons();
%gear_attach();
