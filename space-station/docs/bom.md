# Space Station — educational master BOM (#42)

**Product:** ISM-SSN-1  
**Slice:** study BOM tying the habitat-board fab package to the module STL / structural stubs.

## Scope / weapons boundary (hard)

- Habitat / civil station architecture only
- Docking / berthing = **mass / volume / power** stubs only
- **No** weapons, seekers, guidance-to-target, warheads, or fuzing
- **No** combat employment or ITAR/EAR station designs
- **Not** a procurement order — PNs freeze at inquire-for-release

## Board (SMT) — from `../fab/BOM.csv`

| Ref | Qty | Value | Role |
|-----|-----|-------|------|
| U1 | 1 | RP2040 | Habitat C&DH MCU stub |
| U2 | 1 | IMU-6DOF | Cabin / attitude sense stub |
| U3 | 1 | RADIO | Comms stub |
| J1 | 1 | PinHeader 1×03 | EPS telemetry stub |
| J2 | 1 | PinHeader 1×03 | ECLSS fan/valve stub |
| J3 | 1 | PinHeader 1×03 | Command/data handling UART stub |
| J4 | 1 | PinHeader 1×03 | Docking sense / umbilical enable (mass/volume/power only) |
| H1–H4 | 4 | M3 hole | Board mounting |

## Mechanical / study article

| ID | Qty | Item | Source |
|----|-----|------|--------|
| MECH-MOD-STL | 1 | `module_study.stl` print (habitat / node / truss / berthing ghosts) | `../mechanical/` |
| MECH-SCAD | 1 | `module_study.scad` parametric source | `../shell/` |
| MECH-FAST-M3 | lot | M3 hardware for board tray | study |
| MECH-TRAY | 1 | Habitat-board tray stub | `structural.yaml` |
| DOCK-STUB | 1 | Berthing mass/volume/power placeholder | `docking-placeholders.yaml` |

## Electrical harness (study)

| ID | Qty | Item | Notes |
|----|-----|------|-------|
| HAR-EPS | 1 | EPS telemetry lead | J1 |
| HAR-ECLSS | 1 | Fan/valve lead | J2 — civil ECLSS only |
| HAR-CDH | 1 | C&DH UART lead | J3 |
| HAR-DOCK | 1 | Docking sense / umbilical enable | J4 — no weapons employment |
| HAR-PWR | 1 | Bench / EPS stub | Current-limited |

## Out of BOM (explicit)

Weapons payloads, seekers, guidance-to-target kits, warheads, fuzing/arming hardware, combat docking adapters, ITAR/EAR station designs.
