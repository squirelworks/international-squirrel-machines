# ISM Space Station — (#42)

**Program ID:** ISM-SSN-1 (study name TBD)  
**Status:** design note → KiCad → structural → Gerbers/STL → BOM/assembly in-tree; polish / inquire still open.

## Prior slices
Design-note (modules / power / ECLSS / docking / avionics). KiCad habitat board. Structural shells / berthing rings / truss. Gerbers + STL. This PR adds educational master BOM + assembly sequence.

## Weapons boundary (hard)

- Habitat / civil station architecture only
- **No** weapons, seekers, guidance-to-target, warheads, fuzing, or combat employment
- Docked spacecraft follow the same rule (mass/power/berthing stubs)
- **No** export-controlled (ITAR/EAR) station or weapon designs
- Fab/STL/BOM outputs are **educational layout stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Modules, power, life support, docking, avionics |
| `docs/structural.md` | Habitat/node/lab shells + truss study |
| `docs/fab-mechanical.md` | Gerber + STL notes |
| `docs/bom.md` | Educational master BOM |
| `docs/assembly.md` | Study assembly sequence |
| `docs/citations.yaml` | Open / public citations |
| `docs/eclss_budget_examples.py` | Teaching ECLSS / power budget check |
| `interfaces/station.yaml` | Machine-readable module / power / ECLSS stubs |
| `interfaces/docking-placeholders.yaml` | Berthing mass/volume/power only |
| `interfaces/hab-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-station-hab.*` | Study KiCad habitat board |
| `fab/` | Study Gerbers + CPL + BOM stub |
| `shell/module_study.scad` | Habitat + truss + ghost structure |
| `mechanical/module_study.stl` | Exported study STL |

## Roadmap (#42) status
- [x] Design note (modules, power, life support, docking, avionics)
- [x] KiCad boards (power, environmental, computing)
- [x] Structural / mechanical design
- [x] Gerbers + mechanical files
- [x] BOM / assembly
- [ ] Polish and inquire for release

## Weapons boundary
Docking / berthing = **mass / volume / power only**. Never weapons, seekers, guidance-to-target, warheads, or fuzing in-repo.
