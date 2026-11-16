# Fab package — ISM Keyboard XL

| File | Use |
|------|-----|
| `ism-keyboard-xl-gerbers.zip` | JLCPCB/PCBWay upload (4-layer + Excellon, incl. blind-via drills) |
| `BOM.csv` | SMT BOM with LCSC where a catalog part exists |
| `ism-keyboard-xl-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Every **SMT/catalog** line has an LCSC number.
- Rows marked **No LCSC** in Notes are intentional and **do not block** fab readiness:
  - `U1` — custom ISM RP2040 carrier (not a JLCPCB catalog SKU)
  - `H1–H4` — mechanical NPTH mounting holes (no SMT part)

119× MX hotswap + diodes. Regenerate with `python3 scripts/build_keyboard_xl.py`.
