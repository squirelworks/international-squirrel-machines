# ISM Subsonic Bomber — KiCad (inert bay SAFE/INHIBIT) (#38)

Study-scale **bay door / SAFE / INHIBIT** board for ISM-SB-1. Open with **KiCad 8**.

## Weapons boundary (hard)

- Bay channels are **inert mass / door / SAFE-INHIBIT integration stubs** only
- `GPIO_WOW` is weight-on-wheels sense for inhibit logic packaging — not arming
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming codes
- **No** employment, targeting, or weapons-effectiveness content
- **No** ITAR/EAR munition or fire-control designs

## Project-local libraries

| File | Role |
|------|------|
| `sym-lib-table` | `ISM.kicad_sym` |
| `fp-lib-table` | `ISM.pretty/` |
| `ISM.kicad_sym` / `ISM.pretty/` | Study MCU, IMU, RADIO, CONN |

## Schematic / PCB (`ism-sb-bay`)

| Net / header | Role |
|--------------|------|
| I2C | IMU / airframe sensors stub |
| SPI | Telemetry / flash stub |
| J1 `PWM_DOOR` | Bay door actuator stub |
| J2 `GPIO_SAFE` | Bay SAFE discrete stub |
| J3 `GPIO_INHIBIT` | Bay INHIBIT discrete stub |
| J4 `GPIO_WOW` | Weight-on-wheels sense stub |
| 3V3 / 5V / GND | Rails with PWR_FLAG |

Study MCU footprint pitch is packaging-level (not production RP2040 0.4 mm).
