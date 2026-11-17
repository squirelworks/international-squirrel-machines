# Fab package — ISM NVMe carrier

| File | Use |
|------|-----|
| `ism-nvme-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-nvme-cpl.csv` | Centroid / pick-and-place |

Commodity **M.2 2280 NVMe SSD** is off-board. PCIe lanes stubbed — USB bridge ASIC is a follow-up.
Regenerate with `python3 scripts/build_nvme.py`.
