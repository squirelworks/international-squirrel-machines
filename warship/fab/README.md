# Fab package — ISM Warship scale-model control (#43)

| File | Use |
|------|-----|
| `ism-warship-control-gerbers.zip` | Study Gerber + Excellon upload package |
| `ism-warship-control-cpl.csv` | Centroid / pick-and-place |
| `BOM.csv` | SMT BOM stub (educational) |

## Scope limits (hard)

- Scale-model control board only (thruster / rudder / ballast stubs)
- Weapons / combat sensors = **mass / footprint elsewhere** — not on this board
- **No** fire control, combat-system internals, seekers, guidance, warheads, or fuzing
- **No** ITAR/EAR content
- **Not** a production fab release — study Gerbers for CI/fab-diff practice

## Regenerate

```bash
PCB=warship/kicad/ism-warship-control.kicad_pcb
mkdir -p warship/fab/gerbers_tmp
kicad-cli pcb export gerbers -o warship/fab/gerbers_tmp/ \
  -l F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste "$PCB"
kicad-cli pcb export drill -o warship/fab/gerbers_tmp/ --format excellon --excellon-units mm "$PCB"
(cd warship/fab/gerbers_tmp && zip -q ../ism-warship-control-gerbers.zip *)
rm -rf warship/fab/gerbers_tmp
kicad-cli pcb export pos -o warship/fab/ism-warship-control-cpl.csv \
  --format csv --units mm --side both "$PCB"
```
