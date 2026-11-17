# Fighter Jet — Gerbers + study shell STL (#85)

**Product:** ISM-FJ-1 “Nutcracker”  
**Slice:** study Gerber package for the avionics-bay I/O board + OpenSCAD airframe STL export.

## Scope limits (hard)

- Bay board = surface / throttle PWM stubs only
- Program stores / weapons remain **mass / footprint / SAFE / INHIBIT** placeholders (see `sensors-weapons/`)
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming codes
- **No** ITAR/EAR content
- Shell STL is a **reduced-scale study model**, not production tooling

## Deliverables

| Path | Role |
|------|------|
| `../fab/ism-fighter-jet-gerbers.zip` | Gerber + drill study package |
| `../fab/ism-fighter-jet-cpl.csv` | Centroid |
| `../fab/BOM.csv` | Educational BOM stub |
| `../shell/airframe.stl` | Study airframe STL (beside `airframe.scad`; `mechanical/` stays design docs) |

## Next

Bay/study BOM / assembly notes: `bom.md`, `assembly.md` (this program track). Remaining: #78 Soft blockers / open product decisions / inquire-for-release.
