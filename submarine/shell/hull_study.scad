// ISM-SS-1 submarine hull + structural study — #44
// Units: mm. Printable scale-model proportion sketch.
// Ghost ring frames / casing / sail structure for educational layout.
// No sonar solids — sensors are YAML mass/footprint only.
// No quieting / acoustic / life-support / weapons geometry.

hull_length = 320;
hull_diameter = 40;
ring_count = 8;
ring_spacing = hull_length / (ring_count + 1);

module teardrop_hull() {
    // Axisymmetric teaching form (Albacore-class language)
    hull() {
        translate([12, 0, 0])
            sphere(d = hull_diameter * 0.55, $fn = 40);
        translate([hull_length * 0.35, 0, 0])
            sphere(d = hull_diameter, $fn = 40);
        translate([hull_length - 20, 0, 0])
            sphere(d = hull_diameter * 0.35, $fn = 40);
    }
}

module ring_frames() {
    // Ghost circumferential stiffeners — packaging only, not sized for depth
    for (i = [1:ring_count]) {
        translate([i * ring_spacing, 0, 0])
            rotate([0, 90, 0])
                difference() {
                    cylinder(h = 2, d = hull_diameter * 0.92, center = true, $fn = 36);
                    cylinder(h = 3, d = hull_diameter * 0.72, center = true, $fn = 36);
                }
    }
}

module outer_casing_ghost() {
    // Free-flooding outer fairing stub (textbook two-hull language)
    translate([hull_length * 0.15, 0, -hull_diameter * 0.05])
        scale([1, 1.08, 1.12])
            teardrop_hull();
}

module sail_structure() {
    translate([hull_length * 0.32, 0, hull_diameter * 0.35]) {
        cube([28, 10, 22], center = true);
        // trunk / mast stub — mass/KG only
        translate([0, 0, 14])
            cube([8, 6, 10], center = true);
    }
}

module sternplanes() {
    translate([hull_length - 28, 0, 0]) {
        cube([18, hull_diameter * 1.1, 2], center = true);
        cube([18, 2, hull_diameter * 1.1], center = true);
        // spar stubs through cruciform
        cube([22, 3, 3], center = true);
        cube([3, 3, 22], center = true);
    }
}

module ballast_bay_stubs() {
    // Fore/aft trim volume placeholders — no plumbing
    translate([40, 0, -hull_diameter * 0.15])
        cube([36, 16, 10], center = true);
    translate([hull_length - 55, 0, -hull_diameter * 0.15])
        cube([36, 16, 10], center = true);
}

echo("#44: submarine structural study — rings/casing only; no acoustic/weapons solids");
rotate([0, 90, 0]) {
    // outer casing slightly larger; hull on top for visibility in preview
    %outer_casing_ghost();
    teardrop_hull();
    ring_frames();
    sail_structure();
    sternplanes();
    ballast_bay_stubs();
}
