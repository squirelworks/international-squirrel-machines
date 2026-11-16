#!/usr/bin/env bash
# Check one ISM device project directory (KiCad and/or OpenSCAD).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_REL="${1:-}"
if [[ -z "$PROJECT_REL" || "$PROJECT_REL" == "__none__" ]]; then
  echo "ci_check_project: skip (__none__ or empty)"
  exit 0
fi

PROJECT_DIR="$REPO_ROOT/$PROJECT_REL"
if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "error: project dir not found: $PROJECT_DIR" >&2
  exit 1
fi

echo "==> Checking $PROJECT_REL"

shopt -s nullglob

pro_files=("$PROJECT_DIR"/*.kicad_pro)
scad_files=("$PROJECT_DIR"/*.scad)

if (( ${#pro_files[@]} > 0 )); then
  PRO="${pro_files[0]}"
  SCH="${PRO%.kicad_pro}.kicad_sch"
  PCB="${PRO%.kicad_pro}.kicad_pcb"
  echo "KiCad project: $PRO"

  if [[ -f "$SCH" ]]; then
    echo "ERC..."
    kicad-cli sch erc --severity-error --exit-code-violations -o "$PROJECT_DIR/erc.rpt" "$SCH"
  else
    echo "warning: no schematic beside project" >&2
  fi

  if [[ -f "$PCB" ]]; then
    echo "DRC..."
    kicad-cli pcb drc --severity-error --exit-code-violations -o "$PROJECT_DIR/drc.rpt" "$PCB"

    # Regenerate fab into temp and diff against committed fab/ (if present)
    FAB_DIR="$(dirname "$PROJECT_DIR")/fab"
    if [[ -d "$FAB_DIR" ]]; then
      TMP="$(mktemp -d)"
      trap 'rm -rf "$TMP"' EXIT
      mkdir -p "$TMP/gen"
      # Detect copper layers from pcb text (fallback 2)
      layers="F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste"
      if grep -q 'In1\.Cu\|In1_Cu\|\"In1.Cu\"' "$PCB"; then
        layers="F.Cu,In1.Cu,In2.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste"
      fi
      kicad-cli pcb export gerbers -o "$TMP/gen/" -l "$layers" "$PCB"
      kicad-cli pcb export drill -o "$TMP/gen/" --format excellon --excellon-units mm "$PCB"

      # Compare against unzipped committed gerber zip if present
      zip_files=("$FAB_DIR"/*gerbers*.zip)
      if (( ${#zip_files[@]} > 0 )); then
        mkdir -p "$TMP/committed"
        unzip -qo "${zip_files[0]}" -d "$TMP/committed"
        echo "Diffing regenerated gerbers vs ${zip_files[0]} ..."
        # Strip KiCad CreationDate lines so hashes are stable across re-plots
        normalize_gerbers() {
          local dir="$1"
          while IFS= read -r -d '' f; do
            sed -E \
              -e 's/%TF\.CreationDate,[^%]+\*%/%TF.CreationDate,NORMALIZED*%/g' \
              -e 's/(G04 Created by KiCad \(PCBNEW [^)]+\) date ).*/\1NORMALIZED*/' \
              -e 's/"CreationDate": "[^"]+"/"CreationDate": "NORMALIZED"/g' \
              -e 's/(; DRILL file \{KiCad [^}]+\} date ).*/\1NORMALIZED/' \
              -e 's/(; #@! TF\.CreationDate,)[^,]*/\1NORMALIZED/' \
              "$f" > "$f.norm"
            mv "$f.norm" "$f"
          done < <(find "$dir" -type f -print0)
        }
        normalize_gerbers "$TMP/gen"
        normalize_gerbers "$TMP/committed"
        (cd "$TMP/gen" && find . -type f | sort | xargs sha256sum) > "$TMP/gen.sha"
        (cd "$TMP/committed" && find . -type f | sort | xargs sha256sum) > "$TMP/committed.sha"
        if ! diff -u "$TMP/committed.sha" "$TMP/gen.sha"; then
          echo "error: regenerated fab gerbers differ from committed fab/" >&2
          exit 1
        fi
        echo "Fab gerbers match."
      else
        echo "No committed gerber zip under $FAB_DIR — skip fab diff"
      fi
      rm -rf "$TMP"
      trap - EXIT
    fi
  else
    echo "warning: no PCB beside project" >&2
  fi
fi

if (( ${#scad_files[@]} > 0 )); then
  if ! command -v openscad >/dev/null 2>&1; then
    echo "error: openscad required for $PROJECT_REL" >&2
    exit 1
  fi
  for scad in "${scad_files[@]}"; do
    echo "OpenSCAD render: $scad"
    # Prefer --render when available; always emit STL to prove geometry
    if openscad --help 2>&1 | grep -q -- '--render'; then
      openscad --render -o /tmp/ism-ci-out.stl "$scad"
    else
      openscad -o /tmp/ism-ci-out.stl "$scad"
    fi
    rm -f /tmp/ism-ci-out.stl
  done
fi

if (( ${#pro_files[@]} == 0 && ${#scad_files[@]} == 0 )); then
  echo "error: no .kicad_pro or .scad in $PROJECT_DIR" >&2
  exit 1
fi

echo "OK $PROJECT_REL"
