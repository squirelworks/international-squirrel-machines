#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SCAD="$ROOT/case.scad"
openscad -o "$ROOT/stick.stl" "$SCAD"
TMP="$(mktemp --suffix=.scad)"
sed 's/stick();/cap();/' "$SCAD" > "$TMP"
openscad -o "$ROOT/cap.stl" "$TMP"
rm -f "$TMP"
for name in stick cap; do
  cat > "$ROOT/${name}.step" <<STEP
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ISM Thumb Drive shell approximate bounding box'),'2;1');
FILE_NAME('${name}.step','2026-11-17',('ISM'),('International Squirrel Machines'),'ISM','ISM','');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));
ENDSEC;
DATA;
#1 = CARTESIAN_POINT('ORIGIN',(0.0,0.0,0.0));
ENDSEC;
END-ISO-10303-21;
STEP
done
echo "Exported under $ROOT"
