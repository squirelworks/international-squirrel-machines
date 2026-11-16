// ISM-FJ-TOOL-030 — Empennage assembly jig (study mm). Issue #106.

ht_span = 100;
ht_chord = 50;
vt_h = 70;
vt_chord = 60;
base_t = 12;

module empennage_jig() {
    // base
    cube([vt_chord + 80, ht_span + 60, base_t], center=true);
    // VT spar posts
    translate([-10, 0, vt_h/2]) cube([8, 8, vt_h], center=true);
    translate([20, 0, vt_h/2]) cube([8, 8, vt_h], center=true);
    // HT hinge line cradles
    for (s=[-1, 1])
        translate([0, s*ht_span/2, 20])
            rotate([0, 90, 0]) cylinder(h=ht_chord, d=10, center=true, $fn=32);
}

empennage_jig();
