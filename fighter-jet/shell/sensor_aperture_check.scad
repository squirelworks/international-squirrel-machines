// A4 #122 — sensor aperture packaging check (cad-verify compatible).
// Witness cube only at top level; emptiness asserted by check_sensor_apertures.sh.

include <lib/sensor_aperture_keepouts.scad>

echo("A4 #122: aperture∩keepouts and R1-outside-nose must be empty; witness for CI.");
echo("A4 #122: run shell/check_sensor_apertures.sh");

translate([-200, 0, -20])
    cube(4, center = true);
