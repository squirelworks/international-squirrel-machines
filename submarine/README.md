# ISM Submarine — B3 (#44)

**Program ID:** ISM-SS-1 (study name TBD)  
**Plan:** Fred research plan B3 — hull study and printable scale model.

## Scope limits (hard)

- Hull form, stability, trim, and **public-domain hydrodynamics** only
- Sonar and other sensors = **mass / footprint placeholders** only (`interfaces/mass-placeholders.yaml`)
- **No** quieting or acoustic content
- **No** life-support design
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) data

## B3 deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Hull, pressure hull concept, ballast/trim, propulsion packaging, scale-model controls |
| `docs/citations.yaml` | Open / public citations |
| `docs/trim_examples.py` | Trim / reserve-buoyancy teaching check |
| `interfaces/hydrostatics.yaml` | Study displacement / stability stubs |
| `interfaces/mass-placeholders.yaml` | Sonar / sensor mass & footprints only |
| `shell/hull_study.scad` | Printable scale-model hull study |

## Roadmap (#44) status after B3
- [x] Design note (hull form, pressure hull concept, ballast/trim, propulsion packaging, controls for scale model)
- [ ] KiCad boards (scale-model control)
- [ ] Structural / pressure hull design
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
