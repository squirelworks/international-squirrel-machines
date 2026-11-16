// ISM Motherboard tray + I/O shield (original ISM)
// Manifold-safe: bosses unioned into shell, holes cut in one difference().
pcb_w = 140;
pcb_d = 110;
wall = 3;
lip = 2;
tray_h = 12;
eps = 0.02;
mount_d = 2.2;
badge_depth = 0.6;

mounts = [[5, 5], [pcb_w - 5, 5], [5, pcb_d - 5], [pcb_w - 5, pcb_d - 5]];

module tray() {
  difference() {
    union() {
      cube([pcb_w + 2 * wall, pcb_d + 2 * wall, tray_h]);
      for (p = mounts)
        translate([p[0] + wall, p[1] + wall, wall - eps])
          cylinder(h = 6 + eps, d = 6, $fn = 24);
    }
    translate([wall, wall, wall])
      cube([pcb_w, pcb_d, tray_h - wall + eps]);
    // USB-C cutout (front)
    translate([wall + 16, -eps, wall + 2])
      cube([16, wall + 2 * eps, 8]);
    // Header clearance windows
    translate([wall + 20, wall + pcb_d - 2, wall + 1])
      cube([40, wall + 4, 8]);
    for (p = mounts)
      translate([p[0] + wall, p[1] + wall, wall - eps])
        cylinder(h = 8 + 2 * eps, d = mount_d, $fn = 20);
    translate([wall + 8, wall + 8, wall - badge_depth])
      linear_extrude(height = badge_depth + eps)
        text("ISM", size = 5, font = "Liberation Sans:style=Bold");
  }
}

module io_shield() {
  w = pcb_w + 2 * wall;
  h = 28;
  t = wall;
  difference() {
    cube([w, t, h]);
    translate([wall + 16, -eps, 8])
      cube([16, t + 2 * eps, 8]);
    translate([wall + 100, -eps, 6])
      cube([20, t + 2 * eps, 14]);
  }
}

module lid() {
  difference() {
    cube([pcb_w + 2 * wall, pcb_d + 2 * wall, wall]);
    for (p = mounts)
      translate([p[0] + wall, p[1] + wall, -eps])
        cylinder(h = wall + 2 * eps, d = mount_d, $fn = 20);
    translate([(pcb_w + 2 * wall) / 2 - 30, (pcb_d + 2 * wall) / 2 - 6, wall - 1])
      cube([60, 12, 1.2]);
  }
}

tray();
