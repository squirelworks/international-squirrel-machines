// ISM Flash Cards reader shell (original ISM)
// Manifold-safe: bosses unioned, openings cut in one difference().
pcb_w = 55;
pcb_d = 40;
wall = 2.2;
box_h = 12;
eps = 0.02;
mount_d = 2.2;
badge_depth = 0.4;

mounts = [[3.5, 3.5], [pcb_w - 3.5, 3.5], [3.5, pcb_d - 3.5], [pcb_w - 3.5, pcb_d - 3.5]];

module reader() {
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
    translate([wall + pcb_w - 20, -eps, wall + 2])
      cube([14, wall + 4, 7]);
    // microSD slot
    translate([-eps, wall + 16, wall + 2])
      cube([wall + 6, 14, 4]);
    for (p = mounts)
      translate([p[0] + wall, p[1] + wall, wall - eps])
        cylinder(h = 8 + 2 * eps, d = mount_d, $fn = 20);
    translate([wall + 4, wall + 4, wall - badge_depth])
      linear_extrude(height = badge_depth + eps)
        text("ISM", size = 3.5, font = "Liberation Sans:style=Bold");
  }
}

module card_shell() {
  // Approximate microSD outline (SD Physical Layer Simplified Spec family)
  // 15 × 11 × 1 mm class body for print check (±0.2 mm tolerance table in design-note)
  w = 15.0;
  d = 11.0;
  h = 1.0;
  difference() {
    cube([w, d, h]);
    translate([1.2, 1.2, h - 0.3])
      linear_extrude(height = 0.4)
        text("ISM", size = 2.2, font = "Liberation Sans:style=Bold");
  }
}

reader();
