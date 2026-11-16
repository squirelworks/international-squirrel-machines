# Fab package — ISM Rocket logger board (#41)

| File | Use |
|------|-----|
| `ism-rocket-logger-gerbers.zip` | Study Gerber + Excellon upload package |
| `ism-rocket-logger-cpl.csv` | Centroid / pick-and-place |
| `BOM.csv` | SMT BOM stub (educational) |

## Scope limits (hard)

- Passive logger / recovery deployment sensing only
- **No** guidance, steering, or active flight control
- **No** ballistic-missile or reentry-vehicle content
- Certified commercial hobby motors only (catalog classes — not designed here)
- **No** ITAR/EAR content
- **Not** a production fab release — study Gerbers for CI/fab-diff practice

## Regenerate

```bash
PCB=rocket/kicad/ism-rocket-logger.kicad_pcb
mkdir -p rocket/fab/gerbers_tmp
kicad-cli pcb export gerbers -o rocket/fab/gerbers_tmp/ \
  -l F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste "$PCB"
kicad-cli pcb export drill -o rocket/fab/gerbers_tmp/ --format excellon --excellon-units mm "$PCB"
(cd rocket/fab/gerbers_tmp && zip -q ../ism-rocket-logger-gerbers.zip *)
rm -rf rocket/fab/gerbers_tmp
kicad-cli pcb export pos -o rocket/fab/ism-rocket-logger-cpl.csv \
  --format csv --units mm --side both "$PCB"
```
