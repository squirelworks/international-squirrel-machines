# Hypersonic bomber — assembly notes (#37)

**Product:** ISM-HB-1  
**Slice:** educational build sequence for the study Gerbers + blunt-cone STL package.

## Out of scope (hard)

Same as the design note / Gerbers slice: educational aerothermal / TPS instrumentation only. **No** weapons, munition recipes, seekers, guidance, warheads, fuzing, or classified TPS formulations.

## Preconditions

| Artifact | Path |
|----------|------|
| Gerber zip / CPL / fab BOM | `../fab/` |
| Blunt-cone study STL | `../mechanical/blunt_cone_study.stl` |
| Board project | `../kicad/ism-hb-thermal.*` |
| Master BOM note | `bom.md` |

## Sequence

1. **Print / obtain blunt-cone study article** from `blunt_cone_study.stl` (or regenerate via OpenSCAD from `../shell/blunt_cone_study.scad`). Confirm TPS shell ghosts are educational layout only.
2. **Fabricate or order the thermal board** from `ism-hb-thermal-gerbers.zip` + CPL + `BOM.csv`. Study pads — not a production RP2040 pitch claim.
3. **Mount board** on tray under the TPS shell keep-out with H1–H4 / M3 hardware. Keep J1–J4 accessible for sense stubs.
4. **Attach teaching sense leads** for thermistor/TC and heat-flux stubs (bench resistors / dummy sensors OK). Do not install classified TPS coupons or live munitions.
5. **Power** from a current-limited bench supply. Exercise status stubs as packaging BIT only.
6. **Teaching demos (optional)** run `stagnation_examples.py` / `heat_flux_examples.py` — textbook checks, not flight clearance.
7. **Visual QA** against `structural.md` and `heat-shield-tps.md` class language; photograph board orientation for the lab notebook.

## Lab policy

- Physical: fit, clearance, and teaching instrumentation only.
- Simulated: any weapons employment, classified TPS performance, or scramjet design — **out of scope**.
- Over-temp / TPS_OK discretes are packaging status only — not arm/release channels.

## Next (not this PR)

Polish checklist / inquire-for-release gate; remaining sibling BOM slices.
