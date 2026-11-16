// ISM Mouse — parametric printable shell (original ISM design)
// International Squirrel Machines
// Units: millimeters

/* [Overall] */
body_length = 110;
body_width  = 62;
body_height = 38;
wall        = 2.2;
pcb_length  = 90;
pcb_width   = 60;
pcb_clear   = 0.4;
sensor_window_d = 8;
usb_cut_w   = 14;
usb_cut_h   = 8;
button_w    = 14;
button_d    = 10;
encoder_d   = 8;
mount_d     = 2.2;
badge_depth = 0.6;

module mouse_outer() {
    hull() {
        translate([10, 0, body_height * 0.45])
            scale([1.0, body_width / body_height, 1])
                sphere(d=body_height, $fn=48);
        translate([body_length - 18, 0, body_height * 0.35])
            scale([1.1, 0.85, 0.75])
                sphere(d=body_height * 0.9, $fn=48);
        translate([body_length * 0.45, 0, body_height * 0.55])
            scale([1.4, 0.95, 0.7])
                sphere(d=body_height, $fn=48);
    }
}

module pcb_cavity() {
    translate([
        (body_length - pcb_length) / 2,
        -pcb_width / 2,
        wall
    ])
        cube([pcb_length, pcb_width, body_height]);
}

module usb_cut() {
    translate([-1, -usb_cut_w / 2, wall + 2])
        cube([12, usb_cut_w, usb_cut_h]);
}

module sensor_window() {
    translate([body_length * 0.55, 0, -1])
        cylinder(h=wall + 4, d=sensor_window_d, $fn=32);
}

module button_wells() {
    for (x = [body_length * 0.28, body_length * 0.42, body_length * 0.56]) {
        translate([x, body_width * 0.18, body_height - wall - 1])
            cube([button_w, button_d, wall + 3], center=true);
    }
}

module encoder_hole() {
    translate([body_length * 0.72, 0, body_height - wall - 1])
        cylinder(h=wall + 4, d=encoder_d, $fn=32);
}

module mount_posts() {
    positions = [
        [ (body_length - pcb_length) / 2 + 5, -pcb_width / 2 + 5 ],
        [ (body_length - pcb_length) / 2 + pcb_length - 5, -pcb_width / 2 + 5 ],
        [ (body_length - pcb_length) / 2 + 5, pcb_width / 2 - 5 ],
        [ (body_length - pcb_length) / 2 + pcb_length - 5, pcb_width / 2 - 5 ]
    ];
    for (p = positions) {
        translate([p[0], p[1], wall])
            difference() {
                cylinder(h=4, d=6, $fn=24);
                translate([0, 0, -0.1])
                    cylinder(h=5, d=mount_d, $fn=20);
            }
    }
}

module ism_badge() {
    translate([body_length * 0.15, -body_width * 0.35, body_height - badge_depth])
        linear_extrude(height=badge_depth + 0.1)
            text("ISM", size=6, font="Liberation Sans:style=Bold", halign="left", valign="center");
}

module mouse_shell() {
    difference() {
        mouse_outer();
        pcb_cavity();
        usb_cut();
        sensor_window();
        button_wells();
        encoder_hole();
        // split plane helper (top half removed for bottom shell default)
        translate([-5, -body_width, body_height * 0.55])
            cube([body_length + 10, body_width * 2, body_height]);
        ism_badge();
    }
    mount_posts();
}

module mouse_top() {
    difference() {
        mouse_outer();
        translate([-5, -body_width, -1])
            cube([body_length + 10, body_width * 2, body_height * 0.55 + 1]);
        button_wells();
        encoder_hole();
        usb_cut();
        ism_badge();
    }
}

// Default export: bottom shell (holds PCB)
mouse_shell();
