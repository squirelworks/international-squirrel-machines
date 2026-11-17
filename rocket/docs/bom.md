# Rocket — educational master BOM (#41)

**Product:** ISM-RK-1  
**Slice:** study BOM tying the passive logger/recovery fab package to the airframe STL / structural stubs.

## Scope limits (hard)

- Hobby / educational packaging only
- **Certified commercial hobby motors only** (NAR / TRA public catalogs) — motor is owner-supplied, not fabricated here
- **No** guidance, steering, or active flight control
- **No** ballistic-missile or reentry-vehicle content
- **No** ITAR/EAR data
- **Not** a procurement order — PNs freeze at inquire-for-release

## Board (SMT) — from `../fab/BOM.csv`

| Ref | Qty | Value | Role |
|-----|-----|-------|------|
| U1 | 1 | RP2040 | Passive logger MCU stub |
| U2 | 1 | IMU | Attitude/accel log stub |
| U3 | 1 | RADIO | Telemetry stub |
| J1 | 1 | PinHeader 1×03 | Drogue recovery channel stub |
| J2 | 1 | PinHeader 1×03 | Main chute recovery channel stub |
| J3 | 1 | PinHeader 1×03 | Buzzer / locator stub |
| J4 | 1 | PinHeader 1×03 | SAFE LED stub |
| H1–H4 | 4 | M3 hole | Board mounting |

## Mechanical / study article

| ID | Qty | Item | Source |
|----|-----|------|--------|
| MECH-AF-STL | 1 | `airframe_study.stl` print (body + fins + ghosts) | `../mechanical/` |
| MECH-SCAD | 1 | `airframe_study.scad` parametric source | `../shell/` |
| MECH-FAST-M3 | lot | M3 hardware for logger tray | study |
| MECH-TRAY | 1 | Logger-board tray / bay stub | `structural.yaml` |
| MECH-MOTOR-MT | 1 | Motor-mount / centering-ring study | certified hobby motor class only |
| MECH-RECOVERY | 1 | Drogue/main recovery packaging stubs | non-guided |

## Electrical harness (study)

| ID | Qty | Item | Notes |
|----|-----|------|-------|
| HAR-DROGUE | 1 | Recovery channel lead | J1 — deployment sense/drive stub only |
| HAR-MAIN | 1 | Recovery channel lead | J2 — no guidance |
| HAR-BUZ | 1 | Locator lead | J3 |
| HAR-SAFE | 1 | SAFE LED lead | J4 |
| HAR-PWR | 1 | Battery / GND stub | Bench or flight pack per hobby rules |

## Out of BOM (explicit)

Guidance computers, steering actuators, seekers, warheads, fuzing, ballistic-missile / RV content, homemade propellant.
