// ISM-FJ-TOOL-020 — Wing box assembly jig (right wing, study mm)
// Holds front/rear spars at 15%/65% chord; ribs at WS stations. Issue #106.

root_chord = 110;
tip_chord = 45;
semi_span = 140;
spar_front_pct = 0.15;
spar_rear_pct = 0.65;
beam_t = 10;
post_h = 50;

module spar_cradle(x0, x1, y0, y1) {
    hull() {
        translate([x0, y0, 0]) cube([beam_t, beam_t, post_h], center=true);
        translate([x1, y1, 0]) cube([beam_t, beam_t, post_h], center=true);
    }
}

module rib_post(y, chord) {
    translate([chord*0.4, y, 0])
        cylinder(h=post_h, d=8, center=true, $fn=24);
}

module wing_box_jig() {
    // base plate
    translate([root_chord/2, semi_span/2, -post_h/2 - 6])
        cube([root_chord + 40, semi_span + 40, 12], center=true);
    // front spar cradle (approx LE→tip sweep simplified as straight for tool)
    spar_cradle(root_chord*spar_front_pct, tip_chord*spar_front_pct + 20, 0, semi_span);
    // rear spar cradle
    spar_cradle(root_chord*spar_rear_pct, tip_chord*spar_rear_pct + 40, 0, semi_span);
    // rib posts WS-0,2,4,6,8,10
    for (i=[0:5]) {
        y = i * semi_span / 5;
        c = root_chord + (tip_chord - root_chord) * (i/5);
        rib_post(y, c);
    }
}

wing_box_jig();
