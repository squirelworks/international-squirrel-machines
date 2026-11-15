# Buses & Power — ISM-FJ-1

## Data buses
| Bus | Use | Notes |
|-----|-----|-------|
| ISM-Bus A | Primary vehicle network | Dual-redundant physical where practical |
| ISM-Bus B | Dissimilar route backup | Opposite fuselage side |
| Sensor fabric | Radar/EO → MC | Fiber stub preferred |
| FCC cross-channel | Lane sync | Deterministic, short period |
| Maintenance | Ground only | Gated by WOW / maintenance pin |

Protocol details are ISM-original; do not copy proprietary military bus specs into this tree. Contemporaries may be studied as reference only.

## Power
| Bus | Voltage | Feeds |
|-----|---------|-------|
| Primary DC | 28 V | General avionics, EHAs (via converters) |
| Essential DC | 28 V battery-backed | FCC, IMU, essential HUD, radios |
| HVDC stub | ~270 V (optional) | Future electric actuation growth |
| AC stub | If generators require | Conversion at PDU |

PDU in bay slot C; generators on engines; battery in protected bay. Cross-tie logic prevents single generator loss from dropping essential bus.

## Bay PCB relationship
`kicad/` board hangs on essential/primary as appropriate for study; production pinout must match `diagrams/wiring-harness.md` families P2 and A1–A4.
