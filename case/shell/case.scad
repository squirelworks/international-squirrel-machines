// ISM Computer Case — ATX-class chassis + front panel bay (original ISM)
// Manifold-safe: bosses unioned into shell, holes cut in one difference().
// Dimensions approximate mini-ITX / SFF desktop; front bay fits 110×45 FP PCB.

outer_w = 220;
outer_d = 280;
outer_h = 180;
wall = 3;
eps = 0.02;
badge_depth = 0.6;
mount_d = 3.2; // M3 clearance

fp_w = 112;
fp_h = 47;
fp_recess = 8;
fp_x0 = (outer_w - fp_w) / 2;
fp_z0 = (outer_h - fp_h) / 2;

usb_a_w = 15;
usb_a_h = 8;
usb_c_w = 10;
usb_c_h = 4;

mb_x0 = 40;
mb_y0 = 50;
mb_holes = [[0, 0], [152.4, 0], [0, 152.4], [152.4, 152.4]];

fp_bosses = [
  [fp_x0 + 8, fp_z0 + 6],
  [fp_x0 + fp_w - 8, fp_z0 + 6],
  [fp_x0 + 8, fp_z0 + fp_h - 6],
  [fp_x0 + fp_w - 8, fp_z0 + fp_h - 6]
];

module chassis() {
  difference() {
    union() {
      cube([outer_w, outer_d, outer_h]);
      for (p = fp_bosses)
        translate([p[0], 0, p[1]])
          rotate([90, 0, 0])
            cylinder(h = wall + 4, d = 6, $fn = 24);
      for (h = mb_holes)
        translate([mb_x0 + h[0], mb_y0 + h[1], wall - eps])
          cylinder(h = 8 + eps, d = 8, $fn = 24);
    }
    translate([wall, wall, wall])
      cube([outer_w - 2 * wall, outer_d - 2 * wall, outer_h - wall + eps]);
    translate([fp_x0, -eps, fp_z0])
      cube([fp_w, wall + fp_recess + eps, fp_h]);
    for (dx = [-22, 8])
      translate([outer_w / 2 + dx, -eps, outer_h / 2 - 6])
        cube([usb_a_w, wall + 2 * eps, usb_a_h]);
    translate([outer_w / 2 - usb_c_w / 2, -eps, outer_h / 2 + 10])
      cube([usb_c_w, wall + 2 * eps, usb_c_h]);
    translate([outer_w / 2 - 50, outer_d - wall - eps, 40])
      cube([100, wall + 2 * eps, 80]);
    for (z = [40 : 12 : 140])
      for (side = [0, 1])
        translate([side * (outer_w - wall) - eps, 60, z])
          cube([wall + 2 * eps, 40, 6]);
    for (p = fp_bosses)
      translate([p[0], -eps, p[1]])
        rotate([-90, 0, 0])
          cylinder(h = wall + 8, d = mount_d, $fn = 20);
    for (h = mb_holes)
      translate([mb_x0 + h[0], mb_y0 + h[1], wall - eps])
        cylinder(h = 10 + 2 * eps, d = mount_d, $fn = 20);
    translate([16, 16, wall - badge_depth])
      linear_extrude(height = badge_depth + eps)
        text("ISM", size = 8, font = "Liberation Sans:style=Bold");
  }
}

module front_bezel() {
  bw = fp_w + 8;
  bh = fp_h + 8;
  bt = wall;
  difference() {
    cube([bw, bt, bh]);
    translate([4, -eps, 4])
      cube([fp_w, bt + 2 * eps, fp_h]);
    for (dx = [24, 44])
      translate([dx, -eps, bh / 2])
        rotate([-90, 0, 0])
          cylinder(h = bt + 2 * eps, d = 6, $fn = 24);
    for (dx = [64, 76])
      translate([dx, -eps, bh / 2 + 8])
        rotate([-90, 0, 0])
          cylinder(h = bt + 2 * eps, d = 3, $fn = 20);
  }
}

module top_lid() {
  difference() {
    cube([outer_w, outer_d, wall]);
    translate([outer_w / 2 - 40, outer_d / 2 - 8, wall - 1.2])
      cube([80, 16, 1.4]);
    for (p = [[10, 10], [outer_w - 10, 10], [10, outer_d - 10], [outer_w - 10, outer_d - 10]])
      translate([p[0], p[1], -eps])
        cylinder(h = wall + 2 * eps, d = mount_d, $fn = 20);
  }
}

chassis();
