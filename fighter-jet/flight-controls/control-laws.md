# Control Laws (Design Level) — ISM-FJ-1 (#74)

Not production-coded here — architecture for Squirrel-OS/2 partitions and Flight Lab models.

## Axes & effectors
| Axis | Primary effectors | Secondary / blend |
|------|-------------------|-------------------|
| Pitch | All-moving HT | Flaperon (limited) |
| Roll | Ailerons | Differential flaperon; differential thrust stub |
| Yaw | Rudder | Differential thrust; aileron-rudder interconnect |
| Speed | Throttles / nozzles | Speedbrake stub (Block 2) |

## Modes (entry / exit)

| Mode | Intent | Entry | Exit |
|------|--------|-------|------|
| **powered_approach** | High gains, AOA emphasis | Gear down or land flap; KEAS in approach band | Gear+flap up, or select up-and-away |
| **up_and_away** | Pitch-rate / Nz blend + AOA limit | Weight off wheels; KEAS above climb-out | Gear down, degraded, or ground |
| **direct_degraded** | Reduced augmentation; still FBW | Sensor disagree / lane loss beyond threshold | Sensors valid + crew reset |
| **ground** | NWS; surface rate ×0.4; thrust idle logic | Any WOW true | All WOW false + KEAS valid |

Authoritative machine-readable copy: `flight-controls.yaml` → `modes`.

## Gains & scheduling
Schedule on dynamic pressure, Mach (when available), gear, flap, stores config (from MC via ISM-Bus).

## Carefree handling
Pilot commands stay inside envelope protections (`envelope.md`); FCC rejects or shapes commands that would exceed AOA, Nz, or roll-rate limits.
