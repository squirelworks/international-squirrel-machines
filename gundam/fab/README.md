# Fab package — ISM Gundam control board (#46)

| File | Use |
|------|-----|
| `ism-gundam-control-gerbers.zip` | Study Gerber + Excellon upload package |
| `ism-gundam-control-cpl.csv` | Centroid / pick-and-place |
| `BOM.csv` | SMT BOM stub (educational) |

## Scope limits (hard)

- Mecha actuator / SAFE-INHIBIT board only
- Stores = **mass / footprint / SAFE / INHIBIT** stubs — no seekers, guidance, munition propulsion, warheads, fuzing, or arming
- **No** live launch / fire sequences or engagement doctrine
- **No** ITAR/EAR weapon or fire-control designs
- **Not** a production fab release — study Gerbers for CI/fab-diff practice

## Regenerate

```bash
PCB=gundam/kicad/ism-gundam-control.kicad_pcb
mkdir -p gundam/fab/gerbers_tmp
kicad-cli pcb export gerbers -o gundam/fab/gerbers_tmp/ \
  -l F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste "$PCB"
kicad-cli pcb export drill -o gundam/fab/gerbers_tmp/ --format excellon --excellon-units mm "$PCB"
(cd gundam/fab/gerbers_tmp && zip -q ../ism-gundam-control-gerbers.zip *)
rm -rf gundam/fab/gerbers_tmp
kicad-cli pcb export pos -o gundam/fab/ism-gundam-control-cpl.csv \
  --format csv --units mm --side both "$PCB"
```
