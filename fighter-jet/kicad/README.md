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
- Nets wired: I2C, SPI, PWM J1–J4, 3V3 / 5V / GND
- Footprints assigned on symbols; mounting holes **H1–H4**
- U2 (IMU) pads 1–2 spaced with mask margin to avoid SDA/SCL short
- Tracks on F.Cu for bring-up connectivity

## Firmware
Host BIT/UART: `../firmware/` (`make test`).

## ERC / DRC
Target **0 errors** in KiCad 8.0.9 (open project from this directory). Warnings may remain for study pin-count vs full RP2040.
