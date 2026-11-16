# Fab package — ISM CPU module

| File | Use |
|------|-----|
| `ism-cpu-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-cpu-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT/connector lines have LCSC numbers (flash **C82307**).
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- Heatsink shroud is OpenSCAD under `cpu/shell/`.

Regenerate with `python3 scripts/build_cpu.py`.
