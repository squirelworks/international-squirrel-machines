# ISM Aircraft Carrier — KiCad (scale-model deck control) (#45)

Study-scale **deck / aviation-support control** board for ISM-CV-1. Open with **KiCad 8**.

## Weapons boundary (hard)

- Outputs are **elevator / catapult / arresting / rudder actuator stubs** for a scale model only
- Catapult and arresting channels are **load / keep-out class** stubs — not classified plant design
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- Combat topside and aviation ordnance remain mass/footprint placeholders in `../interfaces/mass-placeholders.yaml`

## Project-local libraries

| File | Role |
|------|------|
| `sym-lib-table` | `ISM.kicad_sym` |
| `fp-lib-table` | `ISM.pretty/` |
| `ISM.kicad_sym` / `ISM.pretty/` | Study MCU, IMU, RADIO, CONN |

## Schematic / PCB (`ism-carrier-deck`)

| Net / header | Role |
|--------------|------|
| I2C | IMU / attitude stub |
| SPI | Telemetry radio stub |
| J1 `PWM_ELEV` | Aircraft elevator stub |
| J2 `PWM_CAT` | Catapult shuttle / load stub |
| J3 `PWM_ARREST` | Arresting-gear load stub |
| J4 `PWM_RUDDER` | Ship rudder / steering stub |
| 3V3 / 5V / GND | Rails with PWR_FLAG |

Study MCU footprint pitch is packaging-level (not production RP2040 0.4 mm).
