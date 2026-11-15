# Mission Computer — ISM-FJ-1

## Role
The mission computer (MC) owns sensor fusion for *mission* functions (radar/EO tracks, stores management, data-link, navigation display), while the FCC owns flight-critical control laws. Clear partition: **MC may request modes; FCC arbitrates flight safety.**

## Hardware intent
- Dual-lane MC (active / standby or dual-active with vote on non-critical outputs).
- Cold-plate capable LRU in avionics bay slot A (`diagrams/bay-layouts.md`).
- Boot from ISM read-only media + updatable mission data partition.

## Interfaces
| Interface | Peers |
|-----------|-------|
| ISM-Bus A/B | FCC, radios, HUD symbol generator, stores |
| High-speed sensor link | Radar / EO processors |
| Maintenance port | Ground data load |
| Time sync | IMU / GNSS |

## Failure
MC loss → FCC continues flying; pilot retains basic attitude/HUD from FCC essential symbols; weapons safe.
