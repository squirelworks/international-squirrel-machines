# ISM Supersonic Bomber — (#39)

**Program ID:** ISM-XB-1 (study name TBD)  
**This PR:** KiCad inert bay SAFE/INHIBIT board slice.

## Hypersonic vs this tree
Sustained **hypersonic** aerothermal / TPS education lives under `hypersonic-bomber/` (#37). This tree is **supersonic cruise** (textbook M≈1.5–3) with milder thermal notes.

## Weapons boundary (hard)

- Payload / bay = **inert mass, CG, volume, SAFE/INHIBIT stubs** only
- **No** guidance, seekers, munition propulsion, warheads, fuzing, or arming
- **No** employment or targeting content
- **No** export-controlled (ITAR/EAR) munition or fire-control designs
- KiCad outputs are **bay door + SAFE/INHIBIT / WOW stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Airframe / avionics / thermal / propulsion (deepened) |
| `docs/citations.yaml` | Open / public citations |
| `docs/thermal_examples.py` | Teaching recovery-temperature stub |
| `interfaces/airframe.yaml` | Study OML / stations stubs |
| `interfaces/payload-placeholders.yaml` | Inert bay mass/volume + SAFE/INHIBIT |
| `interfaces/bay-board.yaml` | KiCad channel map |
| `kicad/ism-xb-bay.*` | Study KiCad bay board |
| `shell/airframe_study.scad` | Slender OML + bay volume box |

## Roadmap (#39) status
- [x] Design note (airframe, avionics, thermal, propulsion)
- [x] KiCad boards (inert bay SAFE/INHIBIT — this PR)
- [ ] Structural design
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
