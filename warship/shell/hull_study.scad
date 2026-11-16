// ISM-WS-1 warship hull + structural study — #43
// Units: mm study model. Public-domain proportion sketch + ghost frames/keel.
// No weapons geometry — combat items are YAML mass/footprint boxes only.

hull_length = 400;
hull_beam   = 52;
hull_depth  = 36;
draft       = 18;
frame_count = 8;

module hull_body() {
    hull() {
        translate([20, 0, draft])
            scale([1.2, 0.45, 0.7])
                sphere(d = hull_beam * 0.9, $fn = 36);
        translate([hull_length * 0.45, 0, draft])
            scale([1.0, 0.55, 0.85])
                sphere(d = hull_beam, $fn = 36);
        translate([hull_length - 30, 0, draft + 2])
            scale([1.3, 0.4, 0.65])
                sphere(d = hull_beam * 0.75, $fn = 36);
    }
}

module deck_box() {
    translate([80, -hull_beam * 0.22, hull_depth - 4])
        cube([hull_length * 0.55, hull_beam * 0.44, 8]);
}

module superstructure_stub() {
    translate([150, -18, hull_depth + 4])
        cube([80, 36, 28]);
}

module keel() {
    translate([30, -2, draft - 4])
        cube([hull_length - 60, 4, 6]);
}

module transverse_frames() {
    for (i = [1:frame_count]) {
        x = 40 + i * (hull_length - 80) / (frame_count + 1);
        translate([x, -hull_beam * 0.28, 4])
            difference() {
                cube([3, hull_beam * 0.56, hull_depth - 2]);
                translate([-1, hull_beam * 0.12, draft - 2])
                    cube([5, hull_beam * 0.32, hull_depth]);
            }
    }
}

module deck_beams() {
    for (i = [0:5]) {
        translate([90 + i * 30, -hull_beam * 0.2, hull_depth - 2])
            cube([3, hull_beam * 0.4, 3]);
    }
}

module longitudinal_bulkheads() {
    translate([60, -hull_beam * 0.08, 6])
        cube([hull_length - 120, 2, hull_depth - 10]);
    translate([60, hull_beam * 0.06, 6])
        cube([hull_length - 120, 2, hull_depth - 10]);
}

module transverse_bulkheads() {
    for (x = [100, 200, 300]) {
        translate([x, -hull_beam * 0.25, 6])
            cube([3, hull_beam * 0.5, hull_depth - 10]);
    }
}

module actuator_foundations() {
    // Thruster / rudder scale-model mounts — packaging only
    translate([hull_length - 45, -8, 2])
        cube([20, 16, 8]);
    translate([hull_length - 35, -3, draft - 6])
        cube([12, 6, 10]);
}

echo("#43: warship structural study — frames/keel only; no weapons solids");
hull_body();
deck_box();
superstructure_stub();
%keel();
%transverse_frames();
%deck_beams();
%longitudinal_bulkheads();
%transverse_bulkheads();
%actuator_foundations();
