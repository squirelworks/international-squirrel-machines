# ISM Warship — B2 (#43)

**Program ID:** ISM-WS-1 (study name TBD)  
**Plan:** Fred research plan B2 — hull form, hydrostatics, stability, powering.

## Scope limits (hard)

- **Weapons and combat sensors** appear only as **mass / footprint placeholders** (`interfaces/mass-placeholders.yaml`)
- **No** weapons interfaces, fire control, combat-system internals, seekers, guidance, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) data
- **Public-domain hydrodynamics only** (textbook naval architecture)

Aircraft carrier flight-deck / aviation packaging as a sibling study: `../aircraft-carrier/` (roadmap [#45](https://github.com/squirelworks/international-squirrel-machines/issues/45); B2 includes a light design-note slice with the same weapons/sensor placeholder rule).

## B2 deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Hull, hydrostatics, stability, powering, placeholders |
| `docs/citations.yaml` | Open / public citations |
| `docs/hydrostatics_examples.py` | Displacement / KB / BM teaching check |
| `interfaces/hydrostatics.yaml` | Machine-readable study hydro numbers |
| `interfaces/mass-placeholders.yaml` | Weapons / combat-sensor mass & footprints only |
| `shell/hull_study.scad` | Simplified hull study OML |

## Roadmap (#43) status after B2
- [x] Design note (hull form, hydrostatics, stability, propulsion/powering, mass/footprint placeholders)
- [ ] KiCad boards (navigation, power, scale-model control)
- [ ] Structural design
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
