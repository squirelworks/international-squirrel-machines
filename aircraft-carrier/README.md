# ISM Aircraft Carrier — (#45)

**Program ID:** ISM-CV-1 (study name TBD)  
**This PR:** design-note deepen — flight deck, aviation, combat (placeholders), propulsion.

## Prior slice
B2 (#139 with warship #43) delivered a light flight-deck note + `shell/deck_study.scad`. This PR completes the **#45 design-note** checkbox with machine-readable placeholders and a teaching deck-area check.

## Scope limits (hard)

- Weapons and combat sensors = **mass / footprint / KG placeholders** only
- Aviation ordnance = **inert mass boxes** only
- **No** weapons interfaces, fire control, combat-system internals
- **No** seekers, guidance, warheads, fuzing, arming codes, or engagement doctrine
- **No** export-controlled (ITAR/EAR) combat or acoustic data
- Catapult / arresting gear = load/mass/keep-out stubs (no classified plant design)

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Flight deck, aviation, combat stubs, propulsion |
| `docs/citations.yaml` | Open / public citations |
| `docs/deck_area_examples.py` | Teaching deck-area / parking check |
| `interfaces/aviation.yaml` | Elevators, fuel, inert ordnance stubs |
| `interfaces/mass-placeholders.yaml` | Combat weapons/sensors mass & footprints |
| `shell/deck_study.scad` | Deck + island + elevator/radar mass boxes |

## Roadmap (#45) status
- [x] Design note (flight deck, aviation systems, combat systems, propulsion)
- [ ] KiCad boards
- [ ] Structural design
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
