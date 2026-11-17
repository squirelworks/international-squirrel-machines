# Gundam — assembly notes (#46)

**Product:** ISM-MS-1  
**Slice:** educational build sequence for the study Gerbers + frame STL package.

## Scope / weapons boundary (hard)

Same as the design note / Gerbers slice: mecha frame / actuator packaging only. Stores remain **mass / footprint / SAFE / INHIBIT** stubs — **no** seekers, guidance, munition propulsion, warheads, fuzing, or arming codes.

## Preconditions

| Artifact | Path |
|----------|------|
| Gerber zip / CPL / fab BOM | `../fab/` |
| Frame study STL | `../mechanical/frame_study.stl` |
| Board project | `../kicad/ism-gundam-control.*` |
| Master BOM note | `bom.md` |

## Sequence

1. **Print / obtain frame study article** from `frame_study.stl` (or regenerate via OpenSCAD from `../shell/frame_study.scad`). Confirm torso / limb / inert-stores ghosts.
2. **Fabricate or order the control board** from `ism-gundam-control-gerbers.zip` + CPL + `BOM.csv`. Study pads — not a production RP2040 pitch claim.
3. **Mount board** on tray with H1–H4 / M3 hardware. Keep J1–J4 accessible for leg / arm / SAFE / INHIBIT stubs.
4. **Fit stores placeholder** per `stores-placeholders.yaml` — mass/footprint + SAFE/INHIBIT only; do not install seekers, guidance, or munitions.
5. **Harness** J1 leg PWM, J2 arm PWM, J3 SAFE, J4 INHIBIT. Power from a current-limited bench / EPS stub.
6. **Balance demo (optional)** run `../docs/balance_examples.py` teaching checks — not a combat clearance.
7. **Visual QA** against `structural.md`; photograph board orientation for the lab notebook.

## Lab policy

- Physical: fit, clearance, and stores mass/SAFE/INHIBIT placeholders only.
- Simulated: any live launch, fire sequence, or engagement doctrine — **out of scope**.
- Never attach seekers, warheads, fuzing, or arming hardware.

## Next (not this PR)

Polish checklist / inquire-for-release gate; remaining sibling BOM slices (fighter-jet next / #78 polish gaps).
