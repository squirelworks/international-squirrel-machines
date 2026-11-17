# Satellite — educational master BOM (#31)

**Product:** ISM-SAT-1  
**Slice:** study BOM tying the bus-board fab package to the 3U bus STL / structural stubs.

## Scope / weapons boundary (hard)

- Civilian / educational bus + payload packaging only
- Payload = **mass / power / data** stubs only
- **No** weapons, seekers, guidance-to-target, warheads, or fuzing
- **No** ITAR/EAR bus or payload designs
- **Not** a procurement order — PNs freeze at inquire-for-release

## Board (SMT) — from `../fab/BOM.csv`

| Ref | Qty | Value | Role |
|-----|-----|-------|------|
| U1 | 1 | RP2040 | OBC / bus MCU stub |
| U2 | 1 | IMU | ADCS sense stub |
| U3 | 1 | RADIO | Comms stub |
| J1 | 1 | PinHeader 1×03 | EPS / power rail stub |
| J2 | 1 | PinHeader 1×03 | Radio harness stub |
| J3 | 1 | PinHeader 1×03 | Magnetorquer drive stub |
| J4 | 1 | PinHeader 1×03 | Payload enable stub (mass/power/data only) |
| H1–H4 | 4 | M3 hole | Board mounting |

## Mechanical / study article

| ID | Qty | Item | Source |
|----|-----|------|--------|
| MECH-BUS-STL | 1 | `bus_study.stl` print (3U rails / trays ghosts) | `../mechanical/` |
| MECH-SCAD | 1 | `bus_study.scad` parametric source | `../shell/` |
| MECH-FAST-M3 | lot | M3 hardware for board tray | study |
| MECH-TRAY | 1 | Bus-board tray stub | `structural.yaml` |
| PAY-STUB | 1 | Payload mass/power/data placeholder | `payload-placeholders.yaml` |

## Electrical harness (study)

| ID | Qty | Item | Notes |
|----|-----|------|-------|
| HAR-EPS | 1 | Power/telemetry lead | J1 |
| HAR-RADIO | 1 | UART/radio lead | J2 |
| HAR-MTQ | 1 | Magnetorquer drive lead | J3 — coarse ADCS only |
| HAR-PL | 1 | Payload enable lead | J4 — no weapons payload |
| HAR-PWR | 1 | Bench / EPS stub | Current-limited |

## Out of BOM (explicit)

Weapons payloads, seekers, guidance-to-target kits, warheads, fuzing/arming hardware, ITAR/EAR bus designs.
