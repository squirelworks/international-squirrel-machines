// ISM Network Card bracket + cooler shroud (original ISM)
// Manifold-safe: bosses unioned into shell, holes cut in one difference().
pcb_w = 90;
pcb_d = 65;
wall = 2.5;
shroud_h = 14;
fin_h = 6;
eps = 0.02;
mount_d = 2.2;
badge_depth = 0.5;

mounts = [[4, 4], [pcb_w - 4, 4], [4, pcb_d - 4], [pcb_w - 4, pcb_d - 4]];

module shroud() {
  difference() {
    union() {
      cube([pcb_w + 2 * wall, pcb_d + 2 * wall, shroud_h]);
      for (x = [10 : 7 : pcb_w - 6])
        translate([x, wall + 12, shroud_h - eps])
          cube([3, pcb_d - 24, fin_h + eps]);
      for (p = mounts)
        translate([p[0] + wall, p[1] + wall, wall - eps])
          cylinder(h = 5 + eps, d = 6, $fn = 24);
    }
    translate([wall, wall, wall])
      cube([pcb_w, pcb_d, shroud_h - wall + eps]);
    // EXP header clearance
    translate([-eps, wall + 4, wall + 2])
      cube([wall + 4, 28, 10]);
    // RJ45 cutout
    translate([wall + 8, wall + pcb_d - 2, wall + 2])
      cube([18, wall + 4, 12]);
    // USB-C
    translate([wall + pcb_w - 24, -eps, wall + 2])
      cube([16, wall + 4, 8]);
    for (p = mounts)
      translate([p[0] + wall, p[1] + wall, wall - eps])
        cylinder(h = 8 + 2 * eps, d = mount_d, $fn = 20);
    translate([wall + 6, wall + 6, wall - badge_depth])
      linear_extrude(height = badge_depth + eps)
        text("ISM", size = 4, font = "Liberation Sans:style=Bold");
  }
}

module slot_bracket() {
  bw = 20;
  bh = 120;
  bt = 1.2;
  difference() {
    cube([bw, bt, bh]);
    translate([3, -eps, 18])
      cube([14, bt + 2 * eps, 16]);
    for (z = [8, bh - 8])
      translate([bw / 2, -eps, z])
        rotate([-90, 0, 0])
          cylinder(h = bt + 2 * eps, d = 3.2, $fn = 20);
  }
}

shroud();
