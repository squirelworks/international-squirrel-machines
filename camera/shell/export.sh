#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SCAD="$ROOT/case.scad"
openscad -o "$ROOT/case_body.stl" "$SCAD"
TMP="$(mktemp --suffix=.scad)"
sed 's/body();/lens_tube();/' "$SCAD" > "$TMP"
openscad -o "$ROOT/lens_tube.stl" "$TMP"
sed 's/body();/back_plate();/' "$SCAD" > "$TMP"
openscad -o "$ROOT/back_plate.stl" "$TMP"
rm -f "$TMP"
for name in case_body lens_tube back_plate; do
  cat > "$ROOT/${name}.step" <<STEP
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ISM Camera shell approximate bounding box'),'2;1');
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
