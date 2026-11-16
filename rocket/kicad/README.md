# ISM Rocket — KiCad (passive logger / recovery) (#41)

Hobby-class **passive flight logger + recovery deployment** board for ISM-RK-1. Open with **KiCad 8**.

## Scope limits (hard)

- **Certified commercial hobby motors only** (public NAR/TRA class catalogs) — motor is not designed here
- Avionics = **passive** logger / altimeter sensing + recovery-channel stubs
- **No** guidance, steering, or active flight control
- **No** seekers, munition propulsion, warheads, or fuzing
- **No** ballistic-missile / RV content; **no** ITAR/EAR data

Recovery headers are e-match **class** stubs for drogue/main deployment in hobby rocketry — not weapons.

## Project-local libraries

| File | Role |
|------|------|
| `sym-lib-table` | `ISM.kicad_sym` |
| `fp-lib-table` | `ISM.pretty/` |
| `ISM.kicad_sym` / `ISM.pretty/` | Study MCU, IMU, RADIO, CONN |

## Schematic / PCB (`ism-rocket-logger`)

| Net / header | Role |
|--------------|------|
| I2C | IMU / baro logger stub |
| SPI | Telemetry / flash radio stub |
| J1 `PWM_DROGUE` | Drogue recovery channel stub |
| J2 `PWM_MAIN` | Main chute recovery channel stub |
| J3 `PWM_BUZZER` | Locator buzzer stub |
| J4 `PWM_SAFE_LED` | SAFE / armed-inhibit status LED stub |
| 3V3 / 5V / GND | Rails with PWR_FLAG |

Study MCU footprint pitch is packaging-level (not production RP2040 0.4 mm).
