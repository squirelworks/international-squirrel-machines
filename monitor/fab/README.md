# Fab package — ISM Monitor controller

| File | Use |
|------|-----|
| `ism-monitor-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-monitor-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT lines have LCSC numbers (EEPROM **C6203**, MOSFET **C8545**, HDMI **C132555**).
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- HDMI TMDS stays off this board (commercial scaler); DDC/HPD/5V are on-board.

Regenerate with `python3 scripts/build_monitor.py`.
