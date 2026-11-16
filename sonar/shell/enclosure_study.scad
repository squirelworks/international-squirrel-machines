// ISM-SNR-1 sonar enclosure + structural study — #40
// Units: mm. Handheld box + transducer face + ghost ribs/tray/bezel.
// No quieting geometry, array SP, or weapons solids.

module enclosure_body() {
    difference() {
        cube([120, 70, 40], center = true);
        translate([0, 0, 4])
            cube([108, 58, 36], center = true);
    }
}

module transducer_face() {
    translate([0, -40, 0])
        rotate([90, 0, 0])
            cylinder(h = 12, d = 50, $fn = 40);
}

module display_window() {
    translate([0, 10, 18])
        cube([60, 30, 4], center = true);
}

module enclosure_ribs() {
    for (x = [-40, 0, 40])
        translate([x, 0, -8])
            cube([3, 50, 20], center = true);
}

module echo_board_tray() {
    translate([0, 5, -12])
        cube([80, 40, 3], center = true);
}

module display_bezel() {
    translate([0, 10, 20])
        difference() {
            cube([66, 36, 3], center = true);
            cube([54, 24, 4], center = true);
        }
}

module hull_mount_pads() {
    for (xy = [[-45, -25], [45, -25], [-45, 25], [45, 25]])
        translate([xy[0], xy[1], -22])
            cylinder(h = 4, d = 10, $fn = 20);
}

echo("#40: sonar structural study — ribs/tray/bezel; no quieting/weapons");
enclosure_body();
transducer_face();
display_window();
%enclosure_ribs();
%echo_board_tray();
%display_bezel();
%hull_mount_pads();
