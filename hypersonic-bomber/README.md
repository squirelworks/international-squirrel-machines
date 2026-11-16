# ISM Hypersonic Bomber — (#37)

**Program ID:** ISM-HB-1 (study name TBD)  
**This PR:** KiCad educational thermal / TPS sense board slice.

## Prior slices
B1 (#137) delivered aerothermal/TPS notes and blunt-cone study OML. Deepen added interfaces and teaching heat-flux. This PR adds the study KiCad thermal board.

## Out of scope (hard limits)

- Weapons, munitions, guidance, seekers, warheads, fuzing, or arming
- Operational employment, targeting, or mission planning
- Scramjet / propulsion **design recipes** or performance prediction
- Export-controlled (ITAR/EAR) TPS formulations, classified materials data
- KiCad channels are **teaching thermal / TPS status stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Deepen summary (aerothermal + TPS classes) |
| `docs/aerothermal-concepts.md` | Textbook heat-transfer concepts (B1) |
| `docs/heat-shield-tps.md` | TPS class trades (B1) |
| `docs/citations.yaml` | Open / public citations |
| `docs/stagnation_examples.py` | Stagnation-temperature teaching check |
| `docs/heat_flux_examples.py` | Teaching cold-wall heat-flux stub |
| `interfaces/aerothermal.yaml` | Mach / T∞ / bluntness stubs |
| `interfaces/tps-placeholders.yaml` | TPS **class** placeholders only |
| `interfaces/thermal-board.yaml` | KiCad channel map |
| `kicad/ism-hb-thermal.*` | Study KiCad thermal board |
| `shell/blunt_cone_study.scad` | Blunt sphere-cone + outer TPS shell sketch |

## Roadmap (#37) status
- [x] Design note — aerothermal / heat-shield (B1 + deepen)
- [x] KiCad boards (educational thermal / TPS sense — this PR)
- [ ] Structural / mechanical design (beyond study OML)
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release

## Weapons boundary
**Never** guidance, seekers, munition propulsion, warheads, or fuzing in-repo.
