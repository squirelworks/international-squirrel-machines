// ISM SCSI / SCSI carrier shell (original ISM) — 2.5" bay style
pcb_w = 90;
pcb_d = 45;
wall = 2.2;
box_h = 14;
eps = 0.02;
mount_d = 2.2;
badge_depth = 0.4;

mounts = [[3.5, 3.5], [pcb_w - 3.5, 3.5], [3.5, pcb_d - 3.5], [pcb_w - 3.5, pcb_d - 3.5]];

module carrier() {
  difference() {
    union() {
      cube([pcb_w + 2 * wall, pcb_d + 2 * wall, box_h]);
      for (p = mounts)
        translate([p[0] + wall, p[1] + wall, wall - eps])
          cylinder(h = 4 + eps, d = 5, $fn = 24);
    }
    translate([wall, wall, wall])
      cube([pcb_w, pcb_d, box_h - wall + eps]);
    // USB-C
    translate([wall + 40, -eps, wall + 2])
      cube([14, wall + 4, 7]);
    // SCSI ribbon / drive bay opening
    translate([wall + 55, wall + pcb_d - 1, wall + 2])
      cube([30, wall + 3, 8]);
    // Drive power header
    translate([wall + 72, wall + pcb_d - 1, wall + 4])
      cube([12, wall + 3, 6]);
    for (p = mounts)
      translate([p[0] + wall, p[1] + wall, wall - eps])
        cylinder(h = 8 + 2 * eps, d = mount_d, $fn = 20);
    translate([wall + 4, wall + 4, wall - badge_depth])
      linear_extrude(height = badge_depth + eps)
        text("ISM", size = 3.5, font = "Liberation Sans:style=Bold");
  }
}

module lid() {
  difference() {
    cube([pcb_w + 2 * wall, pcb_d + 2 * wall, 2.5]);
    translate([4, 4, 2.5 - badge_depth])
      linear_extrude(height = badge_depth + eps)
        text("SCSI", size = 4, font = "Liberation Sans:style=Bold");
  }
}

carrier();
