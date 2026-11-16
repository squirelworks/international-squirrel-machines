# ISM Rocket — B4 (#41)

**Program ID:** ISM-RK-1 (study name TBD)  
**Plan:** Fred research plan B4 — hobby / educational-class rocket.

## Scope limits (hard)

- **Certified commercial hobby motors only** (e.g. NAR / TRA consumer / high-power certified classes — public catalogs)
- **No** guidance, steering, or active flight control
- **No** ballistic-missile or reentry-vehicle content
- **No** export-controlled (ITAR/EAR) data
- Openly published sources only
- Avionics = **passive** logger / altimeter + recovery deployment sensing — not a guidance computer

## B4 deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Airframe, fins/stability, recovery, passive avionics, motor mount |
| `docs/citations.yaml` | Open / public citations |
| `docs/stability_examples.py` | Static-margin teaching check |
| `interfaces/airframe.yaml` | Study dimensions / CP–CG stubs |
| `interfaces/avionics-passive.yaml` | Logger / recovery channels — no guidance |
| `shell/airframe_study.scad` | Body + fin study OML |

## Roadmap (#41) status after B4
- [x] Design note (airframe, fins and stability margin, recovery, passive avionics, motor mount for certified motors)
- [ ] KiCad boards (passive logger / altimeter, recovery deployment, power)
- [ ] Structural / mechanical design
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
