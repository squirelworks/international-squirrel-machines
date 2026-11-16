# Fab package — ISM Sound Card

| File | Use |
|------|-----|
| `ism-sound-card-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-sound-card-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog lines include PCM5102A **C96588**, jack **C2839290**, USB-C **C165948**.
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- Headphone amp / mic / UAC2 class remain follow-ups.

Regenerate with `python3 scripts/build_sound_card.py`.
