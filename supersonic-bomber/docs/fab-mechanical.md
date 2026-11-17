# Supersonic bomber — Gerbers + mechanical files (#39)

**Product:** ISM-XB-1  
**Slice:** study Gerber package for the inert-bay SAFE/INHIBIT board + OpenSCAD airframe STL export.

## Weapons boundary (hard)

- Payload / bay = **inert mass, CG, volume, SAFE/INHIBIT** only
- Structural bay cutout remains an **inert volume keep-out**
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming
- **No** ITAR/EAR munition or fire-control designs

## Deliverables

| Path | Role |
|------|------|
| `../fab/ism-xb-bay-gerbers.zip` | Gerber + drill study package |
| `../fab/ism-xb-bay-cpl.csv` | Centroid |
| `../fab/BOM.csv` | Educational BOM stub |
| `../mechanical/airframe_study.stl` | Ghost airframe / bay keep-out STL |

## Next

BOM / assembly notes: `bom.md`, `assembly.md` (this program track). Remaining: polish / inquire-for-release.
