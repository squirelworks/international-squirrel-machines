#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SCAD="$ROOT/case.scad"
openscad -o "$ROOT/reader.stl" "$SCAD"
TMP="$(mktemp --suffix=.scad)"
sed 's/reader();/card_shell();/' "$SCAD" > "$TMP"
openscad -o "$ROOT/card_shell.stl" "$TMP"
rm -f "$TMP"
for name in reader card_shell; do
  cat > "$ROOT/${name}.step" <<STEP
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ISM Flash Cards shell approximate bounding box'),'2;1');
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
