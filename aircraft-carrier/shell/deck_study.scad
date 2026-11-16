// ISM-CV-1 carrier flight-deck study — B2 slice (#45 / #43)
// Units: mm. Proportion sketch only. No weapons solids.

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

echo("B2: carrier deck study — arrangements only; no combat solids");
carrier_hull();
flight_deck();
island();
