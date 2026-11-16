// ISM Fighter Jet — parametric airframe shell (study model) · #72
// International Squirrel Machines
// Units: millimeters. Aligns to aircraft-geometry.yaml FS/WS tables.
// Structural authority: mechanical/ + interfaces/mechanical-airframe.yaml

/* [Overall] */
fuselage_length = 420;
fuselage_width  = 48;
fuselage_height = 56;
nose_length     = 90;
wing_span       = 280;
wing_root_chord = 110;
wing_tip_chord  = 45;
wing_thickness  = 12;
wing_sweep      = 35;
htail_span      = 100;
htail_chord     = 50;
htail_thickness = 6;
vtail_height    = 70;
vtail_chord     = 60;
vtail_thickness = 6;
wall             = 2.4;
avionics_bay_l   = 120;
avionics_bay_w   = 80;
avionics_bay_h   = 18;
badge_depth      = 1.2;

// Station helpers (pct FS → X)
function fs_x(pct) = fuselage_length * pct;
wing_le_x = nose_length + 80; // LE root ≈ FS region matching study
wing_z    = fuselage_height * 0.35;

// Debug overlays off by default so STL export is a single manifold solid.
show_stations = false;
show_structure_planes = false;
show_gear_deployed = true;

module fuselage() {
    difference() {
        union() {
            hull() {
                translate([nose_length, 0, fuselage_height/2])
                    scale([1, fuselage_width/fuselage_height, 1])
                        sphere(d=fuselage_height);
                translate([fuselage_length - 40, 0, fuselage_height/2])
                    scale([1.2, fuselage_width/fuselage_height * 0.7, 0.7])
                        sphere(d=fuselage_height * 0.85);
            }
            translate([nose_length + 40, 0, fuselage_height * 0.85])
                scale([1.6, 0.7, 0.55])
                    sphere(d=fuselage_width);
        }
        translate([nose_length + 10, 0, fuselage_height/2])
            scale([0.92, (fuselage_width - 2*wall)/fuselage_width,
                   (fuselage_height - 2*wall)/fuselage_height])
                hull() {
                    sphere(d=fuselage_height);
                    translate([fuselage_length - nose_length - 60, 0, 0])
                        scale([1.2, 0.7, 0.7])
                            sphere(d=fuselage_height * 0.85);
                }
        // Avionics bay dorsal hatch (FS-48 region)
        translate([nose_length + 30, -avionics_bay_w/2, fuselage_height - avionics_bay_h])
            cube([avionics_bay_l, avionics_bay_w, avionics_bay_h + 2]);
        // Intake / nozzle placeholders
        translate([-2, 0, fuselage_height * 0.35])
            rotate([0, 90, 0])
                cylinder(h=nose_length * 0.4, d=fuselage_width * 0.35, $fn=32);
        translate([fuselage_length - 30, 0, fuselage_height * 0.4])
            rotate([0, 90, 0])
                cylinder(h=40, d=fuselage_width * 0.45, $fn=32);
        // NLG well (FS-18) — stowed bay
        translate([55, -12, 5]) cube([40, 24, 28]);
        // MLG wells (FS-55)
        translate([200, -30, 5]) cube([60, 25, 32]);
        translate([200, 5, 5]) cube([60, 25, 32]);
    }
}

module wing_planform(side=1) {
    polygon([
        [0, 0],
        [wing_root_chord, 0],
        [wing_tip_chord * 0.4, side * wing_span/2],
        [0, side * wing_span/2 * 0.85]
    ]);
}

module wing_half(side=1) {
    translate([wing_le_x, 0, wing_z])
        rotate([0, 0, -side * wing_sweep])
            translate([0, side * fuselage_width/2, 0])
                difference() {
                    linear_extrude(height=wing_thickness, center=true)
                        wing_planform(side);
                    // Aileron hinge groove (~75% chord, outboard)
                    translate([wing_root_chord * 0.75, side * wing_span * 0.38, 0])
                        cube([2.5, wing_span * 0.28, wing_thickness + 2], center=true);
                    // Flaperon hinge groove (~70% chord, inboard)
                    translate([wing_root_chord * 0.70, side * wing_span * 0.18, 0])
                        cube([2.5, wing_span * 0.32, wing_thickness + 2], center=true);
                }
}

module horizontal_stabilizer() {
    translate([fs_x(0.92) - htail_chord * 0.3, 0, fuselage_height * 0.45])
        linear_extrude(height=htail_thickness, center=true)
            polygon([
                [0, -htail_span/2],
                [htail_chord, -htail_span/2 * 0.6],
                [htail_chord,  htail_span/2 * 0.6],
                [0,  htail_span/2]
            ]);
}

