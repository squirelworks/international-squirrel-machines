# ISM Warship — (#43)

**Program ID:** ISM-WS-1 (study name TBD)  
**This PR:** KiCad scale-model control board slice (navigation / trim / thruster stubs).

## Scope limits (hard)

- **Weapons and combat sensors** appear only as **mass / footprint placeholders** (`interfaces/mass-placeholders.yaml`)
- **No** weapons interfaces, fire control, combat-system internals, seekers, guidance, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) data
- **Public-domain hydrodynamics only** (textbook naval architecture)
- KiCad outputs are **scale-model actuator / telemetry stubs** only

Aircraft carrier sibling: `../aircraft-carrier/` (#45).

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Hull, hydrostatics, stability, powering, placeholders |
| `docs/citations.yaml` | Open / public citations |
| `docs/hydrostatics_examples.py` | Displacement / KB / BM teaching check |
| `interfaces/hydrostatics.yaml` | Machine-readable study hydro numbers |
| `interfaces/mass-placeholders.yaml` | Weapons / combat-sensor mass & footprints only |
| `interfaces/control-board.yaml` | Scale-model control channel map |
| `kicad/ism-warship-control.*` | Study KiCad control board |
| `shell/hull_study.scad` | Simplified hull study OML |

## Roadmap (#43) status
- [x] Design note (hull form, hydrostatics, stability, propulsion/powering, mass/footprint placeholders)
- [x] KiCad boards (scale-model control — this PR)
- [ ] Structural design
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
