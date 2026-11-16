// ISM Printer shell — chassis + paper tray (original ISM)
body_w=220; body_d=160; body_h=80; wall=3.5;
pcb_w=100; pcb_h=70; usb_w=14; usb_h=8; mount_d=2.2; badge_depth=0.8;
tray_w=180; tray_d=40; tray_h=8;

module chassis(){difference(){
  cube([body_w,body_d,body_h]);
  translate([wall,wall,wall])cube([body_w-2*wall,body_d-2*wall,body_h]);
  translate([body_w/2-tray_w/2,-1,body_h-tray_h-wall])cube([tray_w,tray_d+wall+2,tray_h]);
  translate([12,body_d-pcb_h-8,wall])cube([pcb_w+2,pcb_h+2,20]);
  translate([12+pcb_w/2-usb_w/2,body_d-wall-1,wall+6])cube([usb_w,wall+4,usb_h]);
  translate([16,body_d-pcb_h,wall-badge_depth])linear_extrude(height=badge_depth+0.1)
    text("ISM PRINTER",size=5,font="Liberation Sans:style=Bold");
}for(p=[[16,body_d-pcb_h-4],[16+pcb_w-4,body_d-pcb_h-4],[16,body_d-12],[16+pcb_w-4,body_d-12]])
  translate([p[0],p[1],wall])difference(){cylinder(h=4,d=6,$fn=24);translate([0,0,-0.1])cylinder(h=5,d=mount_d,$fn=20);}}

module paper_tray(){difference(){
  cube([tray_w,tray_d,tray_h]);
  translate([2,2,2])cube([tray_w-4,tray_d-4,tray_h]);
}}

module lid(){difference(){
  cube([body_w+2,body_d+2,wall]);
  translate([body_w/2-tray_w/2+1,0,-1])cube([tray_w,tray_d+4,wall+2]);
}}

chassis();
