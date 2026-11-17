# Gundam — Gerbers + mechanical files (#46)

**Product:** ISM-MS-1  
**Slice:** study Gerber package for the educational control board + OpenSCAD frame STL export.

## Scope limits (hard)

- Mecha frame / actuator packaging only
- Stores / hardpoints = **mass, footprint, SAFE/INHIBIT** stubs only
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming codes
- **No** live launch / fire sequences or engagement doctrine
- **No** ITAR/EAR content
- Structural / STL outputs remain **educational frame stubs**

## Deliverables

| Path | Role |
|------|------|
| `../fab/ism-gundam-control-gerbers.zip` | Gerber + drill study package |
| `../fab/ism-gundam-control-cpl.csv` | Centroid |
| `../fab/BOM.csv` | Educational BOM stub |
| `../mechanical/frame_study.stl` | Torso / limb / inert-stores ghost STL |

## Next

BOM / assembly notes: `bom.md`, `assembly.md` (this program track). Remaining: polish / inquire-for-release.
