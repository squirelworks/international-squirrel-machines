# Submarine — assembly notes (#44)

**Product:** ISM-SS-1  
**Slice:** educational build sequence for the study Gerbers + hull STL package.

## Scope limits (hard)

Same B3 boundary as the design note / Gerbers slice: scale-model control + hull packaging only. **No** quieting, acoustics, life-support product design, or weapons.

## Preconditions

| Artifact | Path |
|----------|------|
| Gerber zip / CPL / fab BOM | `../fab/` |
| Hull study STL | `../mechanical/hull_study.stl` |
| Board project | `../kicad/ism-submarine-control.*` |
| Master BOM note | `bom.md` |

## Sequence

1. **Print / obtain hull study article** from `hull_study.stl` (or regenerate via OpenSCAD from `../shell/hull_study.scad`). Confirm ghost rings / casing / sail are present — educational layout only.
2. **Fabricate or order the control board** from `ism-submarine-control-gerbers.zip` + `ism-submarine-control-cpl.csv` + `BOM.csv`. Study pads — not a production RP2040 pitch claim.
3. **Mount board** on tray using H1–H4 / M3 hardware. Keep PWM headers J1–J4 accessible aft toward actuator stubs.
4. **Fit inert sensor mass boxes** (bow / flank) per `../interfaces/mass-placeholders.yaml` — mass/footprint only; do not wire acoustic channels (none exist on this board).
5. **Harness PWM stubs** J1 propulsor, J2 stern-plane, J3 rudder, J4 ballast/trim to scale actuators or bench loads. Power from a current-limited bench supply.
6. **Trim demo (optional)** run `../docs/trim_examples.py` teaching checks — not a naval architecture sign-off.
7. **Visual QA** against `structural.md` member list; photograph board orientation and mass-box stations for the lab notebook.

## Lab policy

- Physical: fit, clearance, and inert mass placement only.
- Simulated: any depth, collapse, or acoustic behaviour — **out of scope**.
- Never attach weapons, quieting coatings as a design product, or live acoustic arrays.

## Next

Polish checklist / inquire-for-release gate (open).
