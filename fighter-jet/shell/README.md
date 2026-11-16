# Fighter Jet Shell (Study Model)

Parametric OpenSCAD airframe — **proportion / printable study slice** of the ISM-FJ-1 program, not the structural authority model. Geometry contracts: `../interfaces/aircraft-geometry.yaml` + `../interfaces/mechanical-airframe.yaml` (#72).

## Files
- `airframe.scad` — fuselage (avionics + gear wells), wings (hinge grooves), empennage, spar/rib planes, deployed gear, FS markers
- `propulsion_keepouts.scad` — engine/duct/nozzle packaging modules (A2 #120)
- `propulsion_keepouts_preview.scad` — render keep-outs
- `propulsion_intersection_check.scad` — cad-verify witness cube + echo (clash-free packaging)
- `propulsion_clash_probe.scad` (LIB) + `check_propulsion_packaging.sh` — assert empty ∩ (bay∪gear); script expects OpenSCAD “empty” on the probe driver

## STL exports
Debug flags `show_stations` / `show_structure_planes` default **false** (single manifold `airframe()` solid when gear included). Set true only for on-screen FS/WS planes.

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
