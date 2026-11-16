# ISM Gundam — (#46)

**Program ID:** ISM-MS-1 (study name TBD)  
**This PR:** mechanical / structural study slice (limbs / armor / frame).

## Weapons boundary (hard)

- Stores / hardpoints = **mass, footprint, SAFE/INHIBIT integration stubs** only
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming codes
- **No** live launch / fire sequences or engagement doctrine
- **No** export-controlled (ITAR/EAR) weapon or fire-control designs
- Structural outputs are **educational frame stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Actuators, sensors, power, cockpit, stores stubs |
| `docs/structural.md` | Torso/limb spars + joint / armor study |
| `docs/citations.yaml` | Open / public citations |
| `docs/balance_examples.py` | Teaching CG / limb-mass balance check |
| `interfaces/suit.yaml` | Machine-readable frame / power / actuator stubs |
| `interfaces/stores-placeholders.yaml` | Hardpoint mass/footprint + SAFE/INHIBIT only |
| `interfaces/control-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-gundam-control.*` | Study KiCad control board |
| `shell/frame_study.scad` | Frame + ghost structure |

## Roadmap (#46) status
- [x] Design note (actuators, sensors, power, cockpit, weapons interfaces)
- [x] KiCad control and power boards
- [x] Mechanical / structural design (limbs, armor — this PR)
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
