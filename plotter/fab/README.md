# Fab package — ISM Plotter controller

| File | Use |
|------|-----|
| `ism-plotter-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-plotter-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT lines have LCSC numbers (**DRV8833PWPR = C50506**).
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- Gantry rails / pen mechanics are off-board.

Regenerate with `python3 scripts/build_plotter.py`.
