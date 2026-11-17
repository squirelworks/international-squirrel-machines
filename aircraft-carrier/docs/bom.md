# Aircraft carrier — educational master BOM (#45)

**Product:** ISM-CV-1  
**Slice:** study BOM tying the scale-model deck-control fab package to the deck STL / structural stubs.

## Scope limits (hard)

- Scale-model / educational packaging only
- Weapons / combat sensors / aviation ordnance = **mass / footprint / KG** placeholders only
- Catapult / arresting = **load / mass / keep-out** stubs — no classified plant design
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- **No** ITAR/EAR combat data
- **Not** a procurement order — PNs freeze at inquire-for-release

## Board (SMT) — from `../fab/BOM.csv`

| Ref | Qty | Value | Role |
|-----|-----|-------|------|
| U1 | 1 | RP2040 | Scale-model MCU stub |
| U2 | 1 | IMU | Attitude stub |
| U3 | 1 | RADIO | Telemetry stub |
| J1 | 1 | PinHeader 1×03 | Elevator PWM stub |
| J2 | 1 | PinHeader 1×03 | Catapult load/keep-out stub |
| J3 | 1 | PinHeader 1×03 | Arresting gear load stub |
| J4 | 1 | PinHeader 1×03 | Rudder PWM stub |
| H1–H4 | 4 | M3 hole | Board mounting |

## Mechanical / study article

| ID | Qty | Item | Source |
|----|-----|------|--------|
| MECH-DECK-STL | 1 | `deck_study.stl` print (deck + island + ghosts) | `../mechanical/` |
| MECH-SCAD | 1 | `deck_study.scad` parametric source | `../shell/` |
| MECH-FAST-M3 | lot | M3 hardware for deck-board tray | study |
| MECH-TRAY | 1 | Deck-control board tray stub | `structural.yaml` |
| MASS-WPN | lot | Inert combat mass boxes | `mass-placeholders.yaml` |
| MASS-ORD | lot | Inert aviation-ordnance mass boxes | `aviation.yaml` |

## Electrical harness (study)

| ID | Qty | Item | Notes |
|----|-----|------|-------|
| HAR-ELEV | 1 | 3-pin PWM lead | J1 elevator stub |
| HAR-CAT | 1 | 3-pin lead | J2 catapult load/keep-out stub — not classified plant |
| HAR-ARR | 1 | 3-pin lead | J3 arresting load stub |
| HAR-RUD | 1 | 3-pin PWM lead | J4 rudder stub |
| HAR-PWR | 1 | 5 V / GND stub lead | Bench supply only |

## Out of BOM (explicit)

Weapons fire-control LRUs, seekers, guidance kits, warheads, fuzing/arming hardware, classified catapult plant designs.
