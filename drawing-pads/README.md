# ISM Drawing Pads

Range of USB digitizer / graphics tablets — small, medium, large.
Original International Squirrel Machines design.

Generate all sizes: `python3 scripts/build_drawing_pads.py` — **ERC 0 / DRC 0** each.

| Size | Active area | PCB |
|------|-------------|-----|
| `small/` | 80 × 50 mm | 100 × 75 mm |
| `medium/` | 120 × 75 mm | 150 × 105 mm |
| `large/` | 180 × 110 mm | 220 × 150 mm |

## Fab ordering (per size)

1. `python3 scripts/build_drawing_pads.py`
2. Upload `drawing-pads/<size>/fab/ism-drawing-pad-<size>-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd drawing-pads/<size>/shell && ./export.sh`

### Off-board BOM

- Resistive overlay film matched to active area
- Stylus (passive)
- M2 screws (4×)
- USB-C cable

## Assembly

1. SMT controller section; fit RP2040 module + USB-C.
2. Attach 4-wire touch FPC/overlay to `U3`.
3. Seat PCB in shell; fit top with active window; clip stylus holder.

## Flash

```bash
cd drawing-pads/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_drawing_pad.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x000D**. HID mouse report as digitizer bring-up stand-in.

## Steve interface

| Signal | Module pad | GPIO |
|--------|------------|------|
| TOUCH_XL/XR/YU/YD | 2–5 | GP0–3 |
| BTN_L / BTN_R | 7–8 | GP5–6 |
| USB | 16–17 | DM/DP |

## Related

- [#2](https://github.com/squirelworks/international-squirrel-machines/issues/2)
