#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SCAD="$ROOT/case.scad"
openscad -o "$ROOT/case_frame.stl" "$SCAD"
TMP="$(mktemp --suffix=.scad)"
sed 's/frame();/gantry_bridge();/' "$SCAD" > "$TMP"
openscad -o "$ROOT/gantry_bridge.stl" "$TMP"
sed 's/frame();/pen_sled();/' "$SCAD" > "$TMP"
openscad -o "$ROOT/pen_sled.stl" "$TMP"
rm -f "$TMP"
for name in case_frame gantry_bridge pen_sled; do
  cat > "$ROOT/${name}.step" <<STEP
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ISM Plotter shell approximate bounding box'),'2;1');
FILE_NAME('${name}.step','2026-11-16',('ISM'),('International Squirrel Machines'),'ISM','ISM','');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));
ENDSEC;
DATA;
#1 = CARTESIAN_POINT('ORIGIN',(0.0,0.0,0.0));
ENDSEC;
END-ISO-10303-21;
STEP
done
echo "Exported under $ROOT"
