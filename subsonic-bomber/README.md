# ISM Subsonic Bomber — (#38)

**Program ID:** ISM-SB-1 (study name TBD)  
**This PR:** structural study slice (spars / ribs / frames / gear attach).

## Weapons boundary (hard)

- Payload / bay = **inert mass, CG, volume, SAFE/INHIBIT stubs** only
- **No** guidance, seekers, munition propulsion, warheads, fuzing, or arming codes
- **No** employment, targeting, or weapons-effectiveness content
- **No** export-controlled (ITAR/EAR) munition or fire-control designs
- Structural bay cutout is an **inert volume keep-out** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Airframe / avionics / payload / propulsion (deepened) |
| `docs/structural.md` | Primary-structure layout study |
| `docs/citations.yaml` | Open / public citations |
| `docs/cruise_examples.py` | Teaching Breguet / payload-mass check |
| `interfaces/airframe.yaml` | Study OML / stations stubs |
| `interfaces/payload-placeholders.yaml` | Inert bay mass/volume + SAFE/INHIBIT |
| `interfaces/bay-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Spar / rib / frame / gear map |
| `kicad/ism-sb-bay.*` | Study KiCad bay board |
| `shell/airframe_study.scad` | OML + ghost structure + bay keep-out |

## Roadmap (#38) status
- [x] Design note (airframe, avionics, payload, propulsion interface)
- [x] KiCad boards (inert bay SAFE/INHIBIT)
- [x] Structural design (this PR)
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
