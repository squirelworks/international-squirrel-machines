# Space Station — assembly notes (#42)

**Product:** ISM-SSN-1  
**Slice:** educational build sequence for the study Gerbers + module STL package.

## Scope / weapons boundary (hard)

Same as the design note / Gerbers slice: habitat / civil station architecture only. Docking remains **mass / volume / power** stubs — **no** weapons, seekers, guidance-to-target, warheads, or fuzing.

## Preconditions

| Artifact | Path |
|----------|------|
| Gerber zip / CPL / fab BOM | `../fab/` |
| Module study STL | `../mechanical/module_study.stl` |
| Board project | `../kicad/ism-station-hab.*` |
| Master BOM note | `bom.md` |

## Sequence

1. **Print / obtain module study article** from `module_study.stl` (or regenerate via OpenSCAD from `../shell/module_study.scad`). Confirm habitat / node / truss / berthing ghosts.
2. **Fabricate or order the habitat board** from `ism-station-hab-gerbers.zip` + CPL + `BOM.csv`. Study pads — not a production RP2040 pitch claim.
3. **Mount board** on tray with H1–H4 / M3 hardware. Keep J1–J4 accessible for EPS / ECLSS / C&DH / docking stubs.
4. **Fit docking placeholder** per `docking-placeholders.yaml` — mass/volume/power only; do not install combat docking adapters.
5. **Harness** J1 EPS, J2 ECLSS, J3 C&DH, J4 docking sense. Power from a current-limited bench / EPS stub.
6. **ECLSS / power-budget demo (optional)** run `../docs/eclss_budget_examples.py` teaching checks — not a flight clearance.
7. **Visual QA** against `structural.md`; photograph board orientation for the lab notebook.

## Lab policy

- Physical: fit, clearance, and docking mass/volume/power placeholders only.
- Simulated: any weapons employment or guidance-to-target — **out of scope**.
- Never attach seekers, warheads, or fuzing hardware.

## Next

Polish checklist / inquire-for-release gate (open).
