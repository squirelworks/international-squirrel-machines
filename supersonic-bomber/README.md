# ISM Supersonic Bomber — (#39)

**Program ID:** ISM-XB-1 (study name TBD)  
**This PR:** BOM / assembly notes for the study Gerbers + airframe STL package.

## Prior slices
Design-note (airframe / avionics / thermal / propulsion). KiCad inert-bay SAFE/INHIBIT board. Structural layout. Gerbers + airframe STL. This PR adds educational master BOM + assembly sequence.

## Hypersonic vs this tree
Sustained **hypersonic** aerothermal / TPS education lives under `hypersonic-bomber/` (#37). This tree is **supersonic cruise** (textbook M≈1.5–3) with milder thermal notes.

## Weapons boundary (hard)

- Payload / bay = **inert mass, CG, volume, SAFE/INHIBIT stubs** only
- **No** guidance, seekers, munition propulsion, warheads, fuzing, or arming
- **No** employment or targeting content
- **No** export-controlled (ITAR/EAR) munition or fire-control designs
- Structural bay cutout is an **inert volume keep-out** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Airframe / avionics / thermal / propulsion |
| `docs/structural.md` | Primary-structure layout study |
| `docs/fab-mechanical.md` | Gerber + STL notes |
| `docs/bom.md` | Educational master BOM |
| `docs/assembly.md` | Study assembly sequence |
| `docs/citations.yaml` | Open / public citations |
| `docs/thermal_examples.py` | Teaching recovery-temperature stub |
| `interfaces/*.yaml` | Airframe / payload / bay / structure |
| `kicad/ism-xb-bay.*` | Study KiCad bay board |
| `fab/` | Study Gerbers + CPL + BOM stub |
| `shell/airframe_study.scad` | Slender OML + ghost structure + bay keep-out |
| `mechanical/airframe_study.stl` | Exported study STL |

## Roadmap (#39) status
- [x] Design note (airframe, avionics, thermal, propulsion)
- [x] KiCad boards (inert bay SAFE/INHIBIT)
- [x] Structural design
- [x] Gerbers + mechanical files
- [x] BOM / assembly (this PR)
- [ ] Polish and inquire for release
