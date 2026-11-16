// ISM-MS-1 mobile suit frame study — #46
// Units: mm. Torso + limbs packaging sketch.
// Stores = inert mass boxes only — no munition geometry.

module torso() {
    cube([80, 50, 100], center = true);
}

module head() {
    translate([0, 0, 65])
        sphere(d = 36, $fn = 28);
}

module limb(len) {
    cylinder(h = len, d = 18, $fn = 20);
}

module legs() {
    translate([-22, 0, -50]) rotate([180, 0, 0]) limb(90);
    translate([22, 0, -50]) rotate([180, 0, 0]) limb(90);
}

module arms() {
    translate([-50, 0, 20]) rotate([0, 90, 0]) limb(70);
    translate([50, 0, 20]) rotate([0, -90, 0]) limb(70);
}

module dorsal_inert_box() {
    // Inert stores mass box — packaging only
    translate([0, -40, 10])
        cube([50, 20, 40], center = true);
}

echo("#46: gundam frame study — mecha packaging; stores inert mass only");
torso();
head();
legs();
arms();
dorsal_inert_box();
