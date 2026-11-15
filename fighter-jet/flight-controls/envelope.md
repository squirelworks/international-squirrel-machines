# Flight Envelope Protections — ISM-FJ-1

Design-level protections. Numeric limits TBD with aero database.

## Protections (baseline set)
| Protection | Intent |
|------------|--------|
| AOA limit | Prevent departure / deep stall; cue + hard limit |
| Nz / load factor | Structural & crew limit |
| Roll-rate / yaw-rate | Structural & PIO margin |
| Airspeed / Mach | OverSpeed warning; soft then hard cue |
| Gear / flap placard | Inhibit unsafe configs; WOW interlocks |
| High AOA yaw | Rudder authority manage with sideslip |

## Sensor validity
If air-data or AOA disagree beyond threshold → widen protections toward conservative; declare degraded mode on HUD.

## Stores asymmetry
MC provides stores state; FCC derates roll authority with asymmetric heavy stores.

## Still stubbed
- Exact AOA/Nz numbers
- High-Mach inlet/engine coupling limits
- Spin recovery law (may be Block 2)
