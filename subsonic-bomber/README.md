# ISM Subsonic Bomber — (#38)

**Program ID:** ISM-SB-1 (study name TBD)  
**This PR:** Gerbers + mechanical STL export slice.

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
- [x] Gerbers + mechanical files (this PR)
- [ ] BOM / assembly
- [ ] Polish and inquire for release
