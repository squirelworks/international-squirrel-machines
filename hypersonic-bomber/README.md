# ISM Hypersonic Bomber — B1 (#37)

**Program ID:** ISM-HB-1 (study name TBD)  
**This PR scope (B1):** educational **aerothermal** and **heat-shield / TPS** design notes only.

## Out of scope (hard limits)

This tree does **not** cover:

- Weapons, munitions, guidance, seekers, warheads, fuzing, or arming
- Operational employment, targeting, or mission planning
- Scramjet / propulsion **design recipes** or performance prediction for a real vehicle
- Export-controlled (ITAR/EAR) TPS formulations, classified materials data, or “derived from leaks” sources
- Full airframe / avionics / KiCad productization (later roadmap steps)

## B1 deliverables

| Path | Role |
|------|------|
| `docs/aerothermal-concepts.md` | Textbook hypersonic heat-transfer concepts |
| `docs/heat-shield-tps.md` | Heat-shield / TPS **class** trades (educational) |
| `docs/citations.yaml` | Open / public citations |
| `docs/stagnation_examples.py` | Canonical stagnation-temperature teaching check |
| `shell/blunt_cone_study.scad` | Blunt sphere-cone study OML (heat-shield geometry teaching) |

## Roadmap (#37) status after B1
- [x] Design note — **aerothermal / heat-shield slice only** (this PR)
- [ ] KiCad boards
- [ ] Structural / mechanical design (beyond study OML)
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release

## Weapons boundary
Same military-lane rule as the fighter program: integration / ICD later if needed — **never** guidance, seekers, munition propulsion, warheads, or fuzing in-repo.
