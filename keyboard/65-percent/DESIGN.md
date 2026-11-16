# ISM 65% Keyboard

ANSI 65% — 60% block + right nav cluster (DEL / PGUP / PGDN / HOME / END / arrows).
RP2040 module carrier, USB-C, MX hotswap, 5×14 matrix fully populated (70 keys).

## Electrical

- Matrix: ROW0–4 × COL0–13 (all 70 intersections used)
- Diode per key: 1N4148W SOD-123, cathode on COL
- MCU: `ISM_RP2040_Module` (2.54 mm pitch)
- USB-C + USBLC6-2SC6 + CC 5.1 kΩ
- Nav keys reuse the nine intersections left open on the 60% layout; some electrical rows differ from physical rows (ROW stubs fan per-key on In1)

## PCB

- 4-layer: F.Cu, In1.Cu (ROW), In2.Cu (COL), B.Cu (USB/power)
- Blind vias F↔In1 / F↔In2
- Generator: `scripts/build_keyboard_65.py`
- Lib tables: project-local → `common/kicad` + KiCad 8 stock

## Verification

```bash
kicad-cli sch erc --severity-error --exit-code-violations -o kicad/erc.rpt kicad/ism-keyboard-65.kicad_sch
kicad-cli pcb drc --severity-error --exit-code-violations -o kicad/drc.rpt kicad/ism-keyboard-65.kicad_pcb
```

Fab readiness: `fab/` gerber+drill zip, `BOM.csv` (LCSC), CPL, shell STL/STEP.
