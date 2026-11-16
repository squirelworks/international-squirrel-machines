# Fly-by-Wire Architecture — ISM-FJ-1 (#74)

**Contracts:** `../interfaces/flight-controls.yaml` · surface cmds ↔ `../interfaces/actuators.yaml`  
**Block diagram:** `fcs-block.svg`

## Redundancy
- **Quadruplex FCC** (four lanes) baseline; triplex only with strong analytical justification (**product decision**).
- Block 1: same-code lanes with physical separation of ISM-Bus A/B and power feeds. Dissimilar software = Block 2 option.
- Sensors: redundant air-data, dual/tri IMU, dual AOA/sideslip where fitted.
- Voting: mid-value select; actuator model comparison for hardover; cross-channel data links; frame counters.
- First iron-bird may run dual-lane hardware with quad software emulation — still FBW topology.

## FCC vs mission computer
| Box | Owns |
|-----|------|
| **FCC** | Inner-loop laws, envelope, voted surface commands, NWS, gear-gated modes, BIT |
| **MC** | Outer mode requests, autopilot targets, **stores_config** to FCC |

MC **never** bypasses FCC to actuators.

## Stick / throttle → surface path

```
[Side-stick] --100 Hz--> [FCC lanes] --vote--> [cmd.surface.*]
[Throttle quadrant] ------^                 |
[Pedals / brakes] --------^                 v
                                      [EHA controllers]  ← actuators.yaml
                                            |
                                      [Aileron / HT / Rudder / Flaperon]
```

- HOTAS inceptors are electrical only (force sensors / RVDTs). ICD ranges/topics in `flight-controls.yaml` → `inceptors_icd`.
- Bay PCB (`kicad/`) = **development / study** PWM path paralleling the same logical channels; flight article uses FCC→EHA digital primary.
- Autopilot / auto-throttle are FCC application modes (MC may request).

## Ground vs flight
WOW + airspeed validity switch laws (`control-laws.md`). NWS on ground only.
