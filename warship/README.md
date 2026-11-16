# ISM Warship — (#43)

**Program ID:** ISM-WS-1 (study name TBD)  
**This PR:** structural study slice (keel / frames / decks / bulkheads).

## Scope limits (hard)

- **Weapons and combat sensors** appear only as **mass / footprint placeholders** (`interfaces/mass-placeholders.yaml`)
- **No** weapons interfaces, fire control, combat-system internals, seekers, guidance, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) data
- **Public-domain hydrodynamics only** (textbook naval architecture)
- Structural outputs are **educational layout stubs** — not certified scantlings

Aircraft carrier sibling: `../aircraft-carrier/` (#45).

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Hull, hydrostatics, stability, powering, placeholders |
| `docs/structural.md` | Keel / frames / decks / bulkheads study |
| `docs/citations.yaml` | Open / public citations |
| `docs/hydrostatics_examples.py` | Displacement / KB / BM teaching check |
| `interfaces/hydrostatics.yaml` | Machine-readable study hydro numbers |
| `interfaces/mass-placeholders.yaml` | Weapons / combat-sensor mass & footprints only |
| `interfaces/control-board.yaml` | Scale-model control channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-warship-control.*` | Study KiCad control board |
| `shell/hull_study.scad` | Hull + ghost structural layout |

## Roadmap (#43) status
- [x] Design note (hull form, hydrostatics, stability, propulsion/powering, mass/footprint placeholders)
- [x] KiCad boards (scale-model control)
- [x] Structural design (this PR)
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
