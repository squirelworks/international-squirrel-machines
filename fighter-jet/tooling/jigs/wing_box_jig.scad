// ISM-FJ-TOOL-020 — Wing box assembly jig (right wing, study mm)
// Single manifold solid: cradles/posts rooted into base plate.

root_chord = 110;
tip_chord = 45;
semi_span = 140;
spar_front_pct = 0.15;
spar_rear_pct = 0.65;
beam_t = 10;
post_h = 50;
base_t = 12;
overlap = 3;

module spar_cradle(x0, x1, y0, y1) {
    hull() {
        translate([x0, y0, 0]) cube([beam_t, beam_t, post_h], center = true);
        translate([x1, y1, 0]) cube([beam_t, beam_t, post_h], center = true);
    }
}

module rib_post(y, chord) {
    translate([chord * 0.4, y, 0])
        cylinder(h = post_h, d = 8, center = true, $fn = 24);
}

module wing_box_jig() {
    union() {
        translate([root_chord / 2, semi_span / 2, -post_h / 2 - base_t / 2 + overlap])
            cube([root_chord + 40, semi_span + 40, base_t + overlap], center = true);
        spar_cradle(root_chord * spar_front_pct, tip_chord * spar_front_pct + 20, 0, semi_span);
        spar_cradle(root_chord * spar_rear_pct, tip_chord * spar_rear_pct + 40, 0, semi_span);
        for (i = [0:5]) {
            y = i * semi_span / 5;
            c = root_chord + (tip_chord - root_chord) * (i / 5);
            rib_post(y, c);
        }
    }
}

wing_box_jig();
