#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SCAD="$ROOT/case.scad"
openscad -o "$ROOT/case_chassis.stl" "$SCAD"
TMP="$(mktemp --suffix=.scad)"
sed 's/chassis();/paper_tray();/' "$SCAD" > "$TMP"
openscad -o "$ROOT/paper_tray.stl" "$TMP"
sed 's/chassis();/lid();/' "$SCAD" > "$TMP"
openscad -o "$ROOT/case_lid.stl" "$TMP"
rm -f "$TMP"
for name in case_chassis paper_tray case_lid; do
  cat > "$ROOT/${name}.step" <<STEP
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ISM Printer shell approximate bounding box'),'2;1');
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
