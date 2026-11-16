# ISM Warship — KiCad (scale-model control) (#43)

Study-scale **ship control / trim logger** board for ISM-WS-1. Open with **KiCad 8**.

## Weapons boundary (hard)

- Outputs are **propulsion / steering / ballast actuator stubs** for a scale model only
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- Combat topside remains mass/footprint placeholders in `../interfaces/mass-placeholders.yaml`

## Project-local libraries

| File | Role |
|------|------|
| `sym-lib-table` | Points at `ISM.kicad_sym` |
| `fp-lib-table` | Points at `ISM.pretty/` |
| `ISM.kicad_sym` | MCU, IMU, RADIO, CONN (actuator headers) |
| `ISM.pretty/` | Study footprints (same family as fighter bay study) |

## Schematic / PCB (`ism-warship-control`)

| Net / header | Role |
|--------------|------|
| I2C | IMU trim / attitude stub |
| SPI | Telemetry radio stub |
| J1 `PWM_PORT` | Port thruster / prop stub |
| J2 `PWM_STBD` | Starboard thruster stub |
| J3 `PWM_RUDDER` | Rudder servo stub |
| J4 `PWM_BALLAST` | Ballast / trim pump stub |
| 3V3 / 5V / GND | Rails with PWR_FLAG |

Study MCU footprint pitch is packaging-level (not production RP2040 0.4 mm).
