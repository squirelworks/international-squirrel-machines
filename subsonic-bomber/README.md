# ISM Subsonic Bomber — (#38)

**Program ID:** ISM-SB-1 (study name TBD)  
**This PR:** design-note deepen — airframe interfaces, inert bay/payload stubs, teaching cruise check.

## Prior slice
B1 (#137) delivered `docs/design-note.md` + `shell/airframe_study.scad`. This PR adds machine-readable interfaces, citations, and a teaching cruise/payload mass check.

## Weapons boundary (hard)

- Payload / bay = **inert mass, CG, volume, SAFE/INHIBIT stubs** only
- **No** guidance, seekers, munition propulsion, warheads, fuzing, or arming codes
- **No** employment, targeting, or weapons-effectiveness content
- **No** export-controlled (ITAR/EAR) munition or fire-control designs

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Airframe / avionics / payload / propulsion (deepened) |
| `docs/citations.yaml` | Open / public citations |
| `docs/cruise_examples.py` | Teaching Breguet / payload-mass check |
| `interfaces/airframe.yaml` | Study OML / stations stubs |
| `interfaces/payload-placeholders.yaml` | Inert bay mass/volume + SAFE/INHIBIT |
| `shell/airframe_study.scad` | High-aspect OML + bay volume box |

## Roadmap (#38) status
- [x] Design note (airframe, avionics, payload, propulsion interface)
- [ ] KiCad boards
- [ ] Structural design
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
