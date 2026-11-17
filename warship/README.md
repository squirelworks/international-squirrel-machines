# ISM Warship — (#43)

**Program ID:** ISM-WS-1 (study name TBD)  
**This PR:** BOM / assembly notes for the study Gerbers + hull STL package.

## Prior slices
B2 hydrostatics design note + deepen. KiCad scale-model control board. Structural keel/frames/decks. Gerbers + hull STL. This PR adds educational master BOM + assembly sequence.

## Scope limits (hard)

- **Weapons and combat sensors** appear only as **mass / footprint placeholders** (`interfaces/mass-placeholders.yaml`)
- **No** weapons interfaces, fire control, combat-system internals, seekers, guidance, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) data
- **Public-domain hydrodynamics only** (textbook naval architecture)
- Fab/STL/BOM outputs are **educational study packages** — not certified

Aircraft carrier sibling: `../aircraft-carrier/` (#45).

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Hull, hydrostatics, stability, powering, placeholders |
| `docs/structural.md` | Keel / frames / decks / bulkheads study |
| `docs/fab-mechanical.md` | Gerber + STL notes |
| `docs/bom.md` | Educational master BOM |
| `docs/assembly.md` | Study assembly sequence |
| `docs/citations.yaml` | Open / public citations |
| `docs/hydrostatics_examples.py` | Displacement / KB / BM teaching check |
| `interfaces/hydrostatics.yaml` | Machine-readable study hydro numbers |
| `interfaces/mass-placeholders.yaml` | Weapons / combat-sensor mass & footprints only |
| `interfaces/control-board.yaml` | Scale-model control channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-warship-control.*` | Study KiCad control board |
| `fab/` | Study Gerbers + CPL + BOM stub |
| `shell/hull_study.scad` | Hull + ghost structural layout |
| `mechanical/hull_study.stl` | Exported study STL |

## Roadmap (#43) status
- [x] Design note (hull form, hydrostatics, stability, propulsion/powering, mass/footprint placeholders)
- [x] KiCad boards (scale-model control)
- [x] Structural design
- [x] Gerbers + mechanical files
- [x] BOM / assembly (this PR)
- [ ] Polish and inquire for release

## Weapons boundary
Weapons / combat sensors = **mass / footprint only**. Never fire control, seekers, guidance, warheads, or fuzing in-repo.
