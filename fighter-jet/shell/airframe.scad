// ISM Fighter Jet — parametric airframe shell
// International Squirrel Machines
// Pure Squirrel-OS/2 Warp hardware
// Units: millimeters. Export STLs after tuning parameters.

/* [Overall] */
fuselage_length = 420;
fuselage_width  = 48;
fuselage_height = 56;
nose_length     = 90;
wing_span       = 280;
wing_root_chord = 110;
wing_tip_chord  = 45;
wing_thickness  = 12;
wing_sweep      = 35; // degrees
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

module fuselage() {
    difference() {
        union() {
            // main body
            hull() {
                translate([nose_length, 0, fuselage_height/2])
                    scale([1, fuselage_width/fuselage_height, 1])
                        sphere(d=fuselage_height);
                translate([fuselage_length - 40, 0, fuselage_height/2])
                    scale([1.2, fuselage_width/fuselage_height * 0.7, 0.7])
                        sphere(d=fuselage_height * 0.85);
            }
            // canopy blister
            translate([nose_length + 40, 0, fuselage_height * 0.85])
                scale([1.6, 0.7, 0.55])
                    sphere(d=fuselage_width);
        }
        // hollow
        translate([nose_length + 10, 0, fuselage_height/2])
            scale([0.92, (fuselage_width - 2*wall)/fuselage_width,
                   (fuselage_height - 2*wall)/fuselage_height])
                hull() {
                    sphere(d=fuselage_height);
                    translate([fuselage_length - nose_length - 60, 0, 0])
                        scale([1.2, 0.7, 0.7])
                            sphere(d=fuselage_height * 0.85);
                }
        // avionics bay cutout (dorsal hatch)
        translate([nose_length + 30, -avionics_bay_w/2, fuselage_height - avionics_bay_h])
            cube([avionics_bay_l, avionics_bay_w, avionics_bay_h + 2]);
        // intake / nozzle placeholders
        translate([-2, 0, fuselage_height * 0.35])
            rotate([0, 90, 0])
                cylinder(h=nose_length * 0.4, d=fuselage_width * 0.35, $fn=32);
        translate([fuselage_length - 30, 0, fuselage_height * 0.4])
            rotate([0, 90, 0])
                cylinder(h=40, d=fuselage_width * 0.45, $fn=32);
    }
}

module wing_half(side=1) {
    // side: +1 right, -1 left (looking forward)
    translate([nose_length + 80, 0, fuselage_height * 0.35])
        rotate([0, 0, -side * wing_sweep])
            translate([0, side * fuselage_width/2, 0])
                linear_extrude(height=wing_thickness, center=true)
                    polygon([
                        [0, 0],
                        [wing_root_chord, 0],
                        [wing_tip_chord * 0.4, side * wing_span/2],
                        [0, side * wing_span/2 * 0.85]
                    ]);
}

module horizontal_stabilizer() {
    translate([fuselage_length - 70, 0, fuselage_height * 0.45])
        linear_extrude(height=htail_thickness, center=true)
            polygon([
                [0, -htail_span/2],
                [htail_chord, -htail_span/2 * 0.6],
                [htail_chord,  htail_span/2 * 0.6],
                [0,  htail_span/2]
            ]);
}

module vertical_stabilizer() {
    difference() {
        translate([fuselage_length - 90, 0, fuselage_height * 0.7])
            rotate([90, 0, 0])
                linear_extrude(height=vtail_thickness, center=true)
                    polygon([
                        [0, 0],
                        [vtail_chord, 0],
                        [vtail_chord * 0.55, vtail_height],
                        [vtail_chord * 0.15, vtail_height]
                    ]);
        // ISM badge recess on fin
        translate([fuselage_length - 70, vtail_thickness/2 - 0.1,
                   fuselage_height * 0.7 + vtail_height * 0.45])
            rotate([90, 0, 0])
                cylinder(h=badge_depth + 0.2, d=14, $fn=32);
    }
}

module ism_badge_boss() {
    // printable badge insert for vertical stabilizer
    translate([fuselage_length - 70, vtail_thickness/2 + 0.5,
               fuselage_height * 0.7 + vtail_height * 0.45])
        rotate([90, 0, 0])
            cylinder(h=badge_depth, d=12, $fn=32);
}

module airframe() {
    fuselage();
    wing_half(+1);
    wing_half(-1);
    horizontal_stabilizer();
    vertical_stabilizer();
    ism_badge_boss();
}

// Preview assembly. Comment out and call parts for separate STLs.
airframe();

// Part selectors for export:
// fuselage();
// wing_half(+1); wing_half(-1);
// horizontal_stabilizer();
// vertical_stabilizer();
