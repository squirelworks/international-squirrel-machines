// ISM-FJ-TOOL-010 — Fuselage splice assembly jig (study mm)
// Aligns A01↔A02 at FS-42 and A02↔A03 at FS-72. Issue #106.
// Single manifold solid: rings seat on saddle with overlap; split cuts through wall.

fuse_od = 56;
ring_t = 8;
ring_w = 24;
saddle_h = 40;
base_l = 200;
base_w = 120;
base_t = 12;
pin_d = 6;
overlap = 2;

module splice_ring() {
    difference() {
        union() {
            cylinder(h = ring_w, d = fuse_od + 2 * ring_t, center = true, $fn = 64);
            translate([fuse_od / 2 + ring_t, 0, 0])
                cube([12, 20, ring_w], center = true);
        }
        cylinder(h = ring_w + 2, d = fuse_od, center = true, $fn = 64);
        // Radial slot through wall (not tangent skim)
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
    union() {
        base();
        translate([0, 0, base_t / 2 + saddle_h / 2])
            saddle();
        // Ring OD rests on saddle top with overlap into saddle
        saddle_top = base_t / 2 + saddle_h;
        ring_z = saddle_top + (fuse_od / 2 + ring_t) - overlap;
        translate([-50, 0, ring_z]) splice_ring();
        translate([50, 0, ring_z]) splice_ring();
    }
}

fuselage_splice_jig();
