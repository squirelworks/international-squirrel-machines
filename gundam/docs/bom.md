# Gundam — educational master BOM (#46)

**Product:** ISM-MS-1  
**Slice:** study BOM tying the control-board fab package to the frame STL / structural stubs.

## Scope / weapons boundary (hard)

- Mecha frame / actuator packaging only
- Stores / hardpoints = **mass, footprint, SAFE/INHIBIT** stubs only
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming codes
- **No** live launch / fire sequences or engagement doctrine
- **No** ITAR/EAR weapon or fire-control designs
- **Not** a procurement order — PNs freeze at inquire-for-release

## Board (SMT) — from `../fab/BOM.csv`

| Ref | Qty | Value | Role |
|-----|-----|-------|------|
| U1 | 1 | RP2040 | Mecha control MCU stub |
| U2 | 1 | IMU-6DOF | Joint / attitude sense stub |
| U3 | 1 | RADIO | Telemetry stub |
| J1 | 1 | PinHeader 1×03 | Leg actuator PWM stub |
| J2 | 1 | PinHeader 1×03 | Arm actuator PWM stub |
| J3 | 1 | PinHeader 1×03 | Stores SAFE discrete stub |
| J4 | 1 | PinHeader 1×03 | Stores INHIBIT discrete stub |
| H1–H4 | 4 | M3 hole | Board mounting |

## Mechanical / study article

| ID | Qty | Item | Source |
|----|-----|------|--------|
| MECH-FRAME-STL | 1 | `frame_study.stl` print (torso / limb / inert-stores ghosts) | `../mechanical/` |
| MECH-SCAD | 1 | `frame_study.scad` parametric source | `../shell/` |
| MECH-FAST-M3 | lot | M3 hardware for board tray | study |
| MECH-TRAY | 1 | Control-board tray stub | `structural.yaml` |
| STORES-STUB | 1 | Hardpoint mass/footprint + SAFE/INHIBIT placeholder | `stores-placeholders.yaml` |

## Electrical harness (study)

| ID | Qty | Item | Notes |
|----|-----|------|-------|
| HAR-LEG | 1 | Leg actuator PWM lead | J1 |
| HAR-ARM | 1 | Arm actuator PWM lead | J2 |
| HAR-SAFE | 1 | Stores SAFE discrete | J3 — SAFE only |
| HAR-INH | 1 | Stores INHIBIT discrete | J4 — INHIBIT only; no arming |
| HAR-PWR | 1 | Bench / EPS stub | Current-limited |

## Out of BOM (explicit)

Seekers, guidance kits, munition propulsion, warheads, fuzing/arming hardware, live launch/fire sequence gear, ITAR/EAR weapon or fire-control designs.
