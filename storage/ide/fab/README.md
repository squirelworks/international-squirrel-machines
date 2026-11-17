# Fab package — ISM IDE carrier

| File | Use |
|------|-----|
| `ism-ide-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-ide-cpl.csv` | Centroid / pick-and-place |

Commodity **PATA/IDE drive** is off-board. ATA data bus stubbed — USB–PATA bridge is a follow-up.
Regenerate with `python3 scripts/build_ide.py`.
