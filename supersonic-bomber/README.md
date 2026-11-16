# ISM Supersonic Bomber — (#39)

**Program ID:** ISM-XB-1 (study name TBD)  
**This PR:** design-note deepen — airframe interfaces, cruise thermal stubs, inert bay/payload.

## Prior slice
B1 (#137) delivered `docs/design-note.md` + `shell/airframe_study.scad`. This PR adds machine-readable interfaces, citations, and a teaching cruise-thermal check.

## Hypersonic vs this tree
Sustained **hypersonic** aerothermal / TPS education lives under `hypersonic-bomber/` (#37). This tree is **supersonic cruise** (textbook M≈1.5–3) with milder thermal notes.

## Weapons boundary (hard)

- Payload / bay = **inert mass, CG, volume, SAFE/INHIBIT stubs** only
- **No** guidance, seekers, munition propulsion, warheads, fuzing, or arming
- **No** employment or targeting content
- **No** export-controlled (ITAR/EAR) munition or fire-control designs

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Airframe / avionics / thermal / propulsion (deepened) |
| `docs/citations.yaml` | Open / public citations |
| `docs/thermal_examples.py` | Teaching recovery-temperature stub |
| `interfaces/airframe.yaml` | Study OML / stations stubs |
| `interfaces/payload-placeholders.yaml` | Inert bay mass/volume + SAFE/INHIBIT |
| `shell/airframe_study.scad` | Slender OML + bay volume box |

## Roadmap (#39) status
- [x] Design note (airframe, avionics, thermal, propulsion)
- [ ] KiCad boards
- [ ] Structural design
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
