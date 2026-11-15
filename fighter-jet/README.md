# ISM Fighter Jet

Single-seat fighter airframe for the International Squirrel Machines line — avionics controller, flight-control interfaces, and parametric structural shell.

## Scope
- Avionics controller board (MCU, IMU, radio, power, actuator channels)
- Flight-control interface harness (stick / throttle / surfaces)
- Parametric airframe shell (fuselage, wing, empennage)
- ISM branding (badge / silkscreen)

## Layout
- `kicad/` — avionics PCB schematic + layout scaffold
- `shell/` — parametric OpenSCAD airframe

## Status
Scaffolded. Ready for schematic expansion and airframe parameter tuning.

## Next Steps
1. Expand avionics schematic: full IMU bus, radio module, servo/ESC drivers, power tree.
2. Associate footprints and place components on the avionics PCB.
3. Tune `shell/airframe.scad` parameters and export STLs for fuselage / wing / empennage.
4. Document mounting of the avionics bay and control harness.
5. BOM, assembly notes, renders; then polish and inquire for release.
