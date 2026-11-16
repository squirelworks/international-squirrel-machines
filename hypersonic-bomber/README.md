# ISM Hypersonic Bomber — (#37)

**Program ID:** ISM-HB-1 (study name TBD)  
**This PR:** structural / mechanical study slice (frames / rails under TPS shell).

## Prior slices
B1 (#137) aerothermal/TPS notes + blunt-cone OML. Deepen added interfaces/heat-flux. KiCad thermal board landed. This PR adds educational primary-structure ghosts under the TPS packaging shell.

## Out of scope (hard limits)

- Weapons, munitions, guidance, seekers, warheads, fuzing, or arming
- Operational employment, targeting, or mission planning
- Scramjet / propulsion **design recipes** or performance prediction
- Export-controlled (ITAR/EAR) TPS formulations, classified materials data
- Structural outputs are **educational layout stubs** — not certified

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Deepen summary (aerothermal + TPS classes) |
| `docs/structural.md` | Primary-structure layout under TPS shell |
| `docs/aerothermal-concepts.md` | Textbook heat-transfer concepts (B1) |
| `docs/heat-shield-tps.md` | TPS class trades (B1) |
| `docs/citations.yaml` | Open / public citations |
| `docs/stagnation_examples.py` | Stagnation-temperature teaching check |
| `docs/heat_flux_examples.py` | Teaching cold-wall heat-flux stub |
| `interfaces/aerothermal.yaml` | Mach / T∞ / bluntness stubs |
| `interfaces/tps-placeholders.yaml` | TPS **class** placeholders only |
| `interfaces/thermal-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Frame / rail / bulkhead map |
| `kicad/ism-hb-thermal.*` | Study KiCad thermal board |
| `shell/blunt_cone_study.scad` | Blunt cone + TPS shell + ghost structure |

## Roadmap (#37) status
- [x] Design note — aerothermal / heat-shield (B1 + deepen)
- [x] KiCad boards (educational thermal / TPS sense)
- [x] Structural / mechanical design (this PR)
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release

## Weapons boundary
**Never** guidance, seekers, munition propulsion, warheads, or fuzing in-repo.
