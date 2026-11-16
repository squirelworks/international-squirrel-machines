# ISM Aircraft Carrier — (#45)

**Program ID:** ISM-CV-1 (study name TBD)  
**This PR:** structural study slice (keel / frames / hangar / elevator trunks).

## Scope limits (hard)

- Weapons and combat sensors = **mass / footprint / KG placeholders** only
- Aviation ordnance = **inert mass boxes** only
- **No** weapons interfaces, fire control, combat-system internals
- **No** seekers, guidance, warheads, fuzing, arming codes, or engagement doctrine
- **No** export-controlled (ITAR/EAR) combat or acoustic data
- Catapult / arresting gear = load/mass/keep-out stubs (no classified plant design)
- Structural outputs are **educational layout stubs** — not certified scantlings

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Flight deck, aviation, combat stubs, propulsion |
| `docs/structural.md` | Keel / frames / hangar / elevator study |
| `docs/citations.yaml` | Open / public citations |
| `docs/deck_area_examples.py` | Teaching deck-area / parking check |
| `interfaces/aviation.yaml` | Elevators, fuel, inert ordnance stubs |
| `interfaces/mass-placeholders.yaml` | Combat weapons/sensors mass & footprints |
| `interfaces/control-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-carrier-deck.*` | Study KiCad deck control board |
| `shell/deck_study.scad` | Deck + island + mass boxes + ghost structure |

## Roadmap (#45) status
- [x] Design note (flight deck, aviation systems, combat systems, propulsion)
- [x] KiCad boards (scale-model deck control)
- [x] Structural design (this PR)
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
