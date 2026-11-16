// ISM Camera shell — body + lens tube (original ISM)
// Manifold-safe: bosses unioned into shell, holes cut in one difference().
body_w=70; body_d=50; body_h=35; wall=3;
usb_w=14; usb_h=8; mount_d=2.2; badge_depth=0.6;
lens_od=28; lens_id=22; lens_len=18;
eps=0.02; boss_h=4;

module body(){
  difference(){
    union(){
      cube([body_w,body_d,body_h]);
      for(p=[[6,6],[body_w-6,6],[6,body_d-6],[body_w-6,body_d-6]])
        translate([p[0],p[1],wall-eps])cylinder(h=boss_h+eps,d=6,$fn=24);
    }
    // Inner cavity — leave top lip
    translate([wall,wall,wall])
      cube([body_w-2*wall,body_d-2*wall,body_h-wall+eps]);
    // Lens bore
    translate([body_w/2,-eps,body_h/2])
      rotate([-90,0,0])cylinder(h=wall+2*eps,d=lens_id,$fn=48);
    // USB cutout
    translate([body_w/2-usb_w/2,body_d-wall-eps,wall+4])
      cube([usb_w,wall+2*eps,usb_h]);
    // Mount holes through bosses
    for(p=[[6,6],[body_w-6,6],[6,body_d-6],[body_w-6,body_d-6]])
      translate([p[0],p[1],wall-eps])cylinder(h=boss_h+3*eps,d=mount_d,$fn=20);
    // Badge recess
    translate([8,8,wall-badge_depth])
      linear_extrude(height=badge_depth+eps)
        text("ISM",size=3.5,font="Liberation Sans:style=Bold");
  }
}

module lens_tube(){
  difference(){
    cylinder(h=lens_len,d=lens_od,$fn=48);
    translate([0,0,-eps])cylinder(h=lens_len+2*eps,d=lens_id,$fn=48);
  }
}

module back_plate(){
  difference(){
    cube([body_w+2,body_d+2,wall]);
    translate([body_w/2-usb_w/2+1,body_d-2,-eps])
      cube([usb_w,wall+4,wall+2*eps]);
  }
}

body();
