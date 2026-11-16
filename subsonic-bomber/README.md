# ISM Subsonic Bomber — (#38)

**Program ID:** ISM-SB-1 (study name TBD)  
**This PR:** KiCad inert bay SAFE/INHIBIT board slice.

## Weapons boundary (hard)

- Payload / bay = **inert mass, CG, volume, SAFE/INHIBIT stubs** only
- **No** guidance, seekers, munition propulsion, warheads, fuzing, or arming codes
- **No** employment, targeting, or weapons-effectiveness content
- **No** export-controlled (ITAR/EAR) munition or fire-control designs
- KiCad outputs are **bay door + SAFE/INHIBIT / WOW stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Airframe / avionics / payload / propulsion (deepened) |
| `docs/citations.yaml` | Open / public citations |
| `docs/cruise_examples.py` | Teaching Breguet / payload-mass check |
| `interfaces/airframe.yaml` | Study OML / stations stubs |
| `interfaces/payload-placeholders.yaml` | Inert bay mass/volume + SAFE/INHIBIT |
| `interfaces/bay-board.yaml` | KiCad channel map |
| `kicad/ism-sb-bay.*` | Study KiCad bay board |
| `shell/airframe_study.scad` | High-aspect OML + bay volume box |

## Roadmap (#38) status
- [x] Design note (airframe, avionics, payload, propulsion interface)
- [x] KiCad boards (inert bay SAFE/INHIBIT — this PR)
- [ ] Structural design
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
