// ISM Trackball shell — ball cup + button deck (original ISM)
pcb_w=90; pcb_h=110; wall=3; base_th=3; case_z=28; ball_d=34; cup_z=18;
module bottom(){difference(){
  translate([-wall,-wall,0])cube([pcb_w+2*wall,pcb_h+2*wall,case_z]);
  translate([0,0,base_th])cube([pcb_w,pcb_h,case_z]);
  translate([pcb_w/2-7,-wall-1,base_th+2])cube([14,wall+4,8]);
  // ball cup recess (optics look up from PCB)
  translate([pcb_w/2, pcb_h*0.42, case_z-2])sphere(d=ball_d+2,$fn=48);
  translate([6,6,base_th-0.8])linear_extrude(1)text("ISM TRACKBALL",size=4,font="Liberation Sans:style=Bold");
}for(p=[[5,5],[85,5],[5,105],[85,105]])translate([p[0],p[1],base_th])difference(){cylinder(h=4,d=6,$fn=24);translate([0,0,-0.1])cylinder(h=5,d=2.2,$fn=20);}}
module top(){difference(){
  translate([-wall,-wall,0])cube([pcb_w+2*wall,pcb_h+2*wall,10]);
  translate([2,2,-1])cube([pcb_w-4,pcb_h-4,12]);
  translate([pcb_w/2,pcb_h*0.42,12])sphere(d=ball_d-1,$fn=48);
  translate([pcb_w/2-7,-wall-1,2])cube([14,wall+4,8]);
}}
bottom();
