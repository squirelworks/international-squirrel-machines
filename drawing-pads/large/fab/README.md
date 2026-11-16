# Fab package — ISM Drawing Pad (large)

| File | Use |
|------|-----|
| `ism-drawing-pad-large-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-drawing-pad-large-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT lines have LCSC numbers.
- **No LCSC** (intentional): `U1` ISM module, `U3` touch FPC interface, `H1–H4` NPTH.

Regenerate with `python3 scripts/build_drawing_pads.py`.
