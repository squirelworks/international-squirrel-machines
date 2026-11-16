// ISM-HB-1 blunt sphere-cone + structural study — #37
// Educational heat-shield geometry + outer TPS shell + ghost frames/rails.
// Units: mm. No weapons / stores / munitions / propulsion / TPS-recipe solids.

nose_radius = 18;
aft_length = 220;
base_radius = 42;
tps_shell_offset = 3;  // packaging thickness class — not a recipe
ring_count = 6;

module blunt_sphere_cone(r_nose, r_base, len) {
    hull() {
        translate([0, 0, 0])
            sphere(r = r_nose, $fn = 48);
        translate([len, 0, 0])
            rotate([0, 90, 0])
                cylinder(h = 1, r = r_base, $fn = 48);
    }
}

module tps_shell() {
    difference() {
        blunt_sphere_cone(nose_radius + tps_shell_offset,
                          base_radius + tps_shell_offset,
                          aft_length);
        translate([-1, 0, 0])
            blunt_sphere_cone(nose_radius, base_radius, aft_length + 2);
    }
}

module nose_bulkhead() {
    translate([nose_radius * 0.6, 0, 0])
        rotate([0, 90, 0])
            cylinder(h = 2, r = nose_radius * 0.85, center = true, $fn = 36);
}

module ring_frames() {
    for (i = [1:ring_count]) {
        x = nose_radius + i * (aft_length - nose_radius) / (ring_count + 1);
        // linear radius growth along cone
        r = nose_radius + (base_radius - nose_radius) * (x / aft_length);
        translate([x, 0, 0])
            rotate([0, 90, 0])
                difference() {
                    cylinder(h = 2, r = r * 0.92, center = true, $fn = 36);
                    cylinder(h = 3, r = r * 0.72, center = true, $fn = 36);
                }
    }
}

module longerons() {
    for (a = [0, 90, 180, 270]) {
        rotate([a, 0, 0])
            translate([nose_radius, base_radius * 0.55, 0])
                cube([aft_length - nose_radius - 10, 2, 2]);
    }
}

module tps_attach_rails() {
    // Packaging rails under shell — class placeholder only
    for (a = [45, 135, 225, 315]) {
        rotate([a, 0, 0])
            translate([nose_radius + 10, base_radius * 0.7, 0])
                cube([aft_length - nose_radius - 30, 1.5, 1.5]);
    }
}

module aft_bulkhead() {
    translate([aft_length - 4, 0, 0])
        rotate([0, 90, 0])
            cylinder(h = 3, r = base_radius * 0.9, center = true, $fn = 36);
}

module thermal_board_tray() {
    // KiCad thermal-board mount stub near mid-body
    translate([aft_length * 0.45, 0, -base_radius * 0.25])
        cube([40, 28, 3], center = true);
}

echo("#37: hypersonic structural study — frames under TPS shell; no weapons/recipes");
rotate([0, 90, 0]) {
    blunt_sphere_cone(nose_radius, base_radius, aft_length);
    tps_shell();
    %nose_bulkhead();
    %ring_frames();
    %longerons();
    %tps_attach_rails();
    %aft_bulkhead();
    %thermal_board_tray();
}
