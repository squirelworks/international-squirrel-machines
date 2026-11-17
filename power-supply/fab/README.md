# Fab package — ISM Power Supply (DC rail board)

| File | Use |
|------|-----|
| `ism-power-supply-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-power-supply-cpl.csv` | Centroid / pick-and-place |

## Safety

- **No mains** on this PCB (Track A). Input is 12 V DC from a **certified** AC-DC brick.
- See `../docs/safety.md`.

Regenerate with `python3 scripts/build_power_supply.py`.
