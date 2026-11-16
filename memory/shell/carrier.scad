// ISM Memory RAM module carrier tray (original ISM)
pcb_w=80; pcb_h=36; wall=2.5; base_th=2; tray_z=8; lip=1.2; edge_cut=4;
module tray(){difference(){
  translate([-wall,-wall,0])cube([pcb_w+2*wall,pcb_h+2*wall,tray_z]);
  translate([0,0,base_th])cube([pcb_w,pcb_h,tray_z]);
  // edge finger access slot
  translate([-1,pcb_h-edge_cut,base_th])cube([pcb_w+2,edge_cut+wall+1,tray_z]);
  translate([4,4,base_th-0.6])linear_extrude(0.7)text("ISM RAM",size=4,font="Liberation Sans:style=Bold");
}for(p=[[3.5,3.5],[pcb_w-3.5,3.5]])translate([p[0],p[1],base_th])difference(){cylinder(h=3,d=5,$fn=24);translate([0,0,-0.1])cylinder(h=4,d=2.2,$fn=20);}}
module lid(){difference(){
  translate([-wall,-wall,0])cube([pcb_w+2*wall,pcb_h+2*wall-edge_cut,3]);
  translate([lip,lip,-1])cube([pcb_w-2*lip,pcb_h-2*lip-edge_cut,5]);
}}
tray();
