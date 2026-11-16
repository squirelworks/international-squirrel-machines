# ISM Fighter Jet — KiCad (Bay I/O Concentrator)

Avionics-bay **electrical slice** of ISM-FJ-1 (#75) — not the whole aircraft. FCC, MC, buses, FBW, and sensors: `../avionics/`, `../flight-controls/`.

## Files
- `ism-fighter-jet.kicad_pro`
- `ism-fighter-jet.kicad_sch` — MCU, IMU, radio, actuator headers J1–J4, USB, power pins
- `ism-fighter-jet.kicad_pcb` — bay outline scaffold (~120×80 mm)

## Schematic coverage (#75)
| Block | Status |
|-------|--------|
| IMU I2C | Present (`ISM:IMU`) |
| Radio SPI | Present (`ISM:RADIO`) |
| Actuator PWM headers | J1–J4 → trunks A1–A4 |
| USB debug | DP/DM on MCU |
| Power tree | 3V3/GND on symbols; 28 V→5 V/3V3 tree documented in `../avionics/bay-pcb-placement.md` / architecture (PDU upstream) |

Logical PWM: J1 aileron, J2 HT, J3 rudder, J4 flaperon/throttle study — aligned with `../interfaces/actuators.yaml` study path.

## Placement
See `../avionics/bay-pcb-placement.md`. Pinouts: `../avionics/connectors-pinouts.md`.

## Next
1. Associate footprints; route; Gerbers.
2. Freeze connector series against harness ICD.
3. Firmware bring-up (#84) against this baseline.

Pure Squirrel-OS/2 development. Soft UI apps are out of scope here.
