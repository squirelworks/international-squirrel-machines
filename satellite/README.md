# ISM Satellite — (#31)

**Program ID:** ISM-SAT-1 (study name TBD)  
**This PR:** mechanical structure / panels study slice (rails / trays / hinges).

## Scope / weapons boundary (hard)

- Civilian / educational **bus + payload** architecture only
- Payload mass/power/data stubs — **no** weapons, seekers, guidance-to-target, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) bus or payload designs
- Openly published cubesat / smallsat teaching sources preferred
- Structural outputs are **educational 3U layout stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Bus architecture, power, comms, structure, payload |
| `docs/structural.md` | Rails / panels / trays / hinge study |
| `docs/citations.yaml` | Open / public citations |
| `docs/power_budget_examples.py` | Teaching power-budget check |
| `interfaces/bus.yaml` | Machine-readable bus / power / comms stubs |
| `interfaces/payload-placeholders.yaml` | Payload mass/power/data only |
| `interfaces/bus-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-satellite-bus.*` | Study KiCad bus board |
| `shell/bus_study.scad` | 3U-class structure + ghost members |

## Roadmap (#31) status
- [x] Design note (bus architecture, power, comms, structure, payload)
- [x] KiCad boards (OBC, power, radio)
- [x] Mechanical structure / panels (this PR)
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
