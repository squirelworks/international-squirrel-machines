# Fab package — ISM Memory (RAM module)

| File | Use |
|------|-----|
| `ism-memory-gerbers.zip` | JLCPCB/PCBWay upload (4-layer + Excellon) |
| `BOM.csv` | SMT BOM with LCSC where a catalog part exists |
| `ism-memory-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Every **SMT/catalog** line has an LCSC number.
- Rows marked **No LCSC** in Notes are intentional and **do not block** fab readiness:
  - `U1,U2` — custom ISM DRAM packages
  - `J1` — edge fingers (PCB feature, not an SMT SKU)
  - `H1–H2` — mechanical NPTH mounting holes

Regenerate with `python3 scripts/build_memory.py`.
