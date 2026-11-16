# ISM Supersonic Bomber — B1 (#39)

**Program ID:** ISM-XB-1 (study name TBD)  
**This PR scope (B1):** first design note — airframe, avionics, cruise thermal, propulsion interface.

## Weapons boundary (hard limits)

- Inert payload / bay integration only when stores appear later
- **No** guidance, seekers, munition propulsion, warheads, fuzing, or arming
- **No** employment or targeting content

## Hypersonic vs this tree
Sustained **hypersonic** aerothermal / TPS education lives under `hypersonic-bomber/` (#37). This tree is **supersonic cruise** (textbook M~1.5–3 class) with milder thermal notes.

## B1 deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Airframe / avionics / thermal / propulsion interface |
| `shell/airframe_study.scad` | Low-aspect / slender study OML |

## Roadmap (#39) status after B1
- [x] Design note (airframe, avionics, thermal, propulsion) — this PR
- [ ] KiCad boards
- [ ] Structural design
- [ ] Gerbers + mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
