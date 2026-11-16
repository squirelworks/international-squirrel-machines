# ISM Space Station — (#42)

**Program ID:** ISM-SSN-1 (study name TBD)  
**This PR:** design-note slice — modules, power, life support, docking, avionics.

## Weapons boundary (hard)

- Habitat / civil station architecture only
- **No** weapons, seekers, guidance-to-target, warheads, fuzing, or combat employment
- Docked spacecraft follow the same rule (mass/power/berthing stubs)
- **No** export-controlled (ITAR/EAR) station or weapon designs
- Open educational / public ISS-class architecture language preferred

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Modules, power, life support, docking, avionics |
| `docs/citations.yaml` | Open / public citations |
| `docs/eclss_budget_examples.py` | Teaching ECLSS / power budget check |
| `interfaces/station.yaml` | Machine-readable module / power / ECLSS stubs |
| `interfaces/docking-placeholders.yaml` | Berthing mass/volume/power only |
| `shell/module_study.scad` | Habitat + truss study OML |

## Roadmap (#42) status
- [x] Design note (modules, power, life support, docking, avionics)
- [ ] KiCad boards (power, environmental, computing)
- [ ] Structural / mechanical design
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
