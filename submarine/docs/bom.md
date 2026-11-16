# Submarine — educational master BOM (#44)

**Product:** ISM-SS-1  
**Slice:** study BOM tying the control-board fab package to the hull STL / structural stubs.

## Scope limits (hard) — B3 spirit

- Scale-model / educational packaging only
- Sonar and sensors = **mass / footprint** placeholders (see `../interfaces/mass-placeholders.yaml`)
- **No** quieting, acoustic processing, life-support design
- **No** weapons, seekers, guidance, warheads, or fuzing
- **No** ITAR/EAR content
- **Not** a procurement order — PNs freeze at inquire-for-release

## Board (SMT) — from `../fab/BOM.csv`

| Ref | Qty | Value | Role |
|-----|-----|-------|------|
| U1 | 1 | RP2040 | Scale-model MCU stub |
| U2 | 1 | IMU | Attitude / trim stub |
| U3 | 1 | RADIO | Telemetry stub |
| J1–J4 | 4 | PinHeader 1×03 | Propulsor / stern / rudder / ballast PWM stubs |
| H1–H4 | 4 | M3 hole | Board mounting |

## Mechanical / study article

| ID | Qty | Item | Source |
|----|-----|------|--------|
| MECH-HULL-STL | 1 | `hull_study.stl` print (ghost hull / rings / casing) | `../mechanical/` |
| MECH-SCAD | 1 | `hull_study.scad` parametric source | `../shell/` |
| MECH-FAST-M3 | lot | M3 hardware for board tray | study |
| MECH-TRAY | 1 | Control-board tray stub (print or laser) | `structural.yaml` tray member |
| MASS-SONAR-BOW | 1 | Bow sensor mass box (inert) | `mass-placeholders.yaml` |
| MASS-SONAR-FLANK | 1 | Flank sensor mass box (inert) | `mass-placeholders.yaml` |

## Electrical harness (study)

| ID | Qty | Item | Notes |
|----|-----|------|-------|
| HAR-PWM | 4 | 3-pin PWM leads | J1–J4 to scale actuators |
| HAR-PWR | 1 | 5 V / GND stub lead | Bench supply only |

## Out of BOM (explicit)

Weapons, quieting treatments, acoustic arrays with signal processing, life-support plumbing, certified pressure-hull materials.
