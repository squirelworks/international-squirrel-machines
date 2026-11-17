# Warship — educational master BOM (#43)

**Product:** ISM-WS-1  
**Slice:** study BOM tying the scale-model control fab package to the hull STL / structural stubs.

## Scope limits (hard)

- Scale-model / educational packaging only
- Weapons and combat sensors = **mass / footprint** placeholders only (`../interfaces/mass-placeholders.yaml`)
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- **No** ITAR/EAR content
- **Not** a procurement order — PNs freeze at inquire-for-release

## Board (SMT) — from `../fab/BOM.csv`

| Ref | Qty | Value | Role |
|-----|-----|-------|------|
| U1 | 1 | RP2040 | Scale-model MCU stub |
| U2 | 1 | IMU | Attitude stub |
| U3 | 1 | RADIO | Telemetry stub |
| J1 | 1 | PinHeader 1×03 | Port thruster PWM stub |
| J2 | 1 | PinHeader 1×03 | Stbd thruster PWM stub |
| J3 | 1 | PinHeader 1×03 | Rudder PWM stub |
| J4 | 1 | PinHeader 1×03 | Ballast/trim PWM stub |
| H1–H4 | 4 | M3 hole | Board mounting |

## Mechanical / study article

| ID | Qty | Item | Source |
|----|-----|------|--------|
| MECH-HULL-STL | 1 | `hull_study.stl` print (hull + ghost structure) | `../mechanical/` |
| MECH-SCAD | 1 | `hull_study.scad` parametric source | `../shell/` |
| MECH-FAST-M3 | lot | M3 hardware for control-board tray | study |
| MECH-TRAY | 1 | Control-board tray stub | `structural.yaml` |
| MASS-WPN | lot | Inert weapons mass boxes | `mass-placeholders.yaml` |
| MASS-SENS | lot | Inert combat-sensor mass boxes | `mass-placeholders.yaml` |

## Electrical harness (study)

| ID | Qty | Item | Notes |
|----|-----|------|-------|
| HAR-PORT | 1 | 3-pin PWM lead | J1 port thruster stub |
| HAR-STBD | 1 | 3-pin PWM lead | J2 stbd thruster stub |
| HAR-RUD | 1 | 3-pin PWM lead | J3 rudder stub |
| HAR-BAL | 1 | 3-pin PWM lead | J4 ballast/trim stub |
| HAR-PWR | 1 | 5 V / GND stub lead | Bench supply only |

## Out of BOM (explicit)

Weapons fire-control LRUs, seekers, guidance kits, warheads, fuzing/arming hardware, combat-system internals.
