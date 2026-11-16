# Fighter Jet Shell (Study Model)

Parametric OpenSCAD airframe — **proportion / printable study slice** of the ISM-FJ-1 program, not the structural authority model. Geometry contracts: `../interfaces/aircraft-geometry.yaml` + `../interfaces/mechanical-airframe.yaml` (#72).

## Files
- `airframe.scad` — fuselage (avionics + gear wells), wings (hinge grooves), empennage, spar/rib planes, deployed gear, FS markers

## STL exports
Set `show_stations = false`, `show_structure_planes = false`, then:

```bash
openscad -o fuselage.stl -D 'show_stations=false' -D 'show_structure_planes=false' -D 'show_gear_deployed=false' -D 'airframe(); fuselage();' airframe.scad
# Prefer editing the file to call a single module, e.g. only fuselage();
openscad -o fuselage.stl airframe.scad   # after selecting fuselage() only
openscad -o wing.stl airframe.scad       # wing()
openscad -o empennage.stl airframe.scad  # empennage()
openscad -o gear.stl airframe.scad       # landing_gear_deployed()
```

Targets: `fuselage.stl` / `wing.stl` / `empennage.stl` / `gear.stl`.

## Alignment
- `fuselage_length = 420` mm → `% FS` in `../diagrams/stations.md` / geometry YAML.
- NLG FS-18 / MLG FS-55 wells and gear module match `mechanical-airframe.yaml`.
- Next pass: split A01–A07 per `../diagrams/assembly-breakdown.md`.
