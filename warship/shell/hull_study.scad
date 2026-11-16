// ISM-WS-1 warship hull study — B2 #43
// Units: mm study model. Public-domain proportion sketch only.
// No weapons geometry — combat items are YAML mass/footprint boxes only.

hull_length = 400;
hull_beam   = 52;
hull_depth  = 36;
draft       = 18;

module hull_body() {
    hull() {
        // Bow
        translate([20, 0, draft])
            scale([1.2, 0.45, 0.7])
                sphere(d = hull_beam * 0.9, $fn = 36);
        // Midbody
        translate([hull_length * 0.45, 0, draft])
            scale([1.0, 0.55, 0.85])
                sphere(d = hull_beam, $fn = 36);
        // Stern
        translate([hull_length - 30, 0, draft + 2])
            scale([1.3, 0.4, 0.65])
                sphere(d = hull_beam * 0.75, $fn = 36);
    }
}

module deck_box() {
    translate([80, -hull_beam * 0.22, hull_depth - 4])
        cube([hull_length * 0.55, hull_beam * 0.44, 8]);
}

module superstructure_stub() {
    translate([150, -18, hull_depth + 4])
        cube([80, 36, 28]);
}

echo("B2 #43: warship hull study — hydro/arrangements only; no weapons solids");
hull_body();
deck_box();
superstructure_stub();
