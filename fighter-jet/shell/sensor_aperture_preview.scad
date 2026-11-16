// Preview sensor apertures + keep-outs (draws geometry for CI render).
include <lib/sensor_aperture_keepouts.scad>

radar_aperture_r1();
eo_aperture_eo1();
%sensor_structural_keepouts();
