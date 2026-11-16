# ISM Subsonic Bomber — (#38)

**Program ID:** ISM-SB-1 (study name TBD)  
**This PR:** BOM / assembly notes for the study Gerbers + airframe STL package.

## Prior slices
Design-note (airframe / avionics / payload / propulsion). KiCad inert-bay SAFE/INHIBIT board. Structural layout. Gerbers + airframe STL. This PR adds educational master BOM + assembly sequence.

## Weapons boundary (hard)

- Payload / bay = **inert mass, CG, volume, SAFE/INHIBIT stubs** only
- **No** guidance, seekers, munition propulsion, warheads, fuzing, or arming codes
- **No** employment, targeting, or weapons-effectiveness content
- **No** export-controlled (ITAR/EAR) munition or fire-control designs
- Structural bay cutout is an **inert volume keep-out** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Airframe / avionics / payload / propulsion |
| `docs/structural.md` | Primary-structure layout study |
| `docs/fab-mechanical.md` | Gerber + STL notes |
| `docs/bom.md` | Educational master BOM |
| `docs/assembly.md` | Study assembly sequence |
| `docs/citations.yaml` | Open / public citations |
| `docs/cruise_examples.py` | Teaching Breguet / payload-mass check |
| `interfaces/*.yaml` | Airframe / payload / bay / structure |
| `kicad/ism-sb-bay.*` | Study KiCad bay board |
| `fab/` | Study Gerbers + CPL + BOM stub |
| `shell/airframe_study.scad` | OML + ghost structure + bay keep-out |
| `mechanical/airframe_study.stl` | Exported study STL |

## Roadmap (#38) status
- [x] Design note (airframe, avionics, payload, propulsion interface)
- [x] KiCad boards (inert bay SAFE/INHIBIT)
- [x] Structural design
- [x] Gerbers + mechanical files
- [x] BOM / assembly (this PR)
- [ ] Polish and inquire for release
