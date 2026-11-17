# Fab package — ISM SATA carrier

| File | Use |
|------|-----|
| `ism-sata-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-sata-cpl.csv` | Centroid / pick-and-place |

Commodity **SATA drive** is off-board. A/B pairs stubbed — USB–SATA bridge is a follow-up.
Regenerate with `python3 scripts/build_sata.py`.
