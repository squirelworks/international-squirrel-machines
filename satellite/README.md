# ISM Satellite — (#31)

**Program ID:** ISM-SAT-1 (study name TBD)  
**This PR:** Gerbers + mechanical STL export slice.

## Prior slices
Bus design-note (B5). KiCad OBC/power/radio bus board. Structural 3U rails/trays. This PR exports study Gerbers and STL.

## Scope / weapons boundary (hard)

- Civilian / educational **bus + payload** architecture only
- Payload mass/power/data stubs — **no** weapons, seekers, guidance-to-target, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) bus or payload designs
- Openly published cubesat / smallsat teaching sources preferred
- Fab/STL outputs are **educational 3U study packages** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Bus architecture, power, comms, structure, payload |
| `docs/structural.md` | Rails / panels / trays / hinge study |
| `docs/fab-mechanical.md` | Gerber + STL notes |
| `docs/citations.yaml` | Open / public citations |
| `docs/power_budget_examples.py` | Teaching power-budget check |
| `interfaces/bus.yaml` | Machine-readable bus / power / comms stubs |
| `interfaces/payload-placeholders.yaml` | Payload mass/power/data only |
| `interfaces/bus-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-satellite-bus.*` | Study KiCad bus board |
| `fab/` | Study Gerbers + CPL + BOM stub |
| `shell/bus_study.scad` | 3U-class structure + ghost members |
| `mechanical/bus_study.stl` | Exported study STL |

## Roadmap (#31) status
- [x] Design note (bus architecture, power, comms, structure, payload)
- [x] KiCad boards (OBC, power, radio)
- [x] Mechanical structure / panels
- [x] Gerbers + mechanical files (this PR)
- [ ] BOM / assembly
- [ ] Polish and inquire for release

## Weapons boundary
Payload = **mass / power / data only**. Never weapons, seekers, guidance-to-target, warheads, or fuzing in-repo.
