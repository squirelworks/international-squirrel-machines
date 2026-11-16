# ISM Keyboard — Full Size

ANSI full-size (~104 keys) with F-row, nav/arrow cluster, and numpad. 7×15 matrix (ROW0–6 × COL0–14), RP2040 module (pad 27=ROW5, pad 28=COL14, pad 29=ROW6), USB-C, MX hotswap, printable shell.
Original International Squirrel Machines design (not QMK).

Generate: `python3 scripts/build_keyboard_full.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| MCU | `ISM_RP2040_Module` — pads 1–26 as smaller boards; **pad 27=ROW5**, **pad 28=COL14**, **pad 29=ROW6** |
| Matrix | 104× MX hotswap + 1N4148W; ROW0–6 × COL0–14 |
| Routing | ROW In1.Cu, COL In2.Cu, blind vias |

## Fab

1. `python3 scripts/build_keyboard_full.py`
2. Upload `fab/ism-keyboard-full-size-gerbers.zip`
3. SMT: `fab/ism-keyboard-full-size-cpl.csv` + `fab/BOM.csv`
4. `cd shell && ./export.sh`

## Flash

VID/PID **0x1209 / 0x0005**. Product string `ISM Keyboard Full Size`.

## Steve interfaces

USB HID boot keyboard. Matrix: ROW0–4 on module pads 2–6 (GP0–4); **ROW5 on pad 27 (GP19)**; **ROW6 on pad 29 (GP21)**; COL0–13 on pads 7–13, 19–25 (GP5–18); **COL14 on pad 28 (GP20)**.

## Related

- [#65](https://github.com/squirelworks/international-squirrel-machines/issues/65)
- Sibling: `keyboard/tkl/` (#138), `keyboard/75-percent/` (#136)
