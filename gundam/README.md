# ISM Gundam — (#46)

**Program ID:** ISM-MS-1 (study name TBD)  
**This PR:** KiCad mecha control / power board slice.

## Weapons boundary (hard)

- Stores / hardpoints = **mass, footprint, SAFE/INHIBIT integration stubs** only
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming codes
- **No** live launch / fire sequences or engagement doctrine
- **No** export-controlled (ITAR/EAR) weapon or fire-control designs
- Open educational / public mecha-architecture language preferred
- KiCad outputs are **limb actuator + SAFE/INHIBIT stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Actuators, sensors, power, cockpit, stores stubs |
| `docs/citations.yaml` | Open / public citations |
| `docs/balance_examples.py` | Teaching CG / limb-mass balance check |
| `interfaces/suit.yaml` | Machine-readable frame / power / actuator stubs |
| `interfaces/stores-placeholders.yaml` | Hardpoint mass/footprint + SAFE/INHIBIT only |
| `interfaces/control-board.yaml` | KiCad channel map |
| `kicad/ism-gundam-control.*` | Study KiCad control board |
| `shell/frame_study.scad` | Torso + limb packaging study |

## Roadmap (#46) status
- [x] Design note (actuators, sensors, power, cockpit, weapons interfaces)
- [x] KiCad control and power boards (this PR)
- [ ] Mechanical / structural design (limbs, armor)
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
