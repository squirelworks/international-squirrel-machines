# ISM Keyboard — 75%

Compact ANSI 75% (6×14 matrix, 84 keys), RP2040 module carrier with **ROW5 on pad 27**, USB-C, MX hotswap, printable shell.
Original International Squirrel Machines design (not QMK).

Generate: `python3 scripts/build_keyboard_75.py`  
Target: **ERC 0 / DRC 0** (`kicad-cli … --severity-error`).

## Layout

| Block | Notes |
|-------|--------|
| MCU | `ISM_RP2040_Module` — pads 1–26 as 60%/65%; **pad 27 = ROW5**, pad 28 = COL14 (reserved) |
| Matrix | 84× MX hotswap + 1N4148W; ROW0–5 × COL0–13 |
| Routing | ROW In1.Cu, COL In2.Cu, blind vias |

## Fab

1. `python3 scripts/build_keyboard_75.py`
2. Upload `fab/ism-keyboard-75-gerbers.zip`
3. SMT: `fab/ism-keyboard-75-cpl.csv` + `fab/BOM.csv`
4. `cd shell && ./export.sh`

## Flash

VID/PID **0x1209 / 0x0003**. Product string `ISM Keyboard 75%`.

## Steve interfaces

Same USB HID boot keyboard as 60%/65%. Matrix: ROW0–4 on module pads 2–6 (GP0–4); **ROW5 on pad 27 (GP19)**; COL0–13 on pads 7–13, 19–25 (GP5–18).

## Related

- [#63](https://github.com/squirelworks/international-squirrel-machines/issues/63)
- Sibling: `keyboard/65-percent/` (PR #133), `keyboard/60-percent/` (#128)
