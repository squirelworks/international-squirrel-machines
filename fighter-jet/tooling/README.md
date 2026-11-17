# Tooling — ISM-FJ-1

**Issue:** [#106](https://github.com/squirelworks/international-squirrel-machines/issues/106)  
**Slice:** 4b fab-ready study package (STL + STEP markers, BOM, drawings, assembly).  
**Master index:** `tooling.yaml`  
**Manufacturing research (no tools):** `../materials/manufacturing-sourcing.md` (#100)

Assembly jigs, drill/rivet fixtures, composite layup tools (incl. canopy / intake mandrels), and forming dies keyed to **ISM-FJ-DWG-*** and FS/WS stations. OpenSCAD study tools are parametric (mm) aligned to `shell/airframe.scad` study scale; full-scale factor **36.9** from viability (#103).

## Hard stop
Do **not** design Eric’s shop machines (CNC mill, large-format printer, heat-treat/cure oven). They appear in `tooling.yaml` only as `required_equipment_eric_lane`.

Soft #79/#80 = **Steve’s lane**. Product decisions = **PROPOSED only** (`../docs/decisions.md`).

## Layout

| Path | Contents |
|------|----------|
| `jigs/` | Fuselage, wing, empennage assembly jigs (`.scad` / `.stl` / `.step`) |
| `fixtures/` | Drill / rivet fixtures |
| `layup/` | Wing skin, canopy, intake layup tools |
| `dies/` | Sheet-forming die concepts |
| `export.sh` | Regenerate STL + STEP placeholders |
| `bom.md` / `BOM.csv` | Educational tooling BOM |
| `drawings.md` | Drawing / station cross-refs |
| `assembly.md` | Use / build sequence |
| `tooling.yaml` | Master index → drawings / stations / process |

## Tool ID convention
`ISM-FJ-TOOL-<NNN>` Rev A — TOOL-010…080 in this package.

## Exports
```bash
./export.sh
```
STEP files follow the repo study-placeholder convention (not full B-rep CAD).
