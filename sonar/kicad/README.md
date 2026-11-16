# ISM Sonar — KiCad (echo AFE / DSP / power) (#40)

Educational echo-sounder / fish-finder study board for ISM-SNR-1. Open with **KiCad 8**.

## Scope limits (hard) — same spirit as submarine B3

- Educational / public echo-sounder class only
- `GPIO_TX` is a **teaching TX-pulse enable stub** — not combat sonar drive
- Analog front-end / DSP / display channels are packaging-level stubs
- **No** quieting or acoustic-signature design
- **No** classified beamforming, ASW tactics, or combat employment
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- **No** ITAR/EAR sonar or acoustic-warfare content

## Project-local libraries

| File | Role |
|------|------|
| `sym-lib-table` | `ISM.kicad_sym` |
| `fp-lib-table` | `ISM.pretty/` |
| `ISM.kicad_sym` / `ISM.pretty/` | Study MCU, IMU, RADIO, CONN |

## Schematic / PCB (`ism-sonar-echo`)

| Net / header | Role |
|--------------|------|
| I2C | IMU / cabin sensors stub |
| SPI | Flash / telemetry stub |
| J1 `GPIO_TX` | TX pulse enable stub (fish-finder class) |
| J2 `I2C_AFE` | Analog front-end / envelope sense stub |
| J3 `UART_DSP` | DSP / range-compute UART stub |
| J4 `GPIO_DISP` | Display / backlight stub |
| 3V3 / 5V / GND | Rails with PWR_FLAG |

Study MCU footprint pitch is packaging-level (not production RP2040 0.4 mm).
