# Bay PCB Placement — ISM-FJ-1 (#75)

**Board:** `../kicad/ism-fighter-jet.*` · outline ~120×80 mm study · four M3 bosses (`bay-layouts.md` slot F)

## Placement zones (top view, USB aft)

| Zone | Contents |
|------|----------|
| Forward-left | MCU (RP2040-class) + crystal + decoupling |
| Forward-right | 28 V → 5 V / 3V3 power tree (LDO/buck), `J_PWR` |
| Mid-left | IMU footprint (I2C) |
| Mid-right | Radio module (SPI) + RF keep-out toward board edge |
| Aft edge | J1–J4 actuation headers, spaced for harness boots |
| Aft-center | USB-C/UART debug (`ISM-Bay-Debug`) |

## Routing intent
1. Power entry at `J_PWR` opposite digital/USB.
2. Actuation returns star to header GND — not shared with MCU digital GND plane stitch except at single filter point.
3. RF keep-out: no high-speed under radio antenna pad.
4. IMU away from PWM edges / DC-DC switch node.

## Multi-board justification
FCC and MC are **separate LRUs** (slots B/A). Crowding flight-critical processors onto the bay I/O board would couple HIL debug faults into laws — rejected. Bay PCB remains I/O concentrator + study path for #84 bring-up and #80 HIL.
