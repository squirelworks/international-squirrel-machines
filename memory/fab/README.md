# Fab package — ISM Memory (RAM module)

| File | Use |
|------|-----|
| `ism-memory-gerbers.zip` | JLCPCB/PCBWay upload (4-layer + Excellon) |
| `BOM.csv` | SMT BOM with LCSC where a catalog part exists |
| `ism-memory-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Every **SMT/catalog** line has an LCSC number.
- **Default memory ICs:** `U1,U2` = Lyontek **LY68L6400SLIT** (JLCPCB/LCSC **C261881**), stock SOIC-8.
- **Optional:** swap land pattern to `ISM:ISM_DRAM_SOIC` for a custom ISM DRAM package (not default fab pop).
- Rows marked **No LCSC** in Notes are intentional and **do not block** fab readiness:
  - `J1` — edge fingers (PCB feature, not an SMT SKU)
  - `H1–H2` — mechanical NPTH mounting holes

Regenerate with `python3 scripts/build_memory.py`.
