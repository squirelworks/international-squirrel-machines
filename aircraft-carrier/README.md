# ISM Aircraft Carrier — (#45)

**Program ID:** ISM-CV-1 (study name TBD)  
**This PR:** KiCad scale-model deck control board slice.

## Scope limits (hard)

- Weapons and combat sensors = **mass / footprint / KG placeholders** only
- Aviation ordnance = **inert mass boxes** only
- **No** weapons interfaces, fire control, combat-system internals
- **No** seekers, guidance, warheads, fuzing, arming codes, or engagement doctrine
- **No** export-controlled (ITAR/EAR) combat or acoustic data
- Catapult / arresting gear = load/mass/keep-out stubs (no classified plant design)
- KiCad outputs are **scale-model deck / steering actuator stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Flight deck, aviation, combat stubs, propulsion |
| `docs/citations.yaml` | Open / public citations |
| `docs/deck_area_examples.py` | Teaching deck-area / parking check |
| `interfaces/aviation.yaml` | Elevators, fuel, inert ordnance stubs |
| `interfaces/mass-placeholders.yaml` | Combat weapons/sensors mass & footprints |
| `interfaces/control-board.yaml` | KiCad channel map |
| `kicad/ism-carrier-deck.*` | Study KiCad deck control board |
| `shell/deck_study.scad` | Deck + island + elevator/radar mass boxes |

## Roadmap (#45) status
- [x] Design note (flight deck, aviation systems, combat systems, propulsion)
- [x] KiCad boards (scale-model deck control — this PR)
- [ ] Structural design
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
