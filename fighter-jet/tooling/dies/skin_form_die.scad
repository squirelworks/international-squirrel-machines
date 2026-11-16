// ISM-FJ-TOOL-060 — Sheet Al skin form die pair (study mm). Issue #106.
// Each die is its own manifold solid (export separately if needed).

panel_l = 120;
panel_w = 60;
crown = 6;
die_t = 20;

module male_die() {
    hull() {
        cube([panel_l, panel_w, die_t], center = true);
        translate([0, 0, die_t / 2 + crown / 2])
            scale([1, 1, 0.3]) sphere(d = panel_w, $fn = 48);
    }
}

module female_die() {
    difference() {
        cube([panel_l + 20, panel_w + 20, die_t + crown], center = true);
        translate([0, 0, 4]) male_die();
    }
}

// Preview both; each module is manifold on its own.
translate([0, -panel_w - 20, 0]) male_die();
translate([0, panel_w + 20, 0]) female_die();
