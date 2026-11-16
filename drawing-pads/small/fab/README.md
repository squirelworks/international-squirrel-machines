# Fab package — ISM Drawing Pad (small)

| File | Use |
|------|-----|
| `ism-drawing-pad-small-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-drawing-pad-small-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT lines have LCSC numbers.
- **Default touch IC:** `U3` = **XPT2046** (JLCPCB/LCSC **C19076**), TSSOP-16.
- **Optional:** swap to `ISM:ISM_Touch4_FPC` for direct GPIO/ADC mode (not default fab pop).
- **No LCSC** (intentional): `U1` ISM module, `J3` overlay FPC interface, `H1–H4` NPTH.

Regenerate with `python3 scripts/build_drawing_pads.py`.
