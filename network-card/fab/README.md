# Fab package — ISM Network Card

| File | Use |
|------|-----|
| `ism-network-card-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-network-card-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog lines include W5500 **C113367**, RJ45 **C2839419**, USB-C **C165948**.
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- PoE / PCIe / Wi-Fi remain follow-ups.

Regenerate with `python3 scripts/build_network_card.py`.
