// ISM-FJ-TOOL-070 — Canopy bubble layup mandrel (male, study mm). Issue #106 / 4b.
// Convex form for educational canopy skin layup; vacuum boss sinks into face.

canopy_l = 90;
canopy_w = 48;
canopy_h = 28;
base_t = 10;
boss_sink = 2;

module canopy_layup_mandrel() {
    union() {
        // pedestal
        translate([0, 0, -base_t / 2])
            cube([canopy_l + 20, canopy_w + 20, base_t], center = true);
        // bubble form
        scale([canopy_l / 2, canopy_w / 2, canopy_h])
            sphere(r = 1, $fn = 48);
        // vacuum boss
        translate([0, 0, canopy_h * 0.55 - boss_sink])
            cylinder(h = 8 + boss_sink, d = 14, $fn = 32);
    }
}

canopy_layup_mandrel();
