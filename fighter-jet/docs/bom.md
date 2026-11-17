# Fighter Jet — educational bay/study BOM (#85)

**Product:** ISM-FJ-1 “Nutcracker”  
**Slice:** study BOM tying the avionics-bay fab package to the study airframe STL. Program-level master BOM remains `bom/master-bom.yaml` (#78).

## Scope / weapons boundary (hard)

- Bay board = surface / throttle PWM stubs only
- Program stores / weapons = **mass / footprint / SAFE / INHIBIT** placeholders only
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming codes
- **No** live launch / fire sequences or engagement doctrine
- **No** ITAR/EAR weapon or fire-control designs
- Shell STL is a **reduced-scale study model**, not production tooling
- **Not** a procurement order — PNs freeze at inquire-for-release

## Board (SMT) — from `../fab/BOM.csv`

| Ref | Qty | Value | Role |
|-----|-----|-------|------|
| U1 | 1 | RP2040 | Bay I/O concentrator MCU stub |
| U2 | 1 | IMU-6DOF | Bay attitude sense stub |
| U3 | 1 | RADIO | Telemetry stub |
| J1 | 1 | PinHeader 1×03 | Aileron PWM stub |
| J2 | 1 | PinHeader 1×03 | Elevator PWM stub |
| J3 | 1 | PinHeader 1×03 | Rudder PWM stub |
| J4 | 1 | PinHeader 1×03 | Throttle PWM stub |
| H1–H4 | 4 | M3 hole | Board mounting |

## Mechanical / study article

| ID | Qty | Item | Source |
|----|-----|------|--------|
| MECH-AF-STL | 1 | `airframe.stl` print (reduced-scale study) | `../shell/` |
| MECH-SCAD | 1 | `airframe.scad` parametric source | `../shell/` |
| MECH-FAST-M3 | lot | M3 hardware for bay tray | study |
| STORES-STUB | 1 | Hardpoint mass/footprint + SAFE/INHIBIT placeholder | `../interfaces/inert-stores.yaml`, `safe-inhibit-table.yaml` |

## Electrical harness (study)

| ID | Qty | Item | Notes |
|----|-----|------|-------|
| HAR-AIL | 1 | Aileron PWM lead | J1 |
| HAR-ELV | 1 | Elevator PWM lead | J2 |
| HAR-RUD | 1 | Rudder PWM lead | J3 |
| HAR-THR | 1 | Throttle PWM lead | J4 |
| HAR-PWR | 1 | Bench / EPS stub | Current-limited |

## Related program BOM (#78)

Airframe / systems / avionics LRU categories: `bom/master-bom.yaml` + `assembly-notes.md`. This file covers the **Gerbers/STL study package** only.

## Out of BOM (explicit)

Seekers, guidance kits, munition propulsion, warheads, fuzing/arming hardware, live launch/fire sequence gear, ITAR/EAR weapon or fire-control designs.
