// ISM Camera shell — body + lens tube (original ISM)
body_w=70; body_d=50; body_h=35; wall=3;
pcb_w=80; pcb_h=55; // control board sits behind
usb_w=14; usb_h=8; mount_d=2.2; badge_depth=0.8;
lens_od=28; lens_id=22; lens_len=18;

module body(){difference(){
  cube([body_w,body_d,body_h]);
  translate([wall,wall,wall])cube([body_w-2*wall,body_d-2*wall,body_h]);
  translate([body_w/2, -1, body_h/2])rotate([-90,0,0])cylinder(h=wall+4,d=lens_id,$fn=48);
  translate([body_w/2-usb_w/2,body_d-wall-1,wall+4])cube([usb_w,wall+4,usb_h]);
  translate([6,6,wall-badge_depth])linear_extrude(height=badge_depth+0.1)
    text("ISM CAM",size=4,font="Liberation Sans:style=Bold");
}for(p=[[6,6],[body_w-6,6],[6,body_d-6],[body_w-6,body_d-6]])
  translate([p[0],p[1],wall])difference(){cylinder(h=4,d=6,$fn=24);translate([0,0,-0.1])cylinder(h=5,d=mount_d,$fn=20);}}

module lens_tube(){difference(){
  cylinder(h=lens_len,d=lens_od,$fn=48);
  translate([0,0,-1])cylinder(h=lens_len+2,d=lens_id,$fn=48);
}}

module back_plate(){difference(){
  cube([body_w+2,body_d+2,wall]);
  translate([body_w/2-usb_w/2+1,body_d-2,-1])cube([usb_w,wall+4,wall+2]);
}}

body();
