# Tooling — ISM-FJ-1

**Issue:** [#106](https://github.com/squirelworks/international-squirrel-machines/issues/106)  
**Master index:** `tooling.yaml`  
**Manufacturing research (no tools):** `../materials/manufacturing-sourcing.md` (#100)

Assembly jigs, drill/rivet fixtures, composite layup tools, and forming dies keyed to **ISM-FJ-DWG-*** and FS/WS stations. OpenSCAD study tools are parametric (mm) aligned to `shell/airframe.scad` study scale; full-scale factor **36.9** from viability (#103).

## Hard stop
Do **not** design Eric’s shop machines (CNC mill, large-format printer, heat-treat/cure oven). They appear in `tooling.yaml` only as `required_equipment_eric_lane`.

## Layout

| Path | Contents |
|------|----------|
| `jigs/` | Fuselage, wing, empennage assembly jigs (OpenSCAD) |
| `fixtures/` | Drill / rivet fixtures (OpenSCAD) |
| `layup/` | Composite skin / surface layup tools (OpenSCAD) |
| `dies/` | Sheet-forming die concepts (OpenSCAD) |
| `tooling.yaml` | Master index → drawings / stations / process |

## Tool ID convention
`ISM-FJ-TOOL-<NNN>` Rev A — cited from manufacturing travelers and Steve HIL fixtures later.
