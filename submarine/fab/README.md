# Fab package — ISM Submarine scale-model control (#44)

| File | Use |
|------|-----|
| `ism-submarine-control-gerbers.zip` | Study Gerber + Excellon upload package |
| `ism-submarine-control-cpl.csv` | Centroid / pick-and-place |
| `BOM.csv` | SMT BOM stub (educational) |

## Scope limits (hard)

- Scale-model control board only
- Sonar = **not** on this board (mass/footprint elsewhere)
- **No** quieting, acoustics, weapons, seekers, guidance, warheads, or fuzing
- **Not** a production fab release — study Gerbers for CI/fab-diff practice

## Regenerate

```bash
PCB=submarine/kicad/ism-submarine-control.kicad_pcb
mkdir -p submarine/fab/gerbers_tmp
kicad-cli pcb export gerbers -o submarine/fab/gerbers_tmp/ \
  -l F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste "$PCB"
kicad-cli pcb export drill -o submarine/fab/gerbers_tmp/ --format excellon --excellon-units mm "$PCB"
(cd submarine/fab/gerbers_tmp && zip -q ../ism-submarine-control-gerbers.zip *)
rm -rf submarine/fab/gerbers_tmp
kicad-cli pcb export pos -o submarine/fab/ism-submarine-control-cpl.csv \
  --format csv --units mm --side both "$PCB"
```
