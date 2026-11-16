# Rocket — Gerbers + mechanical files (#41)

**Product:** ISM-RK-1  
**Slice:** study Gerber package for the passive logger / recovery board + OpenSCAD airframe STL export.

## Scope limits (hard)

- Hobby airframe / passive avionics packaging only
- **No** guidance, steering, or active flight control
- **No** ballistic-missile or reentry-vehicle content
- Certified commercial hobby motors only (public catalogs)
- **No** ITAR/EAR content
- Structural / STL outputs remain **educational layout stubs**

## Deliverables

| Path | Role |
|------|------|
| `../fab/ism-rocket-logger-gerbers.zip` | Gerber + drill study package |
| `../fab/ism-rocket-logger-cpl.csv` | Centroid |
| `../fab/BOM.csv` | Educational BOM stub |
| `../mechanical/airframe_study.stl` | Ghost body / fins / rings STL |

## Next (not this PR)

Master BOM / assembly polish, inquire-for-release.
