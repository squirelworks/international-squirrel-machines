# ISM Hypersonic Bomber — KiCad (thermal / TPS sense) (#37)

Study-scale **educational thermal / TPS instrumentation** board for ISM-HB-1. Open with **KiCad 8**.

## Out of scope (hard)

- **No** weapons, munitions, guidance, seekers, warheads, fuzing, or arming
- **No** operational employment or targeting
- **No** scramjet / propulsion design recipes
- **No** ITAR/EAR TPS formulations or classified materials data
- Channels are **teaching sense / status stubs** only

## Project-local libraries

| File | Role |
|------|------|
| `sym-lib-table` | `ISM.kicad_sym` |
| `fp-lib-table` | `ISM.pretty/` |
| `ISM.kicad_sym` / `ISM.pretty/` | Study MCU, IMU, RADIO, CONN |

## Schematic / PCB (`ism-hb-thermal`)

| Net / header | Role |
|--------------|------|
| I2C | IMU / cabin / skin sensors stub |
| SPI | Telemetry / flash stub |
| J1 `ADC_TC1` | Thermocouple / RTD sense stub |
| J2 `ADC_TC2` | Second thermal sense stub |
| J3 `GPIO_TPS_OK` | TPS health status stub |
| J4 `GPIO_OVERTEMP` | Over-temp inhibit packaging stub |
| 3V3 / 5V / GND | Rails with PWR_FLAG |

Study MCU footprint pitch is packaging-level (not production RP2040 0.4 mm).
