// ISM-CV-1 carrier flight-deck study — #45 deepen
// Units: mm. Proportion sketch + topside mass boxes.
// Weapons/sensors = geometry mass boxes only — no combat solids.

deck_length = 600;
deck_beam   = 120;
hull_depth  = 50;

module carrier_hull() {
    hull() {
        translate([40, 0, 20])
            scale([1.5, 0.9, 0.6])
                sphere(d = 80, $fn = 28);
        translate([deck_length * 0.5, 0, 22])
            scale([1.0, 1.0, 0.7])
                sphere(d = deck_beam * 0.85, $fn = 28);
        translate([deck_length - 40, 0, 20])
            scale([1.4, 0.85, 0.55])
                sphere(d = 70, $fn = 28);
    }
}

module flight_deck() {
    translate([20, -deck_beam / 2, hull_depth])
        cube([deck_length - 40, deck_beam, 4]);
}

module island() {
    translate([deck_length * 0.55, deck_beam * 0.25, hull_depth + 4])
        cube([50, 28, 60]);
}

module elevator_opening(x) {
    translate([x, -20, hull_depth - 1])
        cube([30, 24, 6]);
}

module radar_mass_box() {
    // SEN-RADAR-ISLAND mass/windage box
    translate([deck_length * 0.55 + 10, deck_beam * 0.25 + 4, hull_depth + 64])
        cube([24, 20, 28]);
}

module ciws_mass_box(x) {
    // WP-CIWS mount mass box
    translate([x, -deck_beam / 2 + 8, hull_depth + 4])
        cube([12, 12, 16]);
}

echo("#45: carrier deck study — arrangements + mass boxes; no combat interfaces");
carrier_hull();
flight_deck();
island();
elevator_opening(120);
elevator_opening(380);
radar_mass_box();
ciws_mass_box(60);
ciws_mass_box(520);
