# ISM 75% Keyboard

Compact ANSI 75% with F-row and right nav. 6×14 matrix (84 keys).

## Electrical

- ROW0–5 × COL0–13; diode cathode on COL
- MCU: `ISM_RP2040_Module` with **pad 27 = ROW5** (carrier extension; pad 28 = COL14 reserved)
- USB-C + USBLC6-2SC6 + CC 5.1 kΩ

## PCB

- 4-layer F / In1 (ROW) / In2 (COL) / B
- Generator: `scripts/build_keyboard_75.py`

## Verification

```bash
kicad-cli sch erc --severity-error --exit-code-violations -o kicad/erc.rpt kicad/ism-keyboard-75.kicad_sch
kicad-cli pcb drc --severity-error --exit-code-violations -o kicad/drc.rpt kicad/ism-keyboard-75.kicad_pcb
```
