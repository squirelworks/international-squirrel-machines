# Fab package — ISM Motherboard

| File | Use |
|------|-----|
| `ism-motherboard-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-motherboard-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT/connector lines have LCSC numbers.
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- CPU module and proper DIMM/ATX24 sockets are off-board follow-ups.

Regenerate with `python3 scripts/build_motherboard.py`.
