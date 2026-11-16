// ISM-SSN-1 station module study — #42
// Units: mm. Habitat + node + truss packaging sketch.
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

echo("#42: space-station module study — civil habitat; no weapons solids");
habitat();
node();
lab();
truss();
