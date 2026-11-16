# ISM Gundam — KiCad (mecha control / power) (#46)

Study-scale **limb control + SAFE/INHIBIT** board for ISM-MS-1. Open with **KiCad 8**.

## Weapons boundary (hard)

- Limb PWM channels are **actuator stubs** for packaging / balance study
- `GPIO_SAFE` / `GPIO_INHIBIT` are **stores integration discretes** only (same spirit as fighter-jet inert stores)
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming codes
- **No** live launch / fire sequences
- **No** ITAR/EAR weapon or fire-control designs

## Project-local libraries

| File | Role |
|------|------|
| `sym-lib-table` | `ISM.kicad_sym` |
| `fp-lib-table` | `ISM.pretty/` |
| `ISM.kicad_sym` / `ISM.pretty/` | Study MCU, IMU, RADIO, CONN |

## Schematic / PCB (`ism-gundam-control`)

| Net / header | Role |
|--------------|------|
| I2C | IMU / joint sensors stub |
| SPI | Telemetry / flash stub |
| J1 `PWM_LEG` | Leg actuator channel stub |
| J2 `PWM_ARM` | Arm actuator channel stub |
| J3 `GPIO_SAFE` | Stores SAFE discrete stub |
| J4 `GPIO_INHIBIT` | Stores INHIBIT discrete stub |
| 3V3 / 5V / GND | Rails with PWR_FLAG |

Study MCU footprint pitch is packaging-level (not production RP2040 0.4 mm).
