// ISM-FJ-1 adjacent-store clearance envelopes — A4 #122
// Study mm. Inert fit / clearance only — no release kinematics.
// Library modules only.

fuselage_length = 420;
function fs_x(pct) = fuselage_length * pct;

// Station BL/WL from hardpoints.yaml; store body = study-scaled class cylinder
// Full-scale AAM-S ~2.9 m × 0.127 m → study ≈ /36.9 → L~79 mm, D~3.4 mm
// Use exaggerated study envelopes for clash visibility at wing stations.

module store_envelope(bl, wl, fs_pct, dia = 8, len = 60) {
    translate([fs_x(fs_pct) - len / 2, bl, wl - dia / 2])
        rotate([0, 90, 0])
            cylinder(h = len, d = dia, $fn = 24);
}

// Tip + outboard adjacent pair (left wing) at max flap/gear deflection stub:
// deflect BL 3 mm toward neighbor to stress clearance gap.
module adjacent_pair_sta1_sta3(deflect_mm = 3) {
    store_envelope(-140 + deflect_mm, -6, 0.58, 8, 60);  // STA-1
    store_envelope(-105 - deflect_mm, -8, 0.60, 10, 70); // STA-3
}

module adjacent_pair_sta3_sta5(deflect_mm = 3) {
    store_envelope(-105 + deflect_mm, -8, 0.60, 10, 70);
    store_envelope(-70 - deflect_mm, -10, 0.61, 12, 80);
}

module adjacent_pair_sta5_sta7(deflect_mm = 3) {
    store_envelope(-70 + deflect_mm, -10, 0.61, 12, 80);
    store_envelope(-35 - deflect_mm, -12, 0.62, 14, 90);
}

module adjacent_pair_sta7_sta9(deflect_mm = 3) {
    store_envelope(-35 + deflect_mm, -12, 0.62, 14, 90);
    store_envelope(0, -28, 0.55, 16, 100);  // STA-9 CL
}

module pair_intersection_1_3() {
    intersection() {
        store_envelope(-140 + 3, -6, 0.58, 8, 60);
        store_envelope(-105 - 3, -8, 0.60, 10, 70);
    }
}

module pair_intersection_3_5() {
    intersection() {
        store_envelope(-105 + 3, -8, 0.60, 10, 70);
        store_envelope(-70 - 3, -10, 0.61, 12, 80);
    }
}

module pair_intersection_5_7() {
    intersection() {
        store_envelope(-70 + 3, -10, 0.61, 12, 80);
        store_envelope(-35 - 3, -12, 0.62, 14, 90);
    }
}

module pair_intersection_7_9() {
    intersection() {
        store_envelope(-35 + 3, -12, 0.62, 14, 90);
        store_envelope(0, -28, 0.55, 16, 100);
    }
}

module all_adjacent_forbidden_intersections() {
    union() {
        pair_intersection_1_3();
        pair_intersection_3_5();
        pair_intersection_5_7();
        pair_intersection_7_9();
    }
}
