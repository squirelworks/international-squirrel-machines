// ISM-SAT-1 3U bus + structural study — #31
// Units: mm. Structure sketch + ghost trays/hinges/payload deck.
// No weapons geometry — payload is mass/power/data only.

u = 100;
h_3u = 340;

module rails() {
    for (xy = [[1, 1], [1, -1], [-1, 1], [-1, -1]])
        translate([xy[0] * (u / 2 - 5), xy[1] * (u / 2 - 5), 0])
            cube([8, 8, h_3u], center = false);
}

module panels() {
    translate([-u / 2, -u / 2, 0])
        cube([u, 2, h_3u]);
    translate([-u / 2, u / 2 - 2, 0])
        cube([u, 2, h_3u]);
}

module tray() {
    translate([-u / 2 + 10, -u / 2 + 10, h_3u * 0.4])
        cube([u - 20, u - 20, 8]);
}

module avionics_trays() {
    for (z = [h_3u * 0.25, h_3u * 0.55])
        translate([-u / 2 + 12, -u / 2 + 12, z])
            cube([u - 24, u - 24, 4]);
}

module payload_deck() {
    // Non-weapon payload attach — mass/power only
    translate([-u / 2 + 15, -u / 2 + 15, h_3u - 40])
        cube([u - 30, u - 30, 6]);
}

module solar_panel_hinges() {
    for (side = [-1, 1])
        translate([side * (u / 2 - 2), -4, h_3u * 0.5])
            cube([4, 8, 20]);
}

module antenna_mounts() {
    translate([-6, -6, h_3u - 8])
        cube([12, 12, 6]);
}

echo("#31: satellite structural study — rails/trays/panels; no weapons solids");
rails();
panels();
tray();
%avionics_trays();
%payload_deck();
%solar_panel_hinges();
%antenna_mounts();
