# ISM Rocket — (#41)

**Program ID:** ISM-RK-1 (study name TBD)  
**This PR:** structural / mechanical study slice (bulkheads / rings / motor mount / fin roots).

## Scope limits (hard)

- **Certified commercial hobby motors only** (e.g. NAR / TRA consumer / high-power certified classes — public catalogs)
- **No** guidance, steering, or active flight control
- **No** ballistic-missile or reentry-vehicle content
- **No** export-controlled (ITAR/EAR) data
- Openly published sources only
- Avionics = **passive** logger / altimeter + recovery deployment sensing — not a guidance computer
- Structural outputs are **educational layout stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Airframe, fins/stability, recovery, passive avionics, motor mount |
| `docs/structural.md` | Bulkheads / rings / motor mount / fin roots |
| `docs/citations.yaml` | Open / public citations |
| `docs/stability_examples.py` | Static-margin teaching check |
| `interfaces/airframe.yaml` | Study dimensions / CP–CG stubs |
| `interfaces/avionics-passive.yaml` | Logger / recovery channels — no guidance |
| `interfaces/logger-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-rocket-logger.*` | Study KiCad logger / recovery board |
| `shell/airframe_study.scad` | Body + fins + ghost structure |

## Roadmap (#41) status
- [x] Design note (airframe, fins and stability margin, recovery, passive avionics, motor mount for certified motors)
- [x] KiCad boards (passive logger / altimeter, recovery deployment, power)
- [x] Structural / mechanical design (this PR)
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
