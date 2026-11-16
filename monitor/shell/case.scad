// ISM Monitor shell — bezel + rear control bay (original ISM)
panel_w=350; panel_h=200; bezel=12; depth=45; wall=3.5;
pcb_w=100; pcb_h=70; usb_w=14; usb_h=8; hdmi_w=16; hdmi_h=8;
mount_d=2.2; badge_depth=0.8;
inner_w=panel_w; inner_h=panel_h;
case_w=inner_w+2*bezel; case_h=inner_h+2*bezel;

module rear_bay(){difference(){
  translate([-wall,-wall,0])cube([pcb_w+2*wall,pcb_h+2*wall,28]);
  translate([0,0,wall])cube([pcb_w,pcb_h,30]);
  translate([pcb_w/2-usb_w/2,-wall-1,wall+4])cube([usb_w,wall+4,usb_h]);
  translate([8,-wall-1,wall+4])cube([hdmi_w,wall+4,hdmi_h]);
  translate([6,6,wall-badge_depth])linear_extrude(height=badge_depth+0.1)
    text("ISM MONITOR",size=4,font="Liberation Sans:style=Bold");
}for(p=[[4,4],[pcb_w-4,4],[4,pcb_h-4],[pcb_w-4,pcb_h-4]])
  translate([p[0],p[1],wall])difference(){cylinder(h=4,d=6,$fn=24);translate([0,0,-0.1])cylinder(h=5,d=mount_d,$fn=20);}}

module front_bezel(){difference(){
  cube([case_w,case_h,depth]);
  translate([bezel,bezel,wall])cube([inner_w,inner_h,depth]);
  translate([bezel+8,bezel+8,-1])cube([inner_w-16,inner_h-16,wall+2]);
  translate([case_w/2-40,-1,depth-18])cube([80,wall+4,12]); // stand slot
}}

module stand_stub(){difference(){
  translate([0,0,0])cube([80,40,12]);
  translate([10,8,-1])cube([60,24,8]);
}}

rear_bay();
