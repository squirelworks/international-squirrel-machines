// ISM Power Supply enclosure (original ISM) — Track A DC rail board
// Manifold-safe: bosses unioned, vents/holes in one difference().
pcb_w = 100;
pcb_d = 70;
wall = 2.5;
box_h = 40;
eps = 0.02;
mount_d = 2.2;
badge_depth = 0.5;
vent_w = 3;
fan_d = 40;

mounts = [[4, 4], [pcb_w - 4, 4], [4, pcb_d - 4], [pcb_w - 4, pcb_d - 4]];

module enclosure() {
  difference() {
    union() {
      cube([pcb_w + 2 * wall, pcb_d + 2 * wall, box_h]);
      for (p = mounts)
        translate([p[0] + wall, p[1] + wall, wall - eps])
          cylinder(h = 6 + eps, d = 6, $fn = 24);
    }
    translate([wall, wall, wall])
      cube([pcb_w, pcb_d, box_h - wall + eps]);
    // Barrel jack
    translate([-eps, wall + 12, wall + 8])
      cube([wall + 4, 14, 12]);
    // MB_PWR header
    translate([-eps, wall + 36, wall + 4])
      cube([wall + 4, 22, 10]);
    // USB-C
    translate([wall + pcb_w - 22, -eps, wall + 4])
      cube([16, wall + 4, 8]);
    // Side vents
    for (y = [wall + 10 : 8 : wall + pcb_d - 10])
      translate([pcb_w + wall - eps, y, wall + 12])
        cube([wall + 2 * eps, vent_w, 16]);
    // Fan grille (40 mm class)
    translate([wall + pcb_w / 2, wall + pcb_d / 2, box_h - wall - eps])
      for (a = [0 : 45 : 315])
        rotate([0, 0, a])
          translate([8, -1.2, 0])
            cube([fan_d / 2 - 6, 2.4, wall + 2 * eps]);
    for (p = mounts)
      translate([p[0] + wall, p[1] + wall, wall - eps])
        cylinder(h = 10 + 2 * eps, d = mount_d, $fn = 20);
    translate([wall + 8, wall + 8, wall - badge_depth])
      linear_extrude(height = badge_depth + eps)
        text("ISM PSU", size = 5, font = "Liberation Sans:style=Bold");
  }
}

module lid() {
  difference() {
    cube([pcb_w + 2 * wall, pcb_d + 2 * wall, wall]);
    translate([wall + pcb_w / 2, wall + pcb_d / 2, -eps])
      cylinder(h = wall + 2 * eps, d = 38, $fn = 48);
    for (p = mounts)
      translate([p[0] + wall, p[1] + wall, -eps])
        cylinder(h = wall + 2 * eps, d = mount_d, $fn = 20);
  }
}

enclosure();
