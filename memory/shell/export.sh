#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SCAD="$ROOT/carrier.scad"
openscad -o "$ROOT/carrier_tray.stl" "$SCAD"
TMP="$(mktemp --suffix=.scad)"
sed 's/tray();/lid();/' "$SCAD" > "$TMP"
openscad -o "$ROOT/carrier_lid.stl" "$TMP"
rm -f "$TMP"
for name in carrier_tray carrier_lid; do
  cat > "$ROOT/${name}.step" <<STEP
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ISM Memory carrier approximate bounding box'),'2;1');
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
