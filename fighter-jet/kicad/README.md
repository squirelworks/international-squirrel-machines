# ISM Fighter Jet — KiCad (Bay I/O Concentrator)

This project is the **avionics-bay electrical slice** of ISM-FJ-1, not the whole aircraft. Mission computer, FCC, buses, FBW, and sensors are documented under `../avionics/`, `../flight-controls/`, and siblings.

Project files:
- `ism-fighter-jet.kicad_pro`
- `ism-fighter-jet.kicad_sch` (MCU, IMU, radio, actuator headers)
- `ism-fighter-jet.kicad_pcb` (bay outline scaffold)

Logical PWM channels J1–J4 map to actuation trunks A1–A4 in `../diagrams/wiring-harness.md` (aileron, elevator, rudder, throttle).

## Next implementation steps
1. Expand schematic: full IMU bus, radio, crystal, decoupling, USB-C/UART debug, EHA/servo drivers, power tree.
2. Freeze connector pinout against harness ICD.
3. Associate footprints; place; route; export Gerbers.

Pure Squirrel-OS/2 development.
