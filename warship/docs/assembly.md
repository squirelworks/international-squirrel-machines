# Warship — assembly notes (#43)

**Product:** ISM-WS-1  
**Slice:** educational build sequence for the study Gerbers + hull STL package.

## Scope limits (hard)

Same as the design note / Gerbers slice: scale-model control + hull packaging only. Weapons / combat sensors remain **mass / footprint** placeholders — **no** fire control, seekers, guidance, warheads, or fuzing.

## Preconditions

| Artifact | Path |
|----------|------|
| Gerber zip / CPL / fab BOM | `../fab/` |
| Hull study STL | `../mechanical/hull_study.stl` |
| Board project | `../kicad/ism-warship-control.*` |
| Master BOM note | `bom.md` |

## Sequence

1. **Print / obtain hull study article** from `hull_study.stl` (or regenerate via OpenSCAD from `../shell/hull_study.scad`). Confirm ghost keel / frames / decks are present — educational layout only.
2. **Fabricate or order the control board** from `ism-warship-control-gerbers.zip` + CPL + `BOM.csv`. Study pads — not a production RP2040 pitch claim.
3. **Mount board** on tray using H1–H4 / M3 hardware. Keep PWM headers J1–J4 accessible for thruster / rudder / ballast stubs.
4. **Fit inert weapons / combat-sensor mass boxes** per `../interfaces/mass-placeholders.yaml` — mass/footprint only; do not wire fire-control channels (none exist on this board).
5. **Harness PWM stubs** J1 port, J2 stbd, J3 rudder, J4 ballast/trim to scale actuators or bench loads. Power from a current-limited bench supply.
6. **Hydrostatics demo (optional)** run `../docs/hydrostatics_examples.py` teaching checks — not a naval architecture sign-off.
7. **Visual QA** against `structural.md` member list; photograph board orientation and mass-box stations for the lab notebook.

## Lab policy

- Physical: fit, clearance, and inert mass placement only.
- Simulated: any combat employment, fire control, or weapons performance — **out of scope**.
- Never attach live weapons, seekers, or fuzing hardware.

## Next (not this PR)

Polish checklist / inquire-for-release gate; remaining sibling BOM slices (carrier next).
