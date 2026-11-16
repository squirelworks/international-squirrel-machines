# ISM Hypersonic Bomber — (#37)

**Program ID:** ISM-HB-1 (study name TBD)  
**This PR:** Gerbers + mechanical STL export slice.

## Prior slices
B1 aerothermal/TPS notes + blunt-cone OML. Deepen added interfaces/heat-flux. KiCad thermal board + structural ghosts under TPS shell landed. This PR exports study Gerbers and STL.

## Out of scope (hard limits)

- Weapons, munitions, guidance, seekers, warheads, fuzing, or arming
- Operational employment, targeting, or mission planning
- Scramjet / propulsion **design recipes** or performance prediction
- Export-controlled (ITAR/EAR) TPS formulations, classified materials data
- Fab/STL outputs are **educational study packages** — not certified

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Deepen summary (aerothermal + TPS classes) |
| `docs/structural.md` | Primary-structure layout under TPS shell |
| `docs/fab-mechanical.md` | Gerber + STL notes |
| `docs/aerothermal-concepts.md` | Textbook heat-transfer concepts (B1) |
| `docs/heat-shield-tps.md` | TPS class trades (B1) |
| `docs/citations.yaml` | Open / public citations |
| `docs/stagnation_examples.py` | Stagnation-temperature teaching check |
| `docs/heat_flux_examples.py` | Teaching cold-wall heat-flux stub |
| `interfaces/*.yaml` | Aerothermal / TPS / board / structure |
| `kicad/ism-hb-thermal.*` | Study KiCad thermal board |
| `fab/` | Study Gerbers + CPL + BOM stub |
| `shell/blunt_cone_study.scad` | Blunt cone + TPS shell + ghost structure |
| `mechanical/blunt_cone_study.stl` | Exported study STL |

## Roadmap (#37) status
- [x] Design note — aerothermal / heat-shield (B1 + deepen)
- [x] KiCad boards (educational thermal / TPS sense)
- [x] Structural / mechanical design
- [x] Gerbers + mechanical files (this PR)
- [ ] BOM / assembly
- [ ] Polish and inquire for release

## Weapons boundary
**Never** guidance, seekers, munition propulsion, warheads, or fuzing in-repo.
