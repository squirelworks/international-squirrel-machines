# ISM Aircraft Carrier — (#45)

**Program ID:** ISM-CV-1 (study name TBD)  
**This PR:** Gerbers + mechanical STL export slice.

## Prior slices
Flight-deck design note deepen. KiCad scale-model deck control. Structural keel/frames/hangar. This PR exports study Gerbers and STL.

## Scope limits (hard)

- Weapons and combat sensors = **mass / footprint / KG placeholders** only
- Aviation ordnance = **inert mass boxes** only
- **No** weapons interfaces, fire control, combat-system internals
- **No** seekers, guidance, warheads, fuzing, arming codes, or engagement doctrine
- **No** export-controlled (ITAR/EAR) combat or acoustic data
- Catapult / arresting gear = load/mass/keep-out stubs (no classified plant design)
- Fab/STL outputs are **educational study packages** — not certified

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Flight deck, aviation, combat stubs, propulsion |
| `docs/structural.md` | Keel / frames / hangar / elevator study |
| `docs/fab-mechanical.md` | Gerber + STL notes |
| `docs/citations.yaml` | Open / public citations |
| `docs/deck_area_examples.py` | Teaching deck-area / parking check |
| `interfaces/aviation.yaml` | Elevators, fuel, inert ordnance stubs |
| `interfaces/mass-placeholders.yaml` | Combat weapons/sensors mass & footprints |
| `interfaces/control-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-carrier-deck.*` | Study KiCad deck control board |
| `fab/` | Study Gerbers + CPL + BOM stub |
| `shell/deck_study.scad` | Deck + island + mass boxes + ghost structure |
| `mechanical/deck_study.stl` | Exported study STL |

## Roadmap (#45) status
- [x] Design note (flight deck, aviation systems, combat systems, propulsion)
- [x] KiCad boards (scale-model deck control)
- [x] Structural design
- [x] Gerbers + mechanical files (this PR)
- [ ] BOM / assembly
- [ ] Polish and inquire for release

## Weapons boundary
Weapons / combat sensors / aviation ordnance = **mass / footprint only**. Never fire control, seekers, guidance, warheads, or fuzing in-repo.
