# Fab package — ISM Camera controller

| File | Use |
|------|-----|
| `ism-camera-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-camera-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT lines have LCSC numbers (EEPROM **C6203**, header **C124418**).
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- OV2640-class image sensor is an off-board module on `J2`.

Regenerate with `python3 scripts/build_camera.py`.
