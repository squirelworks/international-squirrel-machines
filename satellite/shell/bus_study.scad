// ISM-SAT-1 3U bus study — B5 #31
// Units: mm. Structure sketch only — no weapons geometry.

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

echo("B5 #31: 3U bus study — educational structure; no weapons solids");
rails();
panels();
tray();
