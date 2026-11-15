# Fly-by-Wire Architecture — ISM-FJ-1

## Redundancy
- **Quadruplex FCC** (four lanes) as baseline; triplex acceptable only with strong analytical justification (**product decision**).
- Dissimilar software lanes optional for Block 2; Block 1 same-code with physical separation of ISM-Bus A/B and power feeds.
- Sensors: redundant air-data, dual/tri IMU, dual AOA/sideslip probes where fitted.

## Stick / throttle → surface path

```
[Side-stick] --sensors--> [FCC lanes] --vote--> [surface commands]
[Throttle quadrant] ------^                 |
[Pedals] -----------------^                 v
                                      [EHA controllers]
                                            |
                                      [Aileron / HT / Rudder / Flaperon]
```

- HOTAS inceptors are electrical only (force sensors / RVDTs).
- Bay PCB (`kicad/`) provides a **development and study-model** PWM path paralleling the same logical channels; flight article uses FCC→EHA digital links as primary.
- Autopilot / auto-throttle are FCC application modes, not separate boxes (MC may request modes).

## Voting & monitors
- Mid-value select or weighted vote among lanes.
- Actuator model comparison for hardover detection.
- Frame counters and cross-channel data links between lanes.

## Ground vs flight
WOW + airspeed validity switch control laws (see `control-laws.md`). Nose-wheel steering engaged on ground.
