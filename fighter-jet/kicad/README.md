# ISM Fighter Jet — KiCad (Bay I/O Concentrator)

Avionics-bay **electrical slice** (#75 / Fred verify fixes). Open with **KiCad 8**.

## Project-local libraries
| File | Role |
|------|------|
| `sym-lib-table` | Points at `ISM.kicad_sym` |
| `fp-lib-table` | Points at `ISM.pretty/` |
| `ISM.kicad_sym` | MCU, IMU, RADIO, CONN_SERVO |
| `ISM.pretty/` | QFN-56-1EP_7x7mm_P0.4mm, LGA-14_3x2.5mm_P0.5mm, RADIO_Module, PinHeader_1x03, MountingHole_M3 |

Stock KiCad 8 may not ship the QFN-56 / LGA-14 names we use — **always** open this folder so `${KIPRJMOD}` resolves.

## Schematic / PCB
- Nets wired: I2C, SPI, PWM J1–J4, 3V3 / 5V / GND (PWR_FLAGs on rails)
- Footprints assigned on symbols; mounting holes **H1–H4**
- Study QFN pitch **1.27 mm** in `ISM.pretty` (not production 0.4 mm RP2040)
- 2-layer HVH routing: signal vias + B.Cu verticals; 3V3 under header band on B.Cu

## Firmware
Host BIT/UART: `../firmware/` (`make test`).

## ERC / DRC (KiCad 8.0.9 `kicad-cli`)
Verified from this directory:
- `kicad-cli sch erc …` → **0 violations** (lib_symbols cache uses `ISM:` names)
- `kicad-cli pcb drc …` → **0 errors**, 0 unconnected; `lib_footprint_mismatch` warnings OK for study pads
