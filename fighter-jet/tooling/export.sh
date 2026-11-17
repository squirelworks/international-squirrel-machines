#!/usr/bin/env bash
# Export study STL (+ placeholder STEP) for every tooling OpenSCAD solid (#106 / 4b).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
DATE="$(date -u +%Y-%m-%d)"

export_one() {
  local scad="$1"
  local out_base="$2"
  local dir
  dir="$(dirname "$scad")"
  echo "STL  $scad -> $dir/${out_base}.stl"
  if openscad --help 2>&1 | grep -q -- '--render'; then
    openscad --render -o "$dir/${out_base}.stl" "$scad"
  else
    openscad -o "$dir/${out_base}.stl" "$scad"
  fi
  cat > "$dir/${out_base}.step" <<STEP
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ISM-FJ-1 tooling study approximate solid — ${out_base}'),'2;1');
FILE_NAME('${out_base}.step','${DATE}',('ISM'),('International Squirrel Machines'),'ISM','ISM','');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));
ENDSEC;
DATA;
#1 = CARTESIAN_POINT('ORIGIN',(0.0,0.0,0.0));
ENDSEC;
END-ISO-10303-21;
STEP
  echo "STEP $dir/${out_base}.step (study placeholder bbox marker)"
}

export_one "$ROOT/jigs/fuselage_splice_jig.scad" fuselage_splice_jig
export_one "$ROOT/jigs/wing_box_jig.scad" wing_box_jig
export_one "$ROOT/jigs/empennage_jig.scad" empennage_jig
export_one "$ROOT/fixtures/drill_rivet_fixture.scad" drill_rivet_fixture
export_one "$ROOT/layup/wing_skin_layup_tool.scad" wing_skin_layup_tool
export_one "$ROOT/layup/canopy_layup_mandrel.scad" canopy_layup_mandrel
export_one "$ROOT/layup/intake_layup_mandrel.scad" intake_layup_mandrel
export_one "$ROOT/dies/skin_form_die.scad" skin_form_die

echo "Exported tooling solids under $ROOT"
