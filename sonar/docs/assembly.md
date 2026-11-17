# Sonar — assembly notes (#40)

**Product:** ISM-SNR-1  
**Slice:** educational build sequence for the study Gerbers + enclosure STL package.

## Scope / weapons boundary (hard)

Same as the design note / Gerbers slice: educational / public echo-sounder class only. Transducers remain **mass / footprint / frequency-class** stubs. **No** quieting, acoustic signature, classified beamforming, ASW tactics, weapons, fire control, seekers, guidance, warheads, or fuzing.

## Preconditions

| Artifact | Path |
|----------|------|
| Gerber zip / CPL / fab BOM | `../fab/` |
| Enclosure study STL | `../mechanical/enclosure_study.stl` |
| Board project | `../kicad/ism-sonar-echo.*` |
| Master BOM note | `bom.md` |

## Sequence

1. **Print / obtain enclosure study article** from `enclosure_study.stl` (or regenerate via OpenSCAD from `../shell/enclosure_study.scad`). Confirm enclosure / transducer face / ribs ghosts.
2. **Fabricate or order the echo board** from `ism-sonar-echo-gerbers.zip` + CPL + `BOM.csv`. Study pads — not a production RP2040 pitch claim.
3. **Mount board** on tray with H1–H4 / M3 hardware. Keep J1–J4 accessible for TX / AFE / DSP / display stubs.
4. **Fit transducer placeholder** per `transducer-placeholders.yaml` — mass/footprint/frequency-class only; do not install quieting or classified arrays.
5. **Harness** J1 TX enable, J2 AFE, J3 DSP, J4 display. Power from a current-limited bench / EPS stub.
6. **Range-equation demo (optional)** run `../docs/range_equation_examples.py` teaching checks — not a combat clearance.
7. **Visual QA** against `structural.md`; photograph board orientation for the lab notebook.

## Lab policy

- Physical: fit, clearance, and transducer mass/footprint placeholders only.
- Simulated: quieting, acoustic signature, ASW tactics, or weapons employment — **out of scope**.
- Never attach seekers, warheads, fire control, or fuzing hardware.

## Next

Polish checklist / inquire-for-release gate (open).
