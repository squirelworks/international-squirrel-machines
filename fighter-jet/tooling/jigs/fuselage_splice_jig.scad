// ISM-FJ-TOOL-010 — Fuselage splice assembly jig (study mm)
// Aligns A01↔A02 at FS-42 and A02↔A03 at FS-72. Issue #106.
// Single manifold solid: X-axis rings seat into saddle with volumetric overlap.

fuse_od = 56;
ring_t = 8;
ring_w = 24;
saddle_h = 40;
base_l = 200;
base_w = 120;
base_t = 12;
pin_d = 6;
overlap = 6;
ring_od = fuse_od + 2 * ring_t;

module splice_ring() {
    // Clamp about fuselage X-axis; radial split for open/close.
    rotate([0, 90, 0])
        difference() {
            cylinder(h = ring_w, d = ring_od, center = true, $fn = 64);
            cylinder(h = ring_w + 2, d = fuse_od, center = true, $fn = 64);
            translate([0, -(fuse_od / 2 + ring_t / 2), 0])
                cube([ring_t + 4, ring_t + 2, ring_w + 2], center = true);
        }
}

module saddle() {
    cube([base_l * 0.4, base_w * 0.5, saddle_h], center = true);
}

module base() {
    difference() {
        cube([base_l, base_w, base_t], center = true);
        for (x = [-60, 60])
            translate([x, 0, 0])
                cylinder(h = base_t + 2, d = pin_d, center = true, $fn = 24);
    }
}

module fuselage_splice_jig() {
    saddle_top = base_t / 2 + saddle_h;
    // Ring OD bottom digs `overlap` into the flat saddle top → one solid
    ring_z = saddle_top - overlap + ring_od / 2;
    union() {
        base();
        // Sink saddle into base by 1 mm so the join is volumetric
        translate([0, 0, base_t / 2 + saddle_h / 2 - 1])
            saddle();
        // Pegs from saddle into each ring (belt-and-suspenders manifold join)
        for (x = [-50, 50]) {
            translate([x, 0, saddle_top - overlap / 2])
                cube([ring_w * 0.6, 16, overlap + 2], center = true);
            translate([x, 0, ring_z])
                splice_ring();
        }
    }
}

fuselage_splice_jig();
