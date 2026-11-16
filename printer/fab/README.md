# Fab package — ISM Printer controller

| File | Use |
|------|-----|
| `ism-printer-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-printer-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT lines have LCSC numbers (**DRV8833PWPR = C50506**).
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- Print head / paper path mechanics are off-board.

Regenerate with `python3 scripts/build_printer.py`.
