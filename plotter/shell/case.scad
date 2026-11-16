// ISM Plotter shell — bed frame + control bay (original ISM)
bed_w=300; bed_d=220; wall=3.5; rail_h=20;
pcb_w=100; pcb_h=70; usb_w=14; usb_h=8; mount_d=2.2; badge_depth=0.8;

module frame(){difference(){
  cube([bed_w,bed_d,rail_h+wall]);
  translate([wall,wall,wall])cube([bed_w-2*wall,bed_d-2*wall,rail_h+2]);
  // control bay cut
  translate([12,12,wall])cube([pcb_w+2,pcb_h+2,rail_h]);
  translate([12+pcb_w/2-usb_w/2,-1,wall+4])cube([usb_w,wall+4,usb_h]);
  translate([16,16,wall-badge_depth])linear_extrude(height=badge_depth+0.1)
    text("ISM PLOTTER",size=5,font="Liberation Sans:style=Bold");
}for(p=[[16,16],[16+pcb_w-4,16],[16,16+pcb_h-4],[16+pcb_w-4,16+pcb_h-4]])
  translate([p[0],p[1],wall])difference(){cylinder(h=4,d=6,$fn=24);translate([0,0,-0.1])cylinder(h=5,d=mount_d,$fn=20);}}

module gantry_bridge(){difference(){
  cube([bed_w-2*wall,18,12]);
  translate([8,4,-1])cube([bed_w-2*wall-16,10,14]);
}}

module pen_sled(){difference(){
  cube([40,30,16]);
  translate([8,8,-1])cube([24,14,18]);
  translate([20,15,-1])cylinder(h=20,d=8,$fn=24);
}}

frame();
