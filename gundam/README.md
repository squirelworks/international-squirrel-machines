# ISM Gundam — (#46)

**Program ID:** ISM-MS-1 (study name TBD)  
**Status:** design note → KiCad → structural → Gerbers/STL → BOM/assembly in-tree; polish / inquire still open.

## Prior slices
Design-note (actuators / sensors / power / cockpit / stores stubs). KiCad control board. Structural spars / joints / armor. Gerbers + STL. This PR adds educational master BOM + assembly sequence.

## Weapons boundary (hard)

- Stores / hardpoints = **mass, footprint, SAFE/INHIBIT integration stubs** only
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming codes
- **No** live launch / fire sequences or engagement doctrine
- **No** export-controlled (ITAR/EAR) weapon or fire-control designs
- Fab/STL/BOM outputs are **educational frame stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Actuators, sensors, power, cockpit, stores stubs |
| `docs/structural.md` | Torso/limb spars + joint / armor study |
| `docs/fab-mechanical.md` | Gerber + STL notes |
| `docs/bom.md` | Educational master BOM |
| `docs/assembly.md` | Study assembly sequence |
| `docs/citations.yaml` | Open / public citations |
| `docs/balance_examples.py` | Teaching CG / limb-mass balance check |
| `interfaces/suit.yaml` | Machine-readable frame / power / actuator stubs |
| `interfaces/stores-placeholders.yaml` | Hardpoint mass/footprint + SAFE/INHIBIT only |
| `interfaces/control-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-gundam-control.*` | Study KiCad control board |
| `fab/` | Study Gerbers + CPL + BOM stub |
| `shell/frame_study.scad` | Frame + ghost structure |
| `mechanical/frame_study.stl` | Exported study STL |

## Roadmap (#46) status
- [x] Design note (actuators, sensors, power, cockpit, weapons interfaces)
- [x] KiCad control and power boards
- [x] Mechanical / structural design (limbs, armor)
- [x] Gerbers + mechanical files
- [x] BOM / assembly
- [ ] Polish and inquire for release

## Weapons boundary
Stores = **mass / footprint / SAFE / INHIBIT only**. Never seekers, guidance, munition propulsion, warheads, fuzing, or arming in-repo.
