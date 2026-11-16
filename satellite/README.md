# ISM Satellite — (#31)

**Program ID:** ISM-SAT-1 (study name TBD)  
**This PR:** KiCad bus board slice (OBC / EPS / radio stubs).

## Scope / weapons boundary (hard)

- Civilian / educational **bus + payload** architecture only
- Payload mass/power/data stubs — **no** weapons, seekers, guidance-to-target, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) bus or payload designs
- Openly published cubesat / smallsat teaching sources preferred
- KiCad outputs are **bus OBC / EPS / radio / coarse ADCS stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Bus architecture, power, comms, structure, payload |
| `docs/citations.yaml` | Open / public citations |
| `docs/power_budget_examples.py` | Teaching power-budget check |
| `interfaces/bus.yaml` | Machine-readable bus / power / comms stubs |
| `interfaces/payload-placeholders.yaml` | Payload mass/power/data only |
| `interfaces/bus-board.yaml` | KiCad channel map |
| `kicad/ism-satellite-bus.*` | Study KiCad bus board |
| `shell/bus_study.scad` | 3U-class structure study |

## Roadmap (#31) status
- [x] Design note (bus architecture, power, comms, structure, payload)
- [x] KiCad boards (OBC, power, radio — this PR)
- [ ] Mechanical structure / panels
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
