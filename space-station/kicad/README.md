# ISM Space Station — KiCad (hab power / ECLSS / CDH) (#42)

Habitat / civil-station study board for ISM-SSN-1. Open with **KiCad 8**.

## Weapons boundary (hard)

- Habitat electronics stubs only: EPS, ECLSS actuator, CDH UART, docking sense/enable
- Docking channel is **berthing / umbilical** class — not a weapons interface
- **No** weapons, seekers, guidance-to-target, warheads, fuzing, or combat employment
- **No** ITAR/EAR station or weapon designs
- Attitude / GN&C later boards stay station-keeping — **not** weapons pointing

## Project-local libraries

| File | Role |
|------|------|
| `sym-lib-table` | `ISM.kicad_sym` |
| `fp-lib-table` | `ISM.pretty/` |
| `ISM.kicad_sym` / `ISM.pretty/` | Study MCU, IMU, RADIO, CONN |

## Schematic / PCB (`ism-station-hab`)

| Net / header | Role |
|--------------|------|
| I2C | IMU / cabin sensors stub |
| SPI | Telemetry / flash stub |
| J1 `I2C_EPS` | Electrical power system telemetry stub |
| J2 `PWM_ECLSS` | ECLSS fan / valve actuator stub |
| J3 `UART_CDH` | Command & data handling UART stub |
| J4 `GPIO_DOCK` | Docking sense / umbilical enable stub |
| 3V3 / 5V / GND | Rails with PWR_FLAG |

Study MCU footprint pitch is packaging-level (not production RP2040 0.4 mm).
