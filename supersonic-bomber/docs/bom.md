# Supersonic bomber — educational master BOM (#39)

**Product:** ISM-XB-1  
**Slice:** study BOM tying the inert-bay SAFE/INHIBIT fab package to the airframe STL / structural stubs.

## Weapons boundary (hard)

- Payload / bay = **inert mass, CG, volume, SAFE/INHIBIT** stubs only
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming
- **No** employment or targeting content
- **No** ITAR/EAR munition or fire-control designs
- **Not** a procurement order — PNs freeze at inquire-for-release

## Board (SMT) — from `../fab/BOM.csv`

| Ref | Qty | Value | Role |
|-----|-----|-------|------|
| U1 | 1 | RP2040 | Bay SAFE/INHIBIT MCU stub |
| U2 | 1 | IMU | Attitude stub |
| U3 | 1 | RADIO | Telemetry stub |
| J1 | 1 | PinHeader 1×03 | Bay door actuator stub |
| J2 | 1 | PinHeader 1×03 | SAFE discrete stub |
| J3 | 1 | PinHeader 1×03 | INHIBIT / WOW-class discrete stub |
| J4 | 1 | PinHeader 1×03 | Spare channel stub |
| H1–H4 | 4 | M3 hole | Board mounting |

## Mechanical / study article

| ID | Qty | Item | Source |
|----|-----|------|--------|
| MECH-AF-STL | 1 | `airframe_study.stl` print (slender OML + bay keep-out) | `../mechanical/` |
| MECH-SCAD | 1 | `airframe_study.scad` parametric source | `../shell/` |
| MECH-FAST-M3 | lot | M3 hardware for bay board tray | study |
| MECH-TRAY | 1 | Bay-board tray stub | `structural.yaml` |
| PAY-INERT | 1 | Inert bay mass/CG/volume block | `payload-placeholders.yaml` |

## Electrical harness (study)

| ID | Qty | Item | Notes |
|----|-----|------|-------|
| HAR-DOOR | 1 | 3-pin PWM lead | J1 bay door stub |
| HAR-SAFE | 1 | SAFE discrete lead | J2 — inhibit/safe only |
| HAR-INH | 1 | INHIBIT discrete lead | J3 — no arm/release |
| HAR-PWR | 1 | 5 V / GND stub lead | Bench supply only |

## Out of BOM (explicit)

Seekers, guidance kits, munition propulsion, warheads, fuzing/arming hardware, live release actuators, employment stores. Hypersonic TPS coupons belong under `hypersonic-bomber/` (#37), not this tree.
