# ISM Satellite — B5 (#31)

**Program ID:** ISM-SAT-1 (study name TBD)  
**Plan:** B5 — bus + payload design-note slice.

## Scope / weapons boundary (hard)

- Civilian / educational **bus + payload** architecture only
- Payload mass/power/data stubs — **no** weapons, seekers, guidance-to-target, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) bus or payload designs
- Openly published cubesat / smallsat teaching sources preferred

## B5 deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Bus architecture, power, comms, structure, payload |
| `docs/citations.yaml` | Open / public citations |
| `docs/power_budget_examples.py` | Teaching power-budget check |
| `interfaces/bus.yaml` | Machine-readable bus / power / comms stubs |
| `interfaces/payload-placeholders.yaml` | Payload mass/power/data only |
| `shell/bus_study.scad` | 3U-class structure study |

## Roadmap (#31) status after B5
- [x] Design note (bus architecture, power, comms, structure, payload)
- [ ] KiCad boards (OBC, power, radio)
- [ ] Mechanical structure / panels
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
