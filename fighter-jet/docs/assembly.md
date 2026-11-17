# Fighter Jet — bay/study assembly notes (#85)

**Product:** ISM-FJ-1 “Nutcracker”  
**Slice:** educational build sequence for the study Gerbers + airframe STL package. Program prototype path remains `assembly-notes.md` (#78).

## Scope / weapons boundary (hard)

Same as the Gerbers slice: bay board = surface / throttle PWM stubs only. Stores remain **mass / footprint / SAFE / INHIBIT** stubs — **no** seekers, guidance, munition propulsion, warheads, fuzing, or arming codes.

## Preconditions

| Artifact | Path |
|----------|------|
| Gerber zip / CPL / fab BOM | `../fab/` |
| Study airframe STL | `../shell/airframe.stl` |
| Board project | `../kicad/` |
| Master study BOM note | `bom.md` |
| Program assembly path | `assembly-notes.md` |

## Sequence

1. **Print / obtain study airframe** from `airframe.stl` (or regenerate via OpenSCAD from `../shell/airframe.scad`). Confirm reduced-scale study geometry.
2. **Fabricate or order the bay board** from `ism-fighter-jet-gerbers.zip` + CPL + `BOM.csv`. Study pads — not a production RP2040 pitch claim.
3. **Mount board** in bay tray with H1–H4 / M3 hardware. Keep J1–J4 accessible for aileron / elevator / rudder / throttle stubs.
4. **Fit stores placeholder** per inert-stores / SAFE-INHIBIT interfaces — mass/footprint only; do not install seekers, guidance, or munitions.
5. **Harness** J1–J4 PWM stubs. Power from a current-limited bench / EPS stub; optionally run `../firmware/` host BIT/UART bring-up.
6. **Visual QA** against `fab-mechanical.md`; photograph board orientation for the lab notebook.
7. **Hand off** to the #78 prototype path (`assembly-notes.md`) for structure → iron-bird sequencing when that campaign proceeds.

## Lab policy

- Physical: fit, clearance, and stores mass/SAFE/INHIBIT placeholders only.
- Simulated: any live launch, fire sequence, or engagement doctrine — **out of scope**.
- Never attach seekers, warheads, fuzing, or arming hardware.

## Next (not this PR)

#78 polish remaining Soft blockers (Flight Lab / HIL — Steve); open product decisions; inquire-for-release gate.
