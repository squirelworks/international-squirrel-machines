# Warship — Gerbers + mechanical files (#43)

**Product:** ISM-WS-1  
**Slice:** study Gerber package for the scale-model control board + OpenSCAD hull STL export.

## Scope limits (hard)

- Hull form / scale-model control only
- Weapons and combat sensors = **mass / footprint** placeholders only
- **No** fire control, combat-system internals, seekers, guidance, warheads, or fuzing
- **No** ITAR/EAR content
- Structural / STL outputs remain **educational layout stubs**

## Deliverables

| Path | Role |
|------|------|
| `../fab/ism-warship-control-gerbers.zip` | Gerber + drill study package |
| `../fab/ism-warship-control-cpl.csv` | Centroid |
| `../fab/BOM.csv` | Educational BOM stub |
| `../mechanical/hull_study.stl` | Ghost hull / keel / frames STL |

## Next

BOM / assembly notes: `bom.md`, `assembly.md` (this program track). Remaining: polish / inquire-for-release.
