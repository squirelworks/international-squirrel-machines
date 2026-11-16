// ISM Full Size keyboard case — parametric OpenSCAD (original ISM design)
unit=19.05; rows=7; margin_x=18; margin_y=24; pcb_extra_x=40; pcb_units_x=25.0; pcb_extra_y=150;
wall=3; base_th=3; lip=1.2; usb_w=14; usb_h=8; mount_d=2.2; badge_depth=0.8;
pcb_w=margin_x*2+pcb_units_x*unit+pcb_extra_x; pcb_h=margin_y+rows*unit+pcb_extra_y;
case_w=pcb_w+2*wall; case_h=pcb_h+2*wall; case_z=18;
module switch_cutouts(){for(r=[0:5],c=[0:24])translate([margin_x+(c+0.5)*unit,margin_y+(r+0.5)*unit,-1])cube([14,14,wall+4],center=true);}
module bottom_shell(){difference(){translate([-wall,-wall,0])cube([case_w,case_h,case_z]);translate([0,0,base_th])cube([pcb_w,pcb_h,case_z]);translate([pcb_w/2-usb_w/2,-wall-1,base_th+2])cube([usb_w,wall+4,usb_h]);translate([6,6,base_th-badge_depth])linear_extrude(height=badge_depth+0.1)text("ISM FULL",size=5,font="Liberation Sans:style=Bold");}for(p=[[8,8],[pcb_w-8,8],[8,pcb_h-8],[pcb_w-8,pcb_h-8]])translate([p[0],p[1],base_th])difference(){cylinder(h=4,d=6,$fn=24);translate([0,0,-0.1])cylinder(h=5,d=mount_d,$fn=20);}}
module top_plate(){difference(){translate([-lip,-lip,0])cube([pcb_w+2*lip,pcb_h+2*lip,wall]);switch_cutouts();translate([margin_x,margin_y+6*unit+2,-1])cube([pcb_units_x*unit,pcb_extra_y-4,wall+2]);}}
module top_frame(){difference(){translate([-wall,-wall,0])cube([case_w,case_h,8]);translate([lip,lip,-1])cube([pcb_w-2*lip,pcb_h-2*lip,10]);translate([pcb_w/2-usb_w/2,-wall-1,2])cube([usb_w,wall+4,usb_h]);}}
bottom_shell();
