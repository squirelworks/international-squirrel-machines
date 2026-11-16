// ISM-CV-1 carrier flight-deck + structural study — #45
// Units: mm. Proportion sketch + topside mass boxes + ghost structure.
// Weapons/sensors = geometry mass boxes only — no combat solids.

deck_length = 600;
deck_beam   = 120;
hull_depth  = 50;
frame_count = 10;

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
    translate([deck_length * 0.55 + 10, deck_beam * 0.25 + 4, hull_depth + 64])
        cube([24, 20, 28]);
}

module ciws_mass_box(x) {
    translate([x, -deck_beam / 2 + 8, hull_depth + 4])
        cube([12, 12, 16]);
}

module keel() {
    translate([40, -3, 8])
        cube([deck_length - 80, 6, 8]);
}

module transverse_frames() {
    for (i = [1:frame_count]) {
        x = 50 + i * (deck_length - 100) / (frame_count + 1);
        translate([x, -deck_beam * 0.35, 6])
            cube([3, deck_beam * 0.7, hull_depth - 8]);
    }
}

module hangar_deck() {
    translate([40, -deck_beam * 0.4, hull_depth * 0.55])
        cube([deck_length - 80, deck_beam * 0.8, 3]);
}

module flight_deck_beams() {
    for (i = [0:8]) {
        translate([40 + i * 60, -deck_beam * 0.4, hull_depth - 2])
            cube([4, deck_beam * 0.8, 3]);
    }
}

module elevator_trunks() {
    for (x = [120, 380]) {
        translate([x + 2, -18, 10])
            cube([26, 20, hull_depth - 12]);
    }
}

module island_foundation() {
    translate([deck_length * 0.55, deck_beam * 0.22, hull_depth - 6])
        cube([50, 34, 8]);
}

module catapult_arresting_keepouts() {
    // Load-path placeholders only — no plant design
    translate([80, -8, hull_depth + 4])
        cube([180, 16, 2]);
    translate([deck_length - 200, -8, hull_depth + 4])
        cube([120, 16, 2]);
}

echo("#45: carrier structural study — frames/hangar; mass boxes only; no combat interfaces");
carrier_hull();
flight_deck();
island();
elevator_opening(120);
elevator_opening(380);
radar_mass_box();
ciws_mass_box(60);
ciws_mass_box(520);
%keel();
%transverse_frames();
%hangar_deck();
%flight_deck_beams();
%elevator_trunks();
%island_foundation();
%catapult_arresting_keepouts();
