// ISM-SSN-1 station module + structural study — #42
// Units: mm. Habitat + node + truss + ghost berthing rings / board tray.
// No weapons geometry.

module habitat() {
    translate([0, 0, 0])
        rotate([0, 90, 0])
            cylinder(h = 220, d = 80, $fn = 40);
}

module node() {
    translate([200, 0, 0])
        sphere(d = 70, $fn = 36);
}

module lab() {
    translate([260, 0, 0])
        rotate([0, 90, 0])
            cylinder(h = 160, d = 70, $fn = 40);
}

module truss() {
    translate([80, 0, 50])
        cube([200, 12, 12], center = false);
}

module berthing_rings() {
    // Node port stubs — berthing mass/volume only
    for (a = [0, 90, 180, 270])
        rotate([a, 0, 0])
            translate([200, 0, 28])
                rotate([0, 90, 0])
                    cylinder(h = 6, d = 36, center = true, $fn = 28);
}

module truss_longerons() {
    for (y = [-8, 8])
        translate([80, y, 56])
            cube([200, 3, 3]);
}

module hab_board_tray() {
    translate([60, -20, -10])
        cube([50, 40, 4]);
}

module docking_keepouts() {
    translate([200, 40, 0])
        cube([30, 20, 20], center = true);
}

echo("#42: space-station structural study — shells/rings/truss; no weapons solids");
habitat();
node();
lab();
truss();
%berthing_rings();
%truss_longerons();
%hab_board_tray();
%docking_keepouts();
