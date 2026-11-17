# Fab package — ISM SCSI carrier

| File | Use |
|------|-----|
| `ism-scsi-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-scsi-cpl.csv` | Centroid / pick-and-place |

Commodity **SCSI drive** is off-board. Data bus stubbed — USB–SCSI bridge is a follow-up.
Regenerate with `python3 scripts/build_scsi.py`.
