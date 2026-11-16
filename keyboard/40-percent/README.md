# ISM Keyboard — 40%

Ortholinear 4×12 (48 keys), RP2040 module, USB-C, MX hotswap, printable shell.
Original International Squirrel Machines design (not QMK).

Generate: `python3 scripts/build_keyboard_40.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| MCU | `ISM_RP2040_Module` — ROW0–3 on pads 2–5; COL0–11 on pads 7–13, 19–23 |
| Matrix | 48× MX hotswap + 1N4148W |
| Routing | ROW In1.Cu, COL In2.Cu, blind vias |

## Fab

1. `python3 scripts/build_keyboard_40.py`
2. Upload `fab/ism-keyboard-40-gerbers.zip`
3. SMT: `fab/ism-keyboard-40-cpl.csv` + `fab/BOM.csv`
4. `cd shell && ./export.sh`

## Flash

VID/PID **0x1209 / 0x0006**. Product string `ISM Keyboard 40%`.

## Steve interfaces

USB HID boot keyboard. Matrix: ROW0–3 → GP0–3; COL0–11 → GP5–16.

## Related

- [#60](https://github.com/squirelworks/international-squirrel-machines/issues/60)
- Sibling: `keyboard/full-size/` (#141), `keyboard/60-percent/` (#128)
