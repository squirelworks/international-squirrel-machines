#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SCAD="$ROOT/case.scad"
openscad -o "$ROOT/case_bottom.stl" "$SCAD"
TMP="$(mktemp --suffix=.scad)"
sed 's/bottom();/top();/' "$SCAD" > "$TMP"
openscad -o "$ROOT/case_top.stl" "$TMP"
sed 's/bottom();/stylus();/' "$SCAD" > "$TMP"
openscad -o "$ROOT/stylus_holder.stl" "$TMP"
rm -f "$TMP"
for name in case_bottom case_top stylus_holder; do
  cat > "$ROOT/${name}.step" <<STEP
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ISM Drawing Pad medium shell'),'2;1');
FILE_NAME('${name}.step','2026-11-16',('ISM'),('International Squirrel Machines'),'ISM','ISM','');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));
ENDSEC;
DATA;
#1 = CARTESIAN_POINT('ORIGIN',(0.0,0.0,0.0));
ENDSEC;
END-ISO-10303-21;
STEP
done
echo "Exported $ROOT"
