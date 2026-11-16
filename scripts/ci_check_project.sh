#!/usr/bin/env bash
# Check one ISM device project directory (KiCad and/or OpenSCAD).
#
# Env:
#   BASE_SHA  If set (PR base commit), ERC/DRC fail only when head introduces
#             more error-severity violations than the same project at BASE_SHA
#             (matches cad-verify --kicad-mode new intent for shared-lib matrices).
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

count_errors() {
  local rpt="$1"
  if [[ ! -f "$rpt" ]]; then
    echo 0
    return
  fi
  # kicad-cli text reports: lines containing "; error"
  grep -c '; error' "$rpt" || true
}

# If BASE_SHA is set and the project exists there, allow pre-existing errors.
allow_preexisting() {
  local kind="$1" head_rpt="$2" head_input_rel="$3"
  local base_sha="${BASE_SHA:-}"
  if [[ -z "$base_sha" ]]; then
    return 1
  fi
  if ! git -C "$REPO_ROOT" cat-file -e "${base_sha}:${head_input_rel}" 2>/dev/null; then
    echo "No ${kind^^} baseline at ${base_sha}:${head_input_rel} (new project) — head must be clean"
    return 1
  fi

  local tmp
  tmp="$(mktemp -d)"

  git -C "$REPO_ROOT" archive "$base_sha" "$PROJECT_REL" | tar -x -C "$tmp"
  # Also need common libs / tables relative to project when present on base
  if git -C "$REPO_ROOT" cat-file -e "${base_sha}:common/kicad" 2>/dev/null; then
    git -C "$REPO_ROOT" archive "$base_sha" "common/kicad" | tar -x -C "$tmp"
  fi

  local base_input="$tmp/$head_input_rel"
  local base_rpt="$tmp/${kind}-base.rpt"
  if [[ ! -f "$base_input" ]]; then
    rm -rf "$tmp"
    return 1
  fi

  echo "Baseline ${kind} on ${base_sha}..."
  set +e
  if [[ "$kind" == "erc" ]]; then
    kicad-cli sch erc --severity-error --exit-code-violations -o "$base_rpt" "$base_input" >/dev/null 2>&1
  else
    kicad-cli pcb drc --severity-error --exit-code-violations -o "$base_rpt" "$base_input" >/dev/null 2>&1
  fi
  set -e

  local head_n base_n
  head_n="$(count_errors "$head_rpt")"
  base_n="$(count_errors "$base_rpt")"
  echo "Baseline ${kind} errors: ${base_n}; head: ${head_n}"
  if (( head_n <= base_n )); then
    echo "warning: ${kind} errors are pre-existing versus ${base_sha} (not failing)"
    rm -rf "$tmp"
    return 0
  fi
  echo "error: ${kind} introduced $((head_n - base_n)) new error(s) versus ${base_sha}" >&2
  rm -rf "$tmp"
  return 1
}

pro_files=("$PROJECT_DIR"/*.kicad_pro)
scad_files=("$PROJECT_DIR"/*.scad)

if (( ${#pro_files[@]} > 0 )); then
  PRO="${pro_files[0]}"
  SCH="${PRO%.kicad_pro}.kicad_sch"
  PCB="${PRO%.kicad_pro}.kicad_pcb"
  echo "KiCad project: $PRO"

  if [[ -f "$SCH" ]]; then
    echo "ERC..."
    set +e
    kicad-cli sch erc --severity-error --exit-code-violations -o "$PROJECT_DIR/erc.rpt" "$SCH"
    erc_rc=$?
    set -e
    if (( erc_rc != 0 )); then
      sch_rel="${SCH#"$REPO_ROOT"/}"
      if ! allow_preexisting erc "$PROJECT_DIR/erc.rpt" "$sch_rel"; then
        exit "$erc_rc"
      fi
    fi
  else
    echo "warning: no schematic beside project" >&2
  fi

  if [[ -f "$PCB" ]]; then
    echo "DRC..."
    set +e
    kicad-cli pcb drc --severity-error --exit-code-violations -o "$PROJECT_DIR/drc.rpt" "$PCB"
    drc_rc=$?
    set -e
    if (( drc_rc != 0 )); then
      pcb_rel="${PCB#"$REPO_ROOT"/}"
      if ! allow_preexisting drc "$PROJECT_DIR/drc.rpt" "$pcb_rel"; then
        exit "$drc_rc"
      fi
    fi

    # Regenerate fab into temp and diff against committed fab/ (if present)
    FAB_DIR="$(dirname "$PROJECT_DIR")/fab"
    if [[ -d "$FAB_DIR" ]]; then
      TMP="$(mktemp -d)"
      trap 'rm -rf "$TMP"' EXIT
      mkdir -p "$TMP/gen"
      layers="F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste"
      if grep -q 'In1\.Cu\|In1_Cu\|\"In1.Cu\"' "$PCB"; then
        layers="F.Cu,In1.Cu,In2.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste"
      fi
      kicad-cli pcb export gerbers -o "$TMP/gen/" -l "$layers" "$PCB"
      kicad-cli pcb export drill -o "$TMP/gen/" --format excellon --excellon-units mm "$PCB"

      zip_files=("$FAB_DIR"/*gerbers*.zip)
      if (( ${#zip_files[@]} > 0 )); then
        mkdir -p "$TMP/committed"
        unzip -qo "${zip_files[0]}" -d "$TMP/committed"
        echo "Diffing regenerated gerbers vs ${zip_files[0]} ..."
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

# Match tools/cad_verify.py: skip library SCAD with no top-level geometry
# (module/function-only files exit OpenSCAD with empty top-level / rc=1).
scad_has_top_level_geometry() {
  local f="$1"
  REPO_ROOT="$REPO_ROOT" python3 - "$f" <<'PY'
import os, sys
from pathlib import Path
sys.path.insert(0, os.environ["REPO_ROOT"])
from tools.cad_verify import draws_something
src = Path(sys.argv[1]).read_text(errors="replace")
sys.exit(0 if draws_something(src) else 1)
PY
}

if (( ${#scad_files[@]} > 0 )); then
  if ! command -v openscad >/dev/null 2>&1; then
    echo "error: openscad required for $PROJECT_REL" >&2
    exit 1
  fi
  for scad in "${scad_files[@]}"; do
    if ! scad_has_top_level_geometry "$scad"; then
      echo "OpenSCAD skip LIB (no top-level geometry): $scad"
      continue
    fi
    echo "OpenSCAD render: $scad"
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
