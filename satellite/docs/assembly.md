# Satellite — assembly notes (#31)

**Product:** ISM-SAT-1  
**Slice:** educational build sequence for the study Gerbers + bus STL package.

## Scope / weapons boundary (hard)

Same as the design note / Gerbers slice: civilian / educational bus + payload packaging only. Payload remains **mass / power / data** stubs — **no** weapons, seekers, guidance-to-target, warheads, or fuzing.

## Preconditions

| Artifact | Path |
|----------|------|
| Gerber zip / CPL / fab BOM | `../fab/` |
| Bus study STL | `../mechanical/bus_study.stl` |
| Board project | `../kicad/ism-satellite-bus.*` |
| Master BOM note | `bom.md` |

## Sequence

1. **Print / obtain bus study article** from `bus_study.stl` (or regenerate via OpenSCAD from `../shell/bus_study.scad`). Confirm 3U rails / trays ghosts.
2. **Fabricate or order the bus board** from `ism-satellite-bus-gerbers.zip` + CPL + `BOM.csv`. Study pads — not a production RP2040 pitch claim.
3. **Mount board** on tray with H1–H4 / M3 hardware. Keep J1–J4 accessible for EPS / radio / MTQ / payload-enable stubs.
4. **Fit payload placeholder** per `payload-placeholders.yaml` — mass/power/data only; do not install weapons payloads.
5. **Harness** J1 EPS, J2 radio, J3 magnetorquer, J4 payload enable. Power from a current-limited bench / EPS stub.
6. **Power-budget demo (optional)** run `../docs/power_budget_examples.py` teaching checks — not a flight clearance.
7. **Visual QA** against `structural.md`; photograph board orientation for the lab notebook.

## Lab policy

- Physical: fit, clearance, and payload mass/power/data placeholders only.
- Simulated: any weapons employment or guidance-to-target — **out of scope**.
- Never attach seekers, warheads, or fuzing hardware.

## Next (not this PR)

Polish checklist / inquire-for-release gate; remaining sibling BOM slices (space-station next).