module ism_badge_boss() {
    // Rooted in fin midplane, protrudes past starboard face (manifold with fin).
    translate([fuselage_length - 70, 0,
               fuselage_height * 0.7 + vtail_height * 0.45])
        rotate([-90, 0, 0])
            cylinder(h = vtail_thickness / 2 + badge_depth, d = 12, $fn = 32);
}

module vertical_stabilizer() {
    difference() {
        union() {
            translate([fuselage_length - 90, 0, fuselage_height * 0.7])
                rotate([90, 0, 0])
                    linear_extrude(height=vtail_thickness, center=true)
                        polygon([
                            [0, 0],
                            [vtail_chord, 0],
                            [vtail_chord * 0.55, vtail_height],
                            [vtail_chord * 0.15, vtail_height]
                        ]);
            ism_badge_boss();
        }
        // Rudder hinge groove (~70% chord)
        translate([fuselage_length - 90 + vtail_chord * 0.70, 0,
                   fuselage_height * 0.7 + vtail_height * 0.35])
            cube([2.5, vtail_thickness + 4, vtail_height * 0.7], center=true);
        // Annular badge recess around boss (does not detach boss)
        translate([fuselage_length - 70, vtail_thickness / 2 - 0.05,
                   fuselage_height * 0.7 + vtail_height * 0.45])
            rotate([-90, 0, 0])
                difference() {
                    cylinder(h = badge_depth + 0.15, d = 14, $fn = 32);
                    translate([0, 0, -0.1])
                        cylinder(h = badge_depth + 0.4, d = 12.2, $fn = 32);
                }
    }
}

module station_marker(fs_pct, d=3) {
    translate([fs_x(fs_pct), 0, fuselage_height + 4])
        color("SaddleBrown") sphere(d=d, $fn=12);
}

module station_set() {
    if (show_stations) {
        station_marker(0.00);
        station_marker(0.12);
        station_marker(0.18); // NLG
        station_marker(0.22);
        station_marker(0.48);
        station_marker(0.55); // MLG
        station_marker(0.62); // carry-through
        station_marker(0.90);
        station_marker(0.92); // HT hinge
        station_marker(1.00);
    }
}

// Spar / rib study planes (debug — not printable mass)
module structure_planes() {
    if (show_structure_planes) {
        // Carry-through FS-62 slab
        translate([fs_x(0.62), 0, wing_z])
            color("SteelBlue", 0.35)
                cube([6, fuselage_width + 20, wing_thickness + 8], center=true);
        // Wing rib posts at WS fractions (right wing LE frame)
        for (ws = [0, 0.25, 0.50, 0.75, 0.92, 1.0]) {
            translate([wing_le_x + wing_root_chord * 0.4,
                       fuselage_width/2 + ws * wing_span/2, wing_z])
                color("DarkOliveGreen", 0.4)
                    cube([wing_root_chord * 0.5, 2, wing_thickness + 4], center=true);
        }
    }
}

module gear_leg(attach, wheel, tire_od) {
    // Single manifold strut: hull into airframe structure above the well,
    // through attach, into wheel hub; tire shares hub volume.
    hub_r = 5;
    union() {
        hull() {
            translate([attach[0], attach[1], attach[2] + 22])
                sphere(d = 6, $fn = 16);
            translate(attach)
                sphere(d = 5, $fn = 16);
            translate(wheel)
                sphere(d = hub_r * 2, $fn = 16);
        }
        translate(wheel) {
            sphere(d = hub_r * 2 + 1, $fn = 20);
            rotate([0, 90, 0])
                cylinder(h = max(10, tire_od * 0.4), d = tire_od, center = true, $fn = 28);
        }
    }
}

module landing_gear_deployed() {
    // Attach points chosen to penetrate remaining belly solid above gear wells;
    // wheel centers aligned to mechanical-airframe.yaml (study mm).
    gear_leg([75.6, 0, 4], [75.6, 0, -28], 18);       // NLG
    gear_leg([231, -18, 4], [231, -42, -32], 28);     // MLG L
    gear_leg([231, 18, 4], [231, 42, -32], 28);       // MLG R
}

module empennage() {
    horizontal_stabilizer();
    vertical_stabilizer();
}

module wing() {
    wing_half(+1);
    wing_half(-1);
}

module airframe() {
    union() {
        fuselage();
        wing();
        empennage();
        if (show_gear_deployed) landing_gear_deployed();
    }
    // Debug overlays (not part of export solid)
    station_set();
    structure_planes();
}

// Preview assembly. For STL export, comment airframe() and call one module.
airframe();

// Export selectors (OpenSCAD CLI -D '...' or uncomment one):
// fuselage();
// wing();
// empennage();
// landing_gear_deployed();
