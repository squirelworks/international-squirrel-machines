// ISM-RK-1 hobby rocket study OML + structure — #41
// Units: mm. Fixed fins + ghost bulkheads/rings/motor mount.
// No actuated surfaces / guidance / ballistic geometry.

body_d = 40;
body_l = 560;
nose_l = 90;
motor_tube_d = 24;
ring_zs = [80, 200, 320];

module nose() {
    translate([0, 0, body_l])
        cylinder(h = nose_l, d1 = body_d, d2 = 2, $fn = 36);
}

module body() {
    cylinder(h = body_l, d = body_d, $fn = 36);
}

module fin() {
    translate([body_d / 2 - 1, 0, 20])
        rotate([90, 0, 0])
            linear_extrude(height = 2, center = true)
                polygon([[0, 0], [45, 0], [35, 55], [0, 70]]);
}

module fins() {
    for (a = [0:90:270])
        rotate([0, 0, a])
            fin();
}

module nose_bulkhead() {
    translate([0, 0, body_l - 4])
        cylinder(h = 3, d = body_d - 2, $fn = 36);
}

module avionics_bulkheads() {
    for (z = [body_l - 80, body_l - 120])
        translate([0, 0, z])
            difference() {
                cylinder(h = 2, d = body_d - 2, $fn = 36);
                cylinder(h = 3, d = 12, $fn = 24);
            }
}

module centering_rings() {
    for (z = ring_zs)
        translate([0, 0, z])
            difference() {
                cylinder(h = 3, d = body_d - 2, $fn = 36);
                cylinder(h = 4, d = motor_tube_d + 1, $fn = 28);
            }
}

module motor_mount_tube() {
    translate([0, 0, 40])
        difference() {
            cylinder(h = 300, d = motor_tube_d, $fn = 28);
            cylinder(h = 302, d = motor_tube_d - 3, $fn = 28);
        }
}

module fin_roots() {
    for (a = [0:90:270])
        rotate([0, 0, a])
            translate([body_d / 2 - 4, -1, 25])
                cube([6, 2, 50]);
}

module recovery_bulkhead() {
    translate([0, 0, 360])
        difference() {
            cylinder(h = 3, d = body_d - 2, $fn = 36);
            cylinder(h = 4, d = 8, $fn = 20);
        }
}

echo("#41: rocket structural study — rings/mount/fin roots; no guidance");
body();
nose();
fins();
%nose_bulkhead();
%avionics_bulkheads();
%centering_rings();
%motor_mount_tube();
%fin_roots();
%recovery_bulkhead();
