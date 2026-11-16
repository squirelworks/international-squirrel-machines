# Fab package — ISM Drawing Pad (medium)

| File | Use |
|------|-----|
| `ism-drawing-pad-medium-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-drawing-pad-medium-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT lines have LCSC numbers.
- **No LCSC** (intentional): `U1` ISM module, `U3` touch FPC interface, `H1–H4` NPTH.

Regenerate with `python3 scripts/build_drawing_pads.py`.
