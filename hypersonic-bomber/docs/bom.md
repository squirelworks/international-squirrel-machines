# Hypersonic bomber — educational master BOM (#37)

**Product:** ISM-HB-1  
**Slice:** study BOM tying the thermal/TPS-sense fab package to the blunt-cone STL / structural stubs.

## Out of scope (hard)

- Weapons, munitions, guidance, seekers, warheads, fuzing, or arming
- Operational employment, targeting, or mission planning
- Scramjet / propulsion **design recipes** or performance prediction
- Export-controlled (ITAR/EAR) TPS formulations or classified materials data
- **Not** a procurement order — PNs freeze at inquire-for-release

## Board (SMT) — from `../fab/BOM.csv`

| Ref | Qty | Value | Role |
|-----|-----|-------|------|
| U1 | 1 | RP2040 | Thermal / TPS sense MCU stub |
| U2 | 1 | IMU | Attitude stub |
| U3 | 1 | RADIO | Telemetry stub |
| J1 | 1 | PinHeader 1×03 | TPS thermistor / TC sense stub |
| J2 | 1 | PinHeader 1×03 | Heat-flux sense stub |
| J3 | 1 | PinHeader 1×03 | TPS health / spare thermal stub |
| J4 | 1 | PinHeader 1×03 | Over-temp packaging stub |
| H1–H4 | 4 | M3 hole | Board mounting |

## Mechanical / study article

| ID | Qty | Item | Source |
|----|-----|------|--------|
| MECH-CONE-STL | 1 | `blunt_cone_study.stl` print (blunt cone + TPS shell ghosts) | `../mechanical/` |
| MECH-SCAD | 1 | `blunt_cone_study.scad` parametric source | `../shell/` |
| MECH-FAST-M3 | lot | M3 hardware for thermal board tray | study |
| MECH-TRAY | 1 | Thermal-board tray stub under TPS shell | `structural.yaml` |
| TPS-CLASS | ref | Textbook TPS class coupon placeholders | `heat-shield-tps.md` — open literature classes only |

## Electrical harness (study)

| ID | Qty | Item | Notes |
|----|-----|------|-------|
| HAR-TC1 | 1 | Sense lead | J1 teaching thermistor/TC stub |
| HAR-FLUX | 1 | Sense lead | J2 heat-flux stub |
| HAR-TPS | 1 | Status lead | J3 TPS_OK packaging stub |
| HAR-OT | 1 | Status lead | J4 over-temp packaging stub — not a weapon inhibit |
| HAR-PWR | 1 | 5 V / GND stub lead | Bench supply only |

## Out of BOM (explicit)

Weapons, seekers, guidance, munition propulsion, warheads, fuzing/arming, classified TPS recipes, scramjet design kits.
