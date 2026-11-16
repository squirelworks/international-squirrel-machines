# Fab package — ISM Case front panel

| File | Use |
|------|-----|
| `ism-case-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-case-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT/connector lines have LCSC numbers.
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- Chassis mechanicals are OpenSCAD under `case/shell/`.

Regenerate with `python3 scripts/build_case.py`.
