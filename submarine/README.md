# ISM Submarine — (#44)

**Program ID:** ISM-SS-1 (study name TBD)  
**This PR:** structural / pressure-hull study slice (rings, casing, sail, spars).

## Scope limits (hard)

- Hull form, stability, trim, and **public-domain hydrodynamics** only
- Sonar and other sensors = **mass / footprint placeholders** only (`interfaces/mass-placeholders.yaml`)
- **No** quieting or acoustic content
- **No** life-support design
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) data
- Structural outputs are **educational pressure-hull layout stubs** — not certified for depth

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Hull, pressure hull concept, ballast/trim, propulsion packaging, scale-model controls |
| `docs/structural.md` | Ring frames / casing / sail / spars study |
| `docs/citations.yaml` | Open / public citations |
| `docs/trim_examples.py` | Trim / reserve-buoyancy teaching check |
| `interfaces/hydrostatics.yaml` | Study displacement / stability stubs |
| `interfaces/mass-placeholders.yaml` | Sonar / sensor mass & footprints only |
| `interfaces/control-board.yaml` | Scale-model control channel map |
| `interfaces/structural.yaml` | Pressure-hull member map |
| `kicad/ism-submarine-control.*` | Study KiCad control board |
| `shell/hull_study.scad` | Hull + ghost structural layout |

## Roadmap (#44) status
- [x] Design note (hull form, pressure hull concept, ballast/trim, propulsion packaging, controls for scale model)
- [x] KiCad boards (scale-model control)
- [x] Structural / pressure hull design (this PR)
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
