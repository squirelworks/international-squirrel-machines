# Drawing Number & Revision Convention — ISM-FJ-1

## Format

```
ISM-FJ-DWG-<NNN>  Rev <letter>
```

| Field | Meaning |
|-------|---------|
| `ISM-FJ` | Product family (Nutcracker air vehicle) |
| `DWG` | Blueprint / ICD sheet (not a narrative note) |
| `NNN` | Three-digit sheet number, stable once issued |
| `Rev` | Capital letter; `A` = first published under this scheme |

Narrative Markdown under `fighter-jet/**` is **not** a drawing. Downstream issues cite **drawing IDs** (`ISM-FJ-DWG-…`) for geometry and ICDs, and file paths for prose.

## Datum (aircraft reference)

| Axis | Positive | Origin |
|------|----------|--------|
| **X** (FS) | Aft | Nose tip (FS-0) |
| **Y** (BL) | Right (pilot view forward) | Fuselage centerline |
| **Z** (WL) | Up | Study waterline through fuselage geometric center (`fuselage_height/2` in `shell/airframe.scad`) |

- **FS** = fuselage station = % of fuselage length × `L` (study `L = 420 mm`).
- **WS** = wing station = % of semi-span from centerline outboard.
- **BL** = butt line = lateral offset from centerline (mm study / % span for full-scale).
- Units on every sheet: **millimetres** for study scale; **% FS / % WS** remain scale-invariant.
- Study scale stated on each sheet: **1 SVG drawing unit = 1 mm** of the OpenSCAD study model unless a scale bar says otherwise.

## Sheet ownership
Sheets live under `fighter-jet/diagrams/`. Machine-readable companions for Flight Lab (Steve / SquirrelSoft) live under `fighter-jet/interfaces/` and must stay consistent with these drawing IDs.
