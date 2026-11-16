# Fab package — ISM Supersonic Bomber bay board (#39)

| File | Use |
|------|-----|
| `ism-xb-bay-gerbers.zip` | Study Gerber + Excellon upload package |
| `ism-xb-bay-cpl.csv` | Centroid / pick-and-place |
| `BOM.csv` | SMT BOM stub (educational) |

## Weapons boundary (hard)

- Bay channels = **SAFE/INHIBIT / door / WOW stubs** only
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming
- **Not** a production fab release — study Gerbers for CI/fab-diff practice

## Regenerate

```bash
PCB=supersonic-bomber/kicad/ism-xb-bay.kicad_pcb
mkdir -p supersonic-bomber/fab/gerbers_tmp
kicad-cli pcb export gerbers -o supersonic-bomber/fab/gerbers_tmp/ \
  -l F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste "$PCB"
kicad-cli pcb export drill -o supersonic-bomber/fab/gerbers_tmp/ --format excellon --excellon-units mm "$PCB"
(cd supersonic-bomber/fab/gerbers_tmp && zip -q ../ism-xb-bay-gerbers.zip *)
rm -rf supersonic-bomber/fab/gerbers_tmp
kicad-cli pcb export pos -o supersonic-bomber/fab/ism-xb-bay-cpl.csv \
  --format csv --units mm --side both "$PCB"
```
