# Submarine — Gerbers + mechanical files (#44)

**Product:** ISM-SS-1  
**Slice:** study Gerber package for the scale-model control board + OpenSCAD hull STL export.

## Scope limits (hard) — B3 spirit

- Hull form / scale-model control only
- Sonar and sensors = **mass / footprint** placeholders
- **No** quieting or acoustic signature design
- **No** weapons, seekers, guidance, warheads, or fuzing
- **No** ITAR/EAR content

## Deliverables

| Path | Role |
|------|------|
| `../fab/ism-submarine-control-gerbers.zip` | Gerber + drill study package |
| `../fab/ism-submarine-control-cpl.csv` | Centroid |
| `../fab/BOM.csv` | Educational BOM stub |
| `../mechanical/hull_study.stl` | Ghost hull / rings / casing STL |

## Next (not this PR)

Master BOM / assembly polish, inquire-for-release.
