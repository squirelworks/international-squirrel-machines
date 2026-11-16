# ISM Supersonic Bomber — (#39)

**Program ID:** ISM-XB-1 (study name TBD)  
**This PR:** structural study slice (spars / ribs / frames / gear attach).

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
| `docs/design-note.md` | Airframe / avionics / thermal / propulsion (deepened) |
| `docs/structural.md` | Primary-structure layout study |
| `docs/citations.yaml` | Open / public citations |
| `docs/thermal_examples.py` | Teaching recovery-temperature stub |
| `interfaces/airframe.yaml` | Study OML / stations stubs |
| `interfaces/payload-placeholders.yaml` | Inert bay mass/volume + SAFE/INHIBIT |
| `interfaces/bay-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Spar / rib / frame / gear map |
| `kicad/ism-xb-bay.*` | Study KiCad bay board |
| `shell/airframe_study.scad` | Slender OML + ghost structure + bay keep-out |

## Roadmap (#39) status
- [x] Design note (airframe, avionics, thermal, propulsion)
- [x] KiCad boards (inert bay SAFE/INHIBIT)
- [x] Structural design (this PR)
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
