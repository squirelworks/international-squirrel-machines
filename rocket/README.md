# ISM Rocket — (#41)

**Program ID:** ISM-RK-1 (study name TBD)  
**This PR:** Gerbers + mechanical STL export slice.

## Prior slices
Hobby airframe design note (B4). KiCad passive logger / recovery board. Structural bulkheads/rings/motor-mount/fin roots. This PR exports study Gerbers and STL.

## Scope limits (hard)

- **Certified commercial hobby motors only** (e.g. NAR / TRA consumer / high-power certified classes — public catalogs)
- **No** guidance, steering, or active flight control
- **No** ballistic-missile or reentry-vehicle content
- **No** export-controlled (ITAR/EAR) data
- Openly published sources only
- Avionics = **passive** logger / altimeter + recovery deployment sensing — not a guidance computer
- Fab/STL outputs are **educational study packages** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Airframe, fins/stability, recovery, passive avionics, motor mount |
| `docs/structural.md` | Bulkheads / rings / motor mount / fin roots |
| `docs/fab-mechanical.md` | Gerber + STL notes |
| `docs/citations.yaml` | Open / public citations |
| `docs/stability_examples.py` | Static-margin teaching check |
| `interfaces/airframe.yaml` | Study dimensions / CP–CG stubs |
| `interfaces/avionics-passive.yaml` | Logger / recovery channels — no guidance |
| `interfaces/logger-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-rocket-logger.*` | Study KiCad logger / recovery board |
| `fab/` | Study Gerbers + CPL + BOM stub |
| `shell/airframe_study.scad` | Body + fins + ghost structure |
| `mechanical/airframe_study.stl` | Exported study STL |

## Roadmap (#41) status
- [x] Design note (airframe, fins and stability margin, recovery, passive avionics, motor mount for certified motors)
- [x] KiCad boards (passive logger / altimeter, recovery deployment, power)
- [x] Structural / mechanical design
- [x] Gerbers + mechanical files (this PR)
- [ ] BOM / assembly
- [ ] Polish and inquire for release

## Guidance boundary
**Never** guidance, steering, or active flight control in-repo. Logger + recovery sensing only.
