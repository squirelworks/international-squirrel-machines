// ISM-SNR-1 sonar enclosure study — #40
// Units: mm. Handheld box + transducer face keepout.
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

echo("#40: sonar enclosure study — educational echo-sounder; no quieting/weapons");
enclosure_body();
transducer_face();
display_window();
