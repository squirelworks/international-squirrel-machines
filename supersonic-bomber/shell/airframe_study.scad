// ISM-XB-1 supersonic bomber study OML + structure — #39
// Units: mm. Slender OML + inert bay + ghost spars/ribs/frames.
// No munitions / seeker / guidance / live-ejector geometry. No hypersonic TPS solids.

fuselage_length = 480;
fuselage_d = 42;
wing_span = 240;
wing_root = 120;
wing_tip = 20;
wing_sweep = 45;
wing_z = 18;
bay_x = 200;
bay_l = 140;
bay_w = 30;
bay_h = 24;

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
    translate([bay_x, -bay_w / 2, 6])
        cube([bay_l, bay_w, bay_h]);
}

module wing_spars(side = 1) {
    translate([160, 0, wing_z])
        rotate([0, 0, side * wing_sweep]) {
            translate([14, 0, 0])
                cube([4, abs(side) * wing_span / 2, 5]);
            translate([wing_root * 0.4, 0, 0])
                cube([4, abs(side) * wing_span / 2 * 0.8, 4]);
        }
}

module wing_ribs(side = 1) {
    for (i = [1:5]) {
        y = side * (i * wing_span / 12);
        translate([160 + 10, y, wing_z])
            rotate([0, 0, side * wing_sweep])
                cube([wing_root * 0.4, 2, 6], center = true);
    }
}

module carry_through() {
    translate([160, -fuselage_d * 0.3, wing_z - 2])
        cube([45, fuselage_d * 0.6, 7]);
}

module fuselage_frames() {
    for (x = [70, 120, 170, 360, 410]) {
        translate([x, -fuselage_d * 0.3, 3])
            difference() {
                cube([3, fuselage_d * 0.6, fuselage_d * 0.7]);
                if (x >= bay_x && x <= bay_x + bay_l)
                    translate([-1, fuselage_d * 0.12, 3])
                        cube([5, bay_w, bay_h]);
            }
    }
}

module longerons() {
    translate([50, -bay_w / 2 - 3, 9])
        cube([fuselage_length - 100, 2.5, 2.5]);
    translate([50, bay_w / 2 + 0.5, 9])
        cube([fuselage_length - 100, 2.5, 2.5]);
}

module gear_attach() {
    translate([80, 0, 2])
        cube([14, 10, 5], center = true);
    translate([250, -18, 2])
        cube([18, 8, 5], center = true);
    translate([250, 18, 2])
        cube([18, 8, 5], center = true);
}

echo("#39: supersonic bomber structural study — inert bay keep-out; no munitions");
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
