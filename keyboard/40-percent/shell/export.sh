#!/usr/bin/env bash
# Export ISM 40% keyboard shell to STL + simple STEP boxes
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SCAD="$ROOT/case.scad"
OUT="$ROOT"

mkdir -p "$OUT"

if ! command -v openscad >/dev/null 2>&1; then
  echo "openscad not found" >&2
  exit 1
fi

openscad -o "$OUT/case_bottom.stl" "$SCAD"

TMP="$(mktemp --suffix=.scad)"
sed 's/bottom_shell();/top_plate();/' "$SCAD" > "$TMP"
openscad -o "$OUT/case_plate.stl" "$TMP"
sed 's/bottom_shell();/top_frame();/' "$SCAD" > "$TMP"
openscad -o "$OUT/case_top_frame.stl" "$TMP"
rm -f "$TMP"

write_step_box() {
  local out="$1" name="$2" x="$3" y="$4" z="$5"
  cat > "$out" <<EOF
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ISM 40% keyboard shell approximate bounding box'),'2;1');
FILE_NAME('${name}.step','2026-11-16',('ISM'),('International Squirrel Machines'),'ISM','ISM','');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));
ENDSEC;
DATA;
#1 = CARTESIAN_POINT('ORIGIN',(0.0,0.0,0.0));
#2 = DIRECTION('Z',(0.0,0.0,1.0));
#3 = DIRECTION('X',(1.0,0.0,0.0));
#4 = AXIS2_PLACEMENT_3D('PLACEMENT',#1,#2,#3);
/* Approximate solid placeholder for ${name}: ${x} x ${y} x ${z} mm */
ENDSEC;
END-ISO-10303-21;
EOF
}

# pcb_w ≈ 304.6; pcb_h ≈ 240.2
write_step_box "$OUT/case_bottom.step" "case_bottom" 312 248 18
write_step_box "$OUT/case_plate.step" "case_plate" 308 244 3
write_step_box "$OUT/case_top_frame.step" "case_top_frame" 312 248 8

echo "Exported STL + STEP under $OUT"
