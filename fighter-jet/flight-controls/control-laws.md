# Control Laws (Design Level) — ISM-FJ-1

Not coded here — architecture for future Squirrel-OS/2 flight software partitions.

## Axes & effectors
| Axis | Primary effectors | Secondary / blend |
|------|-------------------|-------------------|
| Pitch | All-moving HT | Flaperon (limited) |
| Roll | Ailerons | Differential flaperon; differential thrust stub |
| Yaw | Rudder | Differential thrust; aileron-rudder interconnect |
| Speed | Throttles / nozzles | Speedbrake stub (Block 2) |

## Modes
1. **Powered approach** — higher gains, AOA emphasis, gentle pitch response.
2. **Up-and-away / combat** — pitch-rate / Nz command blended with AOA limit.
3. **Direct (degraded)** — reduced augmentation if sensors lost; still FBW, not mechanical.
4. **Ground** — NWS, restricted surface rates, thrust idle logic.

## Gains & scheduling
Schedule on dynamic pressure, Mach (when available), gear, flap, stores config. Stores config from MC via ISM-Bus.

## Carefree handling intent
Pilot commands stay inside envelope protections (`envelope.md`); FCC rejects or shapes commands that would exceed AOA, Nz, or roll-rate limits.
