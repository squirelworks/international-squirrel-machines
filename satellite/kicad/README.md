# ISM Satellite — KiCad (OBC / EPS / radio) (#31)

Civilian / educational **bus** study board for ISM-SAT-1. Open with **KiCad 8**.

## Scope / weapons boundary (hard)

- Bus electronics stubs only: OBC, EPS sense/control, radio UART, magnetorquer PWM, payload enable
- Payload = **mass / power / data** stubs — enable line is a bus power gate, not a weapon interface
- **No** weapons, seekers, guidance-to-target, warheads, or fuzing
- **No** ITAR/EAR bus or payload designs
- ADCS channel is coarse magnetorquer-class — **not** weapons pointing

## Project-local libraries

| File | Role |
|------|------|
| `sym-lib-table` | `ISM.kicad_sym` |
| `fp-lib-table` | `ISM.pretty/` |
| `ISM.kicad_sym` / `ISM.pretty/` | Study MCU, IMU, RADIO, CONN |

## Schematic / PCB (`ism-satellite-bus`)

| Net / header | Role |
|--------------|------|
| I2C | IMU / sensors stub |
| SPI | Flash / secondary bus stub |
| J1 `I2C_EPS` | EPS telemetry / control stub |
| J2 `UART_RADIO` | TT&C radio UART stub |
| J3 `PWM_MTQ` | Magnetorquer drive stub (coarse ADCS) |
| J4 `GPIO_PL_EN` | Payload bus-power enable stub |
| 3V3 / 5V / GND | Rails with PWR_FLAG |

Study MCU footprint pitch is packaging-level (not production RP2040 0.4 mm).
