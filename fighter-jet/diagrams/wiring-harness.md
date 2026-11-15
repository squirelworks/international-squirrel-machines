# Wiring & Harness Overview — ISM-FJ-1

Conceptual trunks only. Pinouts freeze when bay PCB connector ICD lands.

## Trunk map

```
                    [Generators / Batteries]
                              |
                         (P) Power backbone 28 V / 270 V HVDC stub
                              |
         +--------------------+--------------------+
         |                    |                    |
    [PDU / Bay PCB]      [FCC lanes]          [MC / Sensors]
         |                    |                    |
    (A) Actuation        (D) Data bus         (S) Sensor feeds
    EHA / servo PWM      ISM-Bus / backup     radar, EO, IMU
         |                    |                    |
    [Surfaces]           [HUD / LAD / HOTAS]  [Stores safe/arm]
```

## Harness families

| Code | Name | From → To | Notes |
|------|------|-----------|-------|
| P1 | Primary DC | Generators → PDU | Dual-feed, cross-tie |
| P2 | Essential bus | PDU → FCC / MC / IMU | Battery-backed |
| A1–A4 | Actuation | Bay PCB / FCC → aileron, elevator, rudder, throttle/nozzle | Shielded; separate returns |
| D1 | ISM-Bus A | MC ↔ FCC ↔ radios | Dual redundant |
| D2 | ISM-Bus B | Backup path, dissimilar physical route | Opposite side of fuselage |
| S1 | Radar/EO | Nose bay → MC | High-speed fiber stub preferred |
| S2 | IMU | Isolated tray → FCC & MC | Short, quiet harness |
| W1 | Stores | MC → pylons | Safe/arm discrete + serial |
| G1 | Bonding | Structure throughout | Corrosion-aware jumpers |

## Bay PCB role (`kicad/`)
The current KiCad board is the **local I/O concentrator** in the avionics bay: MCU, IMU footprint, radio, and PWM/servo headers (J1–J4). In the full program those headers map to A1–A4 command paths (or to EHA motor drives via intermediate amplifiers — see `hydraulics/`).

## Routing rules (design intent)
1. Power and data on opposite sides of the tunnel where practical.
2. Actuation returns never shared with digital 0 V at FCC.
3. No single connector failure kills more than one FCC lane.
4. Field replaceable harness segments at FS-42 and FS-72 splices.

## Still stubbed
- Exact connector series and pin maps
- Fiber vs copper for S1
- HVDC for future electric actuation growth
