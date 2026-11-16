# ISM Rocket — (#41)

**Program ID:** ISM-RK-1 (study name TBD)  
**This PR:** KiCad passive logger / recovery board slice.

## Scope limits (hard)

- **Certified commercial hobby motors only** (e.g. NAR / TRA consumer / high-power certified classes — public catalogs)
- **No** guidance, steering, or active flight control
- **No** ballistic-missile or reentry-vehicle content
- **No** export-controlled (ITAR/EAR) data
- Openly published sources only
- Avionics = **passive** logger / altimeter + recovery deployment sensing — not a guidance computer
- KiCad outputs are **logger / recovery-channel stubs** only (no guidance computer)

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Airframe, fins/stability, recovery, passive avionics, motor mount |
| `docs/citations.yaml` | Open / public citations |
| `docs/stability_examples.py` | Static-margin teaching check |
| `interfaces/airframe.yaml` | Study dimensions / CP–CG stubs |
| `interfaces/avionics-passive.yaml` | Logger / recovery channels — no guidance |
| `interfaces/logger-board.yaml` | KiCad channel map |
| `kicad/ism-rocket-logger.*` | Study KiCad logger / recovery board |
| `shell/airframe_study.scad` | Body + fin study OML |

## Roadmap (#41) status
- [x] Design note (airframe, fins and stability margin, recovery, passive avionics, motor mount for certified motors)
- [x] KiCad boards (passive logger / altimeter, recovery deployment, power — this PR)
- [ ] Structural / mechanical design
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
