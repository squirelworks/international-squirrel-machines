// ISM Thumb Drive shell (original ISM)
// Manifold-safe: bosses unioned, openings cut in one difference().
pcb_w = 70;
pcb_d = 45;
wall = 2.2;
box_h = 12;
eps = 0.02;
mount_d = 2.2;
badge_depth = 0.4;

mounts = [[3.5, 3.5], [pcb_w - 3.5, 3.5], [3.5, pcb_d - 3.5], [pcb_w - 3.5, pcb_d - 3.5]];

module stick() {
  difference() {
    union() {
      cube([pcb_w + 2 * wall, pcb_d + 2 * wall, box_h]);
      for (p = mounts)
        translate([p[0] + wall, p[1] + wall, wall - eps])
          cylinder(h = 4 + eps, d = 5, $fn = 24);
    }
    translate([wall, wall, wall])
      cube([pcb_w, pcb_d, box_h - wall + eps]);
    // USB-C nose
    translate([wall + pcb_w - 22, -eps, wall + 2])
      cube([14, wall + 4, 7]);
    // LED window
    translate([wall + pcb_w - 18, wall + pcb_d - 1, wall + 3])
      cube([6, wall + 2, 3]);
    for (p = mounts)
      translate([p[0] + wall, p[1] + wall, wall - eps])
        cylinder(h = 8 + 2 * eps, d = mount_d, $fn = 20);
    translate([wall + 4, wall + 4, wall - badge_depth])
      linear_extrude(height = badge_depth + eps)
        text("ISM", size = 3.5, font = "Liberation Sans:style=Bold");
  }
}

module cap() {
  // Removable end-cap silhouette for print check
  w = 20;
  d = pcb_d + 2 * wall + 1;
  h = box_h + 1;
  difference() {
    cube([w, d, h]);
    translate([2, 2, 2])
      cube([w - 4, d - 4, h]);
    translate([4, 4, h - 0.4])
      linear_extrude(height = 0.5)
        text("TD", size = 3, font = "Liberation Sans:style=Bold");
  }
}

stick();
