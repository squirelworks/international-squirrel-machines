# Fab package — ISM Hypersonic Bomber thermal board (#37)

| File | Use |
|------|-----|
| `ism-hb-thermal-gerbers.zip` | Study Gerber + Excellon upload package |
| `ism-hb-thermal-cpl.csv` | Centroid / pick-and-place |
| `BOM.csv` | SMT BOM stub (educational) |

## Out of scope (hard)

- **No** weapons, munitions, guidance, seekers, warheads, fuzing, or arming
- **No** scramjet / propulsion design recipes
- **No** ITAR/EAR TPS formulations
- **Not** a production fab release — study Gerbers for CI/fab-diff practice

## Regenerate

```bash
PCB=hypersonic-bomber/kicad/ism-hb-thermal.kicad_pcb
mkdir -p hypersonic-bomber/fab/gerbers_tmp
kicad-cli pcb export gerbers -o hypersonic-bomber/fab/gerbers_tmp/ \
  -l F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste "$PCB"
kicad-cli pcb export drill -o hypersonic-bomber/fab/gerbers_tmp/ --format excellon --excellon-units mm "$PCB"
(cd hypersonic-bomber/fab/gerbers_tmp && zip -q ../ism-hb-thermal-gerbers.zip *)
rm -rf hypersonic-bomber/fab/gerbers_tmp
kicad-cli pcb export pos -o hypersonic-bomber/fab/ism-hb-thermal-cpl.csv \
  --format csv --units mm --side both "$PCB"
```
