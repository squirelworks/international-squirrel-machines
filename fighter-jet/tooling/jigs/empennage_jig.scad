// ISM-FJ-TOOL-030 — Empennage assembly jig (study mm). Issue #106.
// Manifold solid: HT cradles seat into base with overlap.

ht_span = 100;
ht_chord = 50;
vt_h = 70;
vt_chord = 60;
base_t = 12;
cradle_d = 10;
overlap = 2;

module empennage_jig() {
    union() {
        cube([vt_chord + 80, ht_span + 60, base_t], center = true);
        // VT spar posts — rooted in base
        translate([-10, 0, base_t / 2 + vt_h / 2 - overlap])
            cube([8, 8, vt_h + overlap], center = true);
        translate([20, 0, base_t / 2 + vt_h / 2 - overlap])
            cube([8, 8, vt_h + overlap], center = true);
        // HT hinge cradles — axis at base top + radius - overlap
        cradle_z = base_t / 2 + cradle_d / 2 - overlap;
        for (s = [-1, 1])
            translate([0, s * ht_span / 2, cradle_z])
                rotate([0, 90, 0])
                    cylinder(h = ht_chord, d = cradle_d, center = true, $fn = 32);
    }
}

empennage_jig();
