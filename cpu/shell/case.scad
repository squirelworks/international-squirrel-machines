// ISM CPU module heatsink shroud (original ISM)
// Manifold-safe: bosses unioned into shell, holes cut in one difference().
pcb_w = 65;
pcb_d = 60;
wall = 2.5;
shroud_h = 18;
fin_h = 10;
eps = 0.02;
mount_d = 2.2;
badge_depth = 0.5;

mounts = [[4, 4], [pcb_w - 4, 4], [4, pcb_d - 4], [pcb_w - 4, pcb_d - 4]];

module shroud() {
  difference() {
    union() {
      cube([pcb_w + 2 * wall, pcb_d + 2 * wall, shroud_h]);
      // Cooling fins on top
      for (x = [8 : 6 : pcb_w - 4])
        translate([x, wall + 8, shroud_h - eps])
          cube([2.5, pcb_d - 16, fin_h + eps]);
      for (p = mounts)
        translate([p[0] + wall, p[1] + wall, wall - eps])
          cylinder(h = 5 + eps, d = 6, $fn = 24);
    }
    translate([wall, wall, wall])
      cube([pcb_w, pcb_d, shroud_h - wall + eps]);
    // Header clearance (top edge of board / J1)
    translate([wall + 20, -eps, wall + 2])
      cube([24, wall + 4, 10]);
    // USB-C cutout
    translate([wall + pcb_w - 22, wall + pcb_d - 2, wall + 2])
      cube([16, wall + 4, 8]);
    for (p = mounts)
      translate([p[0] + wall, p[1] + wall, wall - eps])
        cylinder(h = 8 + 2 * eps, d = mount_d, $fn = 20);
    translate([wall + 6, wall + 6, wall - badge_depth])
      linear_extrude(height = badge_depth + eps)
        text("ISM", size = 4, font = "Liberation Sans:style=Bold");
  }
}

module base_plate() {
  difference() {
    cube([pcb_w + 2 * wall, pcb_d + 2 * wall, wall]);
    for (p = mounts)
      translate([p[0] + wall, p[1] + wall, -eps])
        cylinder(h = wall + 2 * eps, d = mount_d, $fn = 20);
    translate([wall + 20, wall + 2, -eps])
      cube([24, 8, wall + 2 * eps]);
  }
}

shroud();
