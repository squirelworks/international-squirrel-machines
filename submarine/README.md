# ISM Submarine — (#44)

**Program ID:** ISM-SS-1 (study name TBD)  
**Status:** design note → KiCad → structural → Gerbers/STL → BOM/assembly in-tree; polish / inquire still open.

## Prior slices
Design-note (hull / trim / packaging). KiCad scale-model control board. Structural rings / casing. Gerbers + hull STL. This PR adds educational master BOM + assembly sequence.

## Scope limits (hard) — B3 spirit

- Hull form, stability, trim and public-domain hydrodynamics only
- Sonar and other sensors = **mass / footprint** placeholders
- **No** quieting or acoustic content
- **No** life-support design
- **No** weapons, seekers, guidance, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) data

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Hull / trim / packaging |
| `docs/structural.md` | Pressure-hull rings / casing study |
| `docs/fab-mechanical.md` | Gerber + STL notes |
| `docs/bom.md` | Educational master BOM |
| `docs/assembly.md` | Study assembly sequence |
| `interfaces/*.yaml` | Hydrostatics / mass / board / structure |
| `kicad/ism-submarine-control.*` | Scale-model control board |
| `fab/` | Study Gerbers + CPL + BOM stub |
| `shell/hull_study.scad` | Hull + ghost structure |
| `mechanical/hull_study.stl` | Exported study STL |

## Roadmap (#44) status
- [x] Design note (hull form, pressure hull concept, ballast/trim, propulsion packaging, controls for scale model)
- [x] KiCad boards (scale-model control)
- [x] Structural / pressure hull design
- [x] Gerbers + mechanical files
- [x] BOM / assembly
- [ ] Polish and inquire for release
