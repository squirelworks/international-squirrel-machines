# ISM Space Station — (#42)

**Program ID:** ISM-SSN-1 (study name TBD)  
**This PR:** structural / mechanical study slice (shells / berthing rings / truss).

## Weapons boundary (hard)

- Habitat / civil station architecture only
- **No** weapons, seekers, guidance-to-target, warheads, fuzing, or combat employment
- Docked spacecraft follow the same rule (mass/power/berthing stubs)
- **No** export-controlled (ITAR/EAR) station or weapon designs
- Structural outputs are **educational layout stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Modules, power, life support, docking, avionics |
| `docs/structural.md` | Habitat/node/lab shells + truss study |
| `docs/citations.yaml` | Open / public citations |
| `docs/eclss_budget_examples.py` | Teaching ECLSS / power budget check |
| `interfaces/station.yaml` | Machine-readable module / power / ECLSS stubs |
| `interfaces/docking-placeholders.yaml` | Berthing mass/volume/power only |
| `interfaces/hab-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-station-hab.*` | Study KiCad habitat board |
| `shell/module_study.scad` | Habitat + truss + ghost structure |

## Roadmap (#42) status
- [x] Design note (modules, power, life support, docking, avionics)
- [x] KiCad boards (power, environmental, computing)
- [x] Structural / mechanical design (this PR)
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
