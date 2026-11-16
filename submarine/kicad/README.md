# ISM Submarine — KiCad (scale-model control) (#44)

Study-scale **submarine control / trim** board for ISM-SS-1. Open with **KiCad 8**.

**Independent of warship KiCad (#160)** — cloned from the fighter bay study template on `main`, not stacked on #160.

## Scope limits (hard)

- Outputs are **scale-model** prop / stern-plane / rudder / ballast actuator stubs only
- Sonar remains **mass/footprint** elsewhere (`../interfaces/mass-placeholders.yaml`) — **no** acoustic processing on this board
- **No** quieting, life-support design, weapons interfaces, fire control
- **No** seekers, guidance, munition propulsion, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) data

## Project-local libraries

| File | Role |
|------|------|
| `sym-lib-table` | Points at `ISM.kicad_sym` |
| `fp-lib-table` | Points at `ISM.pretty/` |
| `ISM.kicad_sym` | MCU, IMU, RADIO, CONN (actuator headers) |
| `ISM.pretty/` | Study footprints |

## Schematic / PCB (`ism-submarine-control`)

| Net / header | Role |
|--------------|------|
| I2C | IMU attitude / trim stub |
| SPI | Telemetry radio stub |
| J1 `PWM_PROP` | Propulsor / thruster stub |
| J2 `PWM_STERN` | Stern-plane servo stub |
| J3 `PWM_RUDDER` | Rudder servo stub |
| J4 `PWM_BALLAST` | Ballast / trim pump stub |
| 3V3 / 5V / GND | Rails with PWR_FLAG |

Study MCU footprint pitch is packaging-level (not production RP2040 0.4 mm).
