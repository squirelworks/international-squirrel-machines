// ISM Drawing Pad small shell (original ISM)
pcb_w=100.0; pcb_h=75.0; active_w=80.0; active_h=50.0;
wall=3; base_th=3; case_z=12; lip=1.2; usb_w=14; usb_h=8; mount_d=2.2;
ax=(pcb_w-active_w)/2; ay=12;
module bottom(){difference(){
  translate([-wall,-wall,0])cube([pcb_w+2*wall,pcb_h+2*wall,case_z]);
  translate([0,0,base_th])cube([pcb_w,pcb_h,case_z]);
  translate([pcb_w/2-usb_w/2,-wall-1,base_th+2])cube([usb_w,wall+4,usb_h]);
  translate([ax,ay,case_z-1])cube([active_w,active_h,3]);
  translate([6,6,base_th-0.7])linear_extrude(0.8)text("ISM PAD SMALL",size=4,font="Liberation Sans:style=Bold");
}for(p=[[4,4],[pcb_w-4,4],[4,pcb_h-4],[pcb_w-4,pcb_h-4]])translate([p[0],p[1],base_th])difference(){cylinder(h=3.5,d=5.5,$fn=24);translate([0,0,-0.1])cylinder(h=4.5,d=mount_d,$fn=20);}}
module top(){difference(){
  translate([-wall,-wall,0])cube([pcb_w+2*wall,pcb_h+2*wall,6]);
  translate([lip,lip,-1])cube([pcb_w-2*lip,pcb_h-2*lip,8]);
  translate([ax,ay,-1])cube([active_w,active_h,10]);
  translate([pcb_w/2-usb_w/2,-wall-1,1])cube([usb_w,wall+4,usb_h]);
}}
module stylus(){
  // holder clip at rear
  translate([pcb_w-18,pcb_h-10,0])difference(){
    cube([14,8,10]);
    translate([2,2,-1])cube([10,4,12]);
  }
}
bottom();
