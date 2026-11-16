# Fab package — ISM Mouse

| File | Use |
|------|-----|
| `ism-mouse-gerbers.zip` | JLCPCB/PCBWay upload (4-layer + Excellon) |
| `BOM.csv` | SMT BOM with LCSC where a catalog part exists |
| `ism-mouse-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Every **SMT/catalog** line has an LCSC number.
- Rows marked **No LCSC** in Notes are intentional and **do not block** fab readiness:
  - `U5` — custom ISM optical sensor (not a JLCPCB catalog SKU)
  - `H1–H4` — mechanical NPTH mounting holes
  - `CASE` / `FEET` / `SCREWS` / `CABLE` — off-board mechanical / print / cable

Regenerate with `python3 scripts/build_mouse.py`.
