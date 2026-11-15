# Fighter Jet Shell (Study Model)

Parametric OpenSCAD airframe — **proportion / printable study slice** of the ISM-FJ-1 program, not the structural authority model. Program docs for structure, materials, FBW, etc. live in sibling directories under `fighter-jet/`.

## Files
- `airframe.scad` — fuselage, wing, empennage, avionics bay cutout, ISM badge boss, optional FS station markers

## Expected exports
- `fuselage.stl` / `wing.stl` / `empennage.stl` (or combined)

## Alignment
- Default `fuselage_length = 420` mm study scale maps to `% FS` in `../diagrams/stations.md`.
- Set `show_stations = false` before production print exports.
- Next pass: split A01–A07 assemblies per `../diagrams/assembly-breakdown.md`.
