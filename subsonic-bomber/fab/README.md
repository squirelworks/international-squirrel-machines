# Fab package — ISM Subsonic Bomber bay board (#38)

| File | Use |
|------|-----|
| `ism-sb-bay-gerbers.zip` | Study Gerber + Excellon upload package |
| `ism-sb-bay-cpl.csv` | Centroid / pick-and-place |
| `BOM.csv` | SMT BOM stub (educational) |

## Weapons boundary (hard)

- Bay channels = **SAFE/INHIBIT / door / WOW stubs** only
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming
- **Not** a production fab release — study Gerbers for CI/fab-diff practice

## Regenerate

```bash
PCB=subsonic-bomber/kicad/ism-sb-bay.kicad_pcb
mkdir -p subsonic-bomber/fab/gerbers_tmp
kicad-cli pcb export gerbers -o subsonic-bomber/fab/gerbers_tmp/ \
  -l F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste "$PCB"
kicad-cli pcb export drill -o subsonic-bomber/fab/gerbers_tmp/ --format excellon --excellon-units mm "$PCB"
(cd subsonic-bomber/fab/gerbers_tmp && zip -q ../ism-sb-bay-gerbers.zip *)
rm -rf subsonic-bomber/fab/gerbers_tmp
kicad-cli pcb export pos -o subsonic-bomber/fab/ism-sb-bay-cpl.csv \
  --format csv --units mm --side both "$PCB"
```
