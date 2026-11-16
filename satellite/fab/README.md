# Fab package — ISM Satellite bus board (#31)

| File | Use |
|------|-----|
| `ism-satellite-bus-gerbers.zip` | Study Gerber + Excellon upload package |
| `ism-satellite-bus-cpl.csv` | Centroid / pick-and-place |
| `BOM.csv` | SMT BOM stub (educational) |

## Scope limits (hard)

- Civilian / educational bus board only
- Payload = **mass / power / data** stubs — no weapons, seekers, guidance-to-target, warheads, or fuzing
- **No** ITAR/EAR bus or payload designs
- **Not** a production fab release — study Gerbers for CI/fab-diff practice

## Regenerate

```bash
PCB=satellite/kicad/ism-satellite-bus.kicad_pcb
mkdir -p satellite/fab/gerbers_tmp
kicad-cli pcb export gerbers -o satellite/fab/gerbers_tmp/ \
  -l F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste "$PCB"
kicad-cli pcb export drill -o satellite/fab/gerbers_tmp/ --format excellon --excellon-units mm "$PCB"
(cd satellite/fab/gerbers_tmp && zip -q ../ism-satellite-bus-gerbers.zip *)
rm -rf satellite/fab/gerbers_tmp
kicad-cli pcb export pos -o satellite/fab/ism-satellite-bus-cpl.csv \
  --format csv --units mm --side both "$PCB"
```
