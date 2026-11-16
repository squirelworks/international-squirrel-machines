// ISM-FJ-TOOL-010 — Fuselage splice assembly jig (study mm)
// Aligns A01↔A02 at FS-42 and A02↔A03 at FS-72. Issue #106.
// Full-scale ≈ ×36.9. Not Eric's CNC — this is the jig geometry only.

fuse_od = 56;
ring_t = 8;
ring_w = 24;
saddle_h = 40;
base_l = 200;
base_w = 120;
base_t = 12;
pin_d = 6;

module splice_ring(label) {
    difference() {
        cylinder(h=ring_w, d=fuse_od + 2*ring_t, center=true, $fn=64);
        cylinder(h=ring_w + 2, d=fuse_od, center=true, $fn=64);
        // hinge split
        translate([0, -fuse_od, 0]) cube([fuse_od*2, fuse_od, ring_w+2], center=true);
    }
    // datum tab
    translate([fuse_od/2 + ring_t, 0, 0])
        cube([12, 20, ring_w], center=true);
}

module saddle() {
    translate([0, 0, -saddle_h/2])
        cube([base_l*0.4, base_w*0.5, saddle_h], center=true);
}

module base() {
    difference() {
        cube([base_l, base_w, base_t], center=true);
        // tooling ball / pin holes at FS refs (symbolic)
        for (x=[-60, 60])
            translate([x, 0, 0]) cylinder(h=base_t+2, d=pin_d, center=true, $fn=24);
    }
}

module fuselage_splice_jig() {
    base();
    translate([0, 0, base_t/2 + saddle_h/2]) saddle();
    translate([-50, 0, base_t/2 + saddle_h + fuse_od/2]) splice_ring("FS-42");
    translate([50, 0, base_t/2 + saddle_h + fuse_od/2]) splice_ring("FS-72");
}

fuselage_splice_jig();
