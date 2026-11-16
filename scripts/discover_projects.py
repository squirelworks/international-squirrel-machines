#!/usr/bin/env python3
"""Discover ISM device projects for CI matrix.

A project is a deepest directory that directly contains a ``.kicad_pro`` or
``.scad`` file. Emits GitHub Actions matrix JSON on stdout.

Usage:
  discover_projects.py --all
  discover_projects.py --base <sha> --head <sha>
  discover_projects.py --changed-files file1 file2 ...
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SKIP_DIR_NAMES = {
    ".git",
    "node_modules",
    "__pycache__",
    "build",
    "gerbers_tmp",
    ".pico-sdk",
}

SHARED_TRIGGERS = (
    "common/",
    ".github/workflows/",
    "common/kicad/",
)

# Device generators under scripts/ map to a device prefix — do NOT expand to all projects.
# Only shared CI/helpers under scripts/ should force a full matrix.
SCRIPT_DEVICE_PREFIXES = (
    ("scripts/build_keyboard_large.py", "keyboard/large/"),
    ("scripts/build_keyboard_40.py", "keyboard/40-percent/"),
    ("scripts/build_keyboard_full.py", "keyboard/full-size/"),
    ("scripts/build_keyboard_tkl.py", "keyboard/tkl/"),
    ("scripts/build_keyboard_75.py", "keyboard/75-percent/"),
    ("scripts/build_keyboard_65.py", "keyboard/65-percent/"),
    ("scripts/build_keyboard_final.py", "keyboard/60-percent/"),
    ("scripts/build_keyboard_60_mod.py", "keyboard/60-percent/"),
    ("scripts/build_trackball.py", "trackball/"),
    ("scripts/build_mouse.py", "mouse/"),
)

SHARED_SCRIPTS = (
    "scripts/ci_check_project.sh",
    "scripts/discover_projects.py",
    "scripts/ism_hw/",
)


def _is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def find_projects(root: Path | None = None) -> list[str]:
    root = root or REPO_ROOT
    projects: set[Path] = set()
    for dirpath, dirnames, filenames in os.walk(root):
        p = Path(dirpath)
        rel_parts = p.relative_to(root).parts if p != root else ()
        if any(part in SKIP_DIR_NAMES for part in rel_parts):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        has_pro = any(f.endswith(".kicad_pro") for f in filenames)
        has_scad = any(f.endswith(".scad") for f in filenames)
        if has_pro or has_scad:
            projects.add(p.relative_to(root))

    # Deepest only: skip a dir if a descendant project exists under it
    kept: list[Path] = []
    for cand in sorted(projects, key=lambda x: (-len(x.parts), str(x))):
        if any(other != cand and str(other).startswith(str(cand) + "/") for other in projects):
            continue
        kept.append(cand)
    return sorted(str(p).replace("\\", "/") for p in kept)


def changed_files_from_git(base: str, head: str) -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...{head}"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        # fallback: show files in head
        proc = subprocess.run(
            ["git", "diff", "--name-only", base, head],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    files = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    return files


def map_files_to_projects(files: list[str], all_projects: list[str]) -> list[str]:
    if not files:
        return []

    # Shared / unclear deps → all projects
    for f in files:
        norm = f.replace("\\", "/")
        if any(norm == t.rstrip("/") or norm.startswith(t) for t in SHARED_TRIGGERS):
            return list(all_projects)
        if norm.endswith(".kicad_sym") or "/ISM.pretty/" in norm or norm.endswith(".kicad_mod"):
            if norm.startswith("common/"):
                return list(all_projects)

    selected: set[str] = set()
    for f in files:
        norm = f.replace("\\", "/")
        matched_any = False

        # Shared CI helpers → full matrix
        if any(norm == s.rstrip("/") or norm.startswith(s) for s in SHARED_SCRIPTS):
            return list(all_projects)

        # Device-specific generators → that device's projects only
        for script, prefix in SCRIPT_DEVICE_PREFIXES:
            if norm == script or norm.startswith(script):
                for proj in all_projects:
                    if proj == prefix.rstrip("/") or proj.startswith(prefix):
                        selected.add(proj)
                matched_any = True
                break
        if matched_any:
            continue

        for proj in all_projects:
            if norm == proj or norm.startswith(proj + "/"):
                selected.add(proj)
                matched_any = True
                continue
            # Sibling paths under the same device folder as a project
            # e.g. mouse/README.md → mouse/shell; keyboard/60-percent/firmware → …
            parent = str(Path(proj).parent).replace("\\", "/")
            if parent not in ("", ".") and (norm == parent or norm.startswith(parent + "/")):
                selected.add(proj)
                matched_any = True
        if not matched_any and norm.startswith("scripts/"):
            # Unknown scripts/ change — conservative full matrix
            return list(all_projects)
    return sorted(selected)


def matrix_payload(projects: list[str]) -> dict:
    if not projects:
        return {"include": [{"project": "__none__"}]}
    return {"include": [{"project": p} for p in projects]}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true", help="Emit every discovered project")
    ap.add_argument("--base", help="Git base SHA/ref for PR discovery")
    ap.add_argument("--head", help="Git head SHA/ref for PR discovery")
    ap.add_argument("--changed-files", nargs="*", help="Explicit changed file list")
    ap.add_argument("--pretty", action="store_true")
    args = ap.parse_args(argv)

    projects = find_projects()

    if args.all:
        selected = projects
    elif args.changed_files is not None:
        selected = map_files_to_projects(args.changed_files, projects)
    elif args.base and args.head:
        selected = map_files_to_projects(changed_files_from_git(args.base, args.head), projects)
    else:
        # Default: all (safe for local runs)
        selected = projects

    payload = matrix_payload(selected)
    if args.pretty:
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
