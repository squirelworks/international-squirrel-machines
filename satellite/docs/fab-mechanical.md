# Satellite — Gerbers + mechanical files (#31)

**Product:** ISM-SAT-1  
**Slice:** study Gerber package for the educational bus board + OpenSCAD 3U bus STL export.

## Scope limits (hard)

- Civilian / educational bus + payload packaging only
- Payload = **mass / power / data** placeholders only
- **No** weapons, seekers, guidance-to-target, warheads, or fuzing
- **No** ITAR/EAR content
- Structural / STL outputs remain **educational 3U layout stubs**

## Deliverables

| Path | Role |
|------|------|
| `../fab/ism-satellite-bus-gerbers.zip` | Gerber + drill study package |
| `../fab/ism-satellite-bus-cpl.csv` | Centroid |
| `../fab/BOM.csv` | Educational BOM stub |
| `../mechanical/bus_study.stl` | Ghost 3U rails / trays STL |

## Next (not this PR)

Master BOM / assembly polish, inquire-for-release.
