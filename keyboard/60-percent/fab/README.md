# Fab package — ISM Keyboard 60%

| File | Use |
|------|-----|
| `ism-keyboard-60-gerbers.zip` | JLCPCB/PCBWay upload (4-layer + Excellon, incl. blind-via drills) |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-keyboard-60-cpl.csv` | Centroid / pick-and-place |

Regenerate with:

```bash
python3 scripts/build_keyboard_final.py
```

Stackup: F.Cu / In1.Cu (ROW) / In2.Cu (COL) / B.Cu. Target ERC/DRC: `kicad-cli … --severity-error --exit-code-violations` → 0.
