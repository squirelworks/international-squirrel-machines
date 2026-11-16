#!/usr/bin/env bash
# Export ISM mouse shell to STL + simple STEP boxes
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT"
SCAD="$ROOT/mouse_case.scad"

mkdir -p "$OUT"

if command -v openscad >/dev/null 2>&1; then
  openscad -o "$OUT/mouse_case_bottom.stl" "$SCAD"
  # Top shell via temporary override
  TMP="$(mktemp --suffix=.scad)"
  cat > "$TMP" <<'EOF'
use <mouse_case.scad>
mouse_top();
EOF
  # Fallback: render same file with module call by rewriting
  cat > "$TMP" <<EOF
include <$(basename "$SCAD")>
EOF
  # Simpler: generate top by substituting final call
  sed 's/mouse_shell();/mouse_top();/' "$SCAD" > "$TMP"
  openscad -o "$OUT/mouse_case_top.stl" "$TMP"
  rm -f "$TMP"
else
  echo "openscad not found" >&2
  exit 1
fi

# Minimal ASCII STEP boxes (AP214) for fab handoff when FreeCAD is unavailable
write_step_box() {
  local out="$1" name="$2" x="$3" y="$4" z="$5"
  cat > "$out" <<EOF
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ISM mouse shell approximate bounding box'),'2;1');
FILE_NAME('${name}.step','2026-11-16',('ISM'),('International Squirrel Machines'),'ISM','ISM','');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));
ENDSEC;
DATA;
#1 = CARTESIAN_POINT('ORIGIN',(0.0,0.0,0.0));
#2 = DIRECTION('Z',(0.0,0.0,1.0));
#3 = DIRECTION('X',(1.0,0.0,0.0));
#4 = AXIS2_PLACEMENT_3D('PLACEMENT',#1,#2,#3);
#5 = CARTESIAN_POINT('P1',(0.0,0.0,0.0));
#6 = CARTESIAN_POINT('P2',(${x},0.0,0.0));
#7 = CARTESIAN_POINT('P3',(${x},${y},0.0));
#8 = CARTESIAN_POINT('P4',(0.0,${y},0.0));
#9 = CARTESIAN_POINT('P5',(0.0,0.0,${z}));
#10 = CARTESIAN_POINT('P6',(${x},0.0,${z}));
#11 = CARTESIAN_POINT('P7',(${x},${y},${z}));
#12 = CARTESIAN_POINT('P8',(0.0,${y},${z}));
/* Approximate solid placeholder for ${name}: ${x} x ${y} x ${z} mm */
ENDSEC;
END-ISO-10303-21;
EOF
}

write_step_box "$OUT/mouse_case_bottom.step" "mouse_case_bottom" 110 62 21
write_step_box "$OUT/mouse_case_top.step" "mouse_case_top" 110 62 17

echo "Exported STL + STEP under $OUT"
