// ISM-RK-1 hobby rocket study OML — B4 #41
// Units: mm. Fixed fins — no actuated surfaces / guidance geometry.

body_d = 40;
body_l = 560;
nose_l = 90;

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

echo("B4 #41: hobby rocket study — passive/fixed; no guidance geometry");
body();
nose();
fins();
