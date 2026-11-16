# ISM Macro Pad

USB 4×4 macro pad — RP2040 module, USB-C, MX hot-swap sockets, diode matrix.
Original International Squirrel Machines design (not QMK).

Generate KiCad + fab: `python3 scripts/build_macro_pad.py`  
Target: **ERC 0 errors**, **DRC 0 errors**.

## Layout

| Block | Notes |
|-------|--------|
| MCU | `ISM_RP2040_Module` (pads 2–5 = ROW0–3, 7–10 = COL0–3) |
| USB | GCT USB4105-class USB-C + USBLC6-2SC6 ESD |
| Matrix | 16× MX hot-swap + 1N4148W diodes |
| PCB | ~148 × 220 mm, 4-layer (ROW In1 / COL In2 + blind vias) |

## Fab ordering

1. `python3 scripts/build_macro_pad.py`
2. Upload `fab/ism-macropad-gerbers.zip`
3. SMT: `fab/ism-macropad-cpl.csv` + `fab/BOM.csv`
4. `cd shell && ./export.sh` — print STLs

### Off-board BOM

- 16× MX switches + keycaps
- M2×6 screws (4×)
- USB-C cable

## Assembly

1. SMT: diodes, passives, ESD, LED, reset.
2. THT/hotswap: MX sockets, USB-C, RP2040 module.
3. Seat PCB on shell posts; screw M2; fit plate + top frame.

## Flash

```bash
cd macro-pad/firmware
mkdir -p build && cd build
cmake .. && make -j
# Hold BOOT, plug USB-C, copy ism_macropad.uf2 to RPI-RP2
```

VID/PID: **0x1209 / 0x000A**. Default map: F1–F16.

## Steve interface

### USB

| Item | Value |
|------|-------|
| Class | HID boot keyboard |
| VID/PID | `0x1209` / `0x000A` |
| Product | `ISM Macro Pad` |

### GPIO (module pads → GPIO)

| Signal | Pad | GPIO |
|--------|-----|------|
| ROW0–3 | 2–5 | GP0–3 |
| COL0–3 | 7–10 | GP5–8 |

### Power

- VBUS 5 V → module LDO → +3V3. USB-C CC 5.1 kΩ to GND.

## Related

- [#9](https://github.com/squirelworks/international-squirrel-machines/issues/9)
- Sibling keyboards under `keyboard/`
