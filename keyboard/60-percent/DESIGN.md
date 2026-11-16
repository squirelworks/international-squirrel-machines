# ISM 60% Keyboard

ANSI 60%, RP2040 module carrier, USB-C, MX hotswap electrical pads, 5×14 matrix.

## Electrical

- Matrix: ROW0–4 × COL0–13 (61 keys; unused intersections open)
- Diode per key: 1N4148W SOD-123, cathode on COL
- MCU: `ISM_RP2040_Module` (2.54 mm pitch) for fan-in
- USB-C + USBLC6-2SC6 + CC 5.1 kΩ

## PCB

- 4-layer: F.Cu, In1.Cu (ROW buses), In2.Cu (COL spines), B.Cu (USB/power)
- Blind vias F↔In1 / F↔In2 (no through-vias shorting inners)
- Generator: `scripts/build_keyboard_final.py`
- Lib tables: project-local → `common/kicad` + KiCad 8 stock

## Verification

```bash
kicad-cli sch erc --severity-error --exit-code-violations -o kicad/erc.rpt kicad/ism-keyboard-60.kicad_sch
kicad-cli pcb drc --severity-error --exit-code-violations -o kicad/drc.rpt kicad/ism-keyboard-60.kicad_pcb
```

Fab readiness: `fab/` gerber+drill zip, `BOM.csv` (LCSC), CPL, shell STL/STEP.
