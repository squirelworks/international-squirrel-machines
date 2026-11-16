#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SCAD="$ROOT/case.scad"
openscad -o "$ROOT/case_rear.stl" "$SCAD"
TMP="$(mktemp --suffix=.scad)"
sed 's/rear_bay();/front_bezel();/' "$SCAD" > "$TMP"
openscad -o "$ROOT/case_bezel.stl" "$TMP"
sed 's/rear_bay();/stand_stub();/' "$SCAD" > "$TMP"
openscad -o "$ROOT/stand_stub.stl" "$TMP"
rm -f "$TMP"
for name in case_rear case_bezel stand_stub; do
  cat > "$ROOT/${name}.step" <<STEP
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ISM Monitor shell approximate bounding box'),'2;1');
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
