// ISM-FJ-TOOL-040 — Drill/rivet edge fixture (study mm). Issue #106.
// Clamps skin/longeron stack; bushing holes at rivet pitch.

pitch = 20;
holes = 8;
bush_id = 3.2;
bush_od = 8;
clamp_w = 40;
clamp_l = pitch * (holes - 1) + 40;
clamp_t = 16;

module drill_rivet_fixture() {
    difference() {
        cube([clamp_l, clamp_w, clamp_t], center=true);
        // work slot
        translate([0, 0, clamp_t/4])
            cube([clamp_l - 20, 12, clamp_t], center=true);
        // bushing holes
        for (i=[0:holes-1]) {
            x = -pitch*(holes-1)/2 + i*pitch;
            translate([x, 0, 0])
                cylinder(h=clamp_t+2, d=bush_id, center=true, $fn=24);
            translate([x, 0, clamp_t/2 - 2])
                cylinder(h=4, d=bush_od, center=true, $fn=24);
        }
    }
}

drill_rivet_fixture();
