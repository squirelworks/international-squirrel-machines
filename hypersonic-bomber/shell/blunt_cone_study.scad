// ISM-HB-1 blunt sphere-cone study OML — B1 #37
// Educational heat-shield geometry only. Units: mm.
// Not a weapons airframe; no stores / bays / munitions geometry.

/* [Nose / cone] */
nose_radius = 18;       // blunt sphere radius
cone_half_angle = 10;   // degrees
aft_length = 220;       // cone frustum length along axis
base_radius = 42;

module blunt_sphere_cone() {
    // Forward hemisphere (blunt nose)
    translate([0, 0, 0])
        sphere(r = nose_radius, $fn = 48);

    // Cone from sphere tangent plane aft
    // Simple teaching solid: cylinder taper (frustum) behind nose
    hull() {
        translate([0, 0, 0])
            sphere(r = nose_radius * 0.98, $fn = 48);
        translate([aft_length, 0, 0])
            rotate([0, 90, 0])
                cylinder(h = 1, r = base_radius, $fn = 48);
    }
}

echo("B1 #37: blunt sphere-cone study — TPS packaging sketch only");
rotate([0, 90, 0])
    blunt_sphere_cone();
