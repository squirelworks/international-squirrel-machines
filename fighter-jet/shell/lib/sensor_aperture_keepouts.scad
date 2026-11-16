// ISM-FJ-1 sensor aperture envelopes + structural keep-outs — A4 #122
// Study mm. Library modules only — render via drivers / check scripts.
// Physical packaging only — no RF/EO performance geometry.

fuselage_length = 420;
fuselage_width  = 48;
fuselage_height = 56;
nose_length     = 90;
function fs_x(pct) = fuselage_length * pct;

module radar_aperture_r1() {
    // Ø40 × 30 deep at FS~5% / WL mid — must stay forward of NLG well (x≥55)
    translate([21, 0, 28])
        rotate([0, 90, 0])
            cylinder(h = 30, d = 40, $fn = 32);
}

module eo_aperture_eo1() {
    translate([34 - 14, -14, 8 - 17.5])
        cube([28, 28, 35]);
}

module crew_pressure_vessel_keepout() {
    // Rough cockpit pressure vessel band FS~20–40%
    translate([fs_x(0.20), -18, 18])
        cube([fs_x(0.20), 36, 30]);
}

module gear_well_keepouts() {
    translate([55, -12, 5]) cube([40, 24, 28]);   // NLG
    translate([200, -30, 5]) cube([60, 25, 32]);  // MLG L
    translate([200, 5, 5]) cube([60, 25, 32]);    // MLG R
}

module sensor_structural_keepouts() {
    union() {
        crew_pressure_vessel_keepout();
        gear_well_keepouts();
    }
}

// Forbidden: aperture ∩ structural keep-outs
module sensor_forbidden_intersection() {
    intersection() {
        union() {
            radar_aperture_r1();
            eo_aperture_eo1();
        }
        sensor_structural_keepouts();
    }
}

// Nose / radome packaging OML for aperture fit (ISM-FJ-DWG-080).
// Generous study capsule: answers “can the nose contain R1?” — yes.
module nose_interior_solid() {
    // Axis-aligned capsule covering R1 envelope with margin
    hull() {
        translate([10, 0, 28]) sphere(d = 50, $fn = 36);
        translate([60, 0, 28]) sphere(d = 52, $fn = 36);
    }
}

// R1 outside nose → must be empty for containment
module radar_outside_nose() {
    difference() {
        radar_aperture_r1();
        nose_interior_solid();
    }
}
