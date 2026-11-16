# Fab package — ISM Graphics Card

| File | Use |
|------|-----|
| `ism-graphics-card-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-graphics-card-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog lines include HDMI **C132555**, EDID **C6203**, DRAM **C261881**.
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- HDMI TMDS / full GPU PHY remain off-board (follow-up).

Regenerate with `python3 scripts/build_graphics_card.py`.
