// ISM-MS-1 mobile suit frame + structural study — #46
// Units: mm. Torso + limbs + ghost spars / joints / board tray.
// Stores = inert mass boxes / pads only — no munition geometry.

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

module torso_frame_spars() {
    for (x = [-20, 20])
        translate([x, 0, 0])
            cube([4, 10, 90], center = true);
}

module limb_spars() {
    translate([-22, 0, -95]) cylinder(h = 80, d = 6, $fn = 12);
    translate([22, 0, -95]) cylinder(h = 80, d = 6, $fn = 12);
}

module joint_stubs() {
    for (p = [[-22, 0, -50], [22, 0, -50], [-45, 0, 20], [45, 0, 20]])
        translate(p) sphere(d = 22, $fn = 20);
}

module armor_keepouts() {
    translate([0, 0, 0])
        cube([92, 58, 110], center = true);
}

module control_board_tray() {
    translate([0, 15, -10])
        cube([50, 30, 4], center = true);
}

module stores_hardpoint_pads() {
    translate([0, -52, 10])
        cube([40, 4, 30], center = true);
}

echo("#46: gundam structural study — spars/joints/tray; stores inert mass only");
torso();
head();
legs();
arms();
dorsal_inert_box();
%torso_frame_spars();
%limb_spars();
%joint_stubs();
%armor_keepouts();
%control_board_tray();
%stores_hardpoint_pads();
