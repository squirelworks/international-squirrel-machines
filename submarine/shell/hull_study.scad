// ISM-SS-1 submarine hull study — B3 #44
// Units: mm. Printable scale-model proportion sketch.
// No sonar solids — sensors are YAML mass/footprint only.
// No quieting / acoustic / life-support geometry.

hull_length = 320;
hull_diameter = 40;

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

module sail_stub() {
    translate([hull_length * 0.32, 0, hull_diameter * 0.35])
        cube([28, 10, 22], center = true);
}

module sternplanes() {
    translate([hull_length - 28, 0, 0]) {
        cube([18, hull_diameter * 1.1, 2], center = true);
        cube([18, 2, hull_diameter * 1.1], center = true);
    }
}

echo("B3 #44: submarine hull study — trim/hull only; no acoustic solids");
rotate([0, 90, 0]) {
    teardrop_hull();
    sail_stub();
    sternplanes();
}
