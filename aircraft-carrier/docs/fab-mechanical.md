# Aircraft carrier — Gerbers + mechanical files (#45)

**Product:** ISM-CV-1  
**Slice:** study Gerber package for the scale-model deck control board + OpenSCAD deck STL export.

## Scope limits (hard)

- Deck / aviation packaging and scale-model control only
- Weapons / combat sensors / aviation ordnance = **mass / footprint** placeholders only
- **No** fire control, combat-system internals, seekers, guidance, warheads, or fuzing
- Catapult / arresting = load/mass/keep-out stubs only
- **No** ITAR/EAR content
- Structural / STL outputs remain **educational layout stubs**

## Deliverables

| Path | Role |
|------|------|
| `../fab/ism-carrier-deck-gerbers.zip` | Gerber + drill study package |
| `../fab/ism-carrier-deck-cpl.csv` | Centroid |
| `../fab/BOM.csv` | Educational BOM stub |
| `../mechanical/deck_study.stl` | Ghost deck / hangar / frames STL |

## Next (not this PR)

Master BOM / assembly polish, inquire-for-release.
