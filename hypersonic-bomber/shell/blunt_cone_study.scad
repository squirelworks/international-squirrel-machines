// ISM-HB-1 blunt sphere-cone study OML — #37 deepen
// Educational heat-shield geometry + outer TPS shell offset.
// Units: mm. No weapons / stores / munitions / propulsion solids.

nose_radius = 18;
aft_length = 220;
base_radius = 42;
tps_shell_offset = 3;  // packaging thickness class — not a recipe

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
    // Outer offset shell — TPS packaging sketch only
    difference() {
        blunt_sphere_cone(nose_radius + tps_shell_offset,
                          base_radius + tps_shell_offset,
                          aft_length);
        translate([-1, 0, 0])
            blunt_sphere_cone(nose_radius, base_radius, aft_length + 2);
    }
}

echo("#37: blunt sphere-cone + TPS shell sketch — aerothermal teaching only");
rotate([0, 90, 0]) {
    blunt_sphere_cone(nose_radius, base_radius, aft_length);
    tps_shell();
}
