# Fab package — ISM Aircraft Carrier deck control (#45)

| File | Use |
|------|-----|
| `ism-carrier-deck-gerbers.zip` | Study Gerber + Excellon upload package |
| `ism-carrier-deck-cpl.csv` | Centroid / pick-and-place |
| `BOM.csv` | SMT BOM stub (educational) |

## Scope limits (hard)

- Scale-model deck control only (elevator / catapult / arresting / rudder stubs)
- Weapons / combat sensors / aviation ordnance = **mass / footprint elsewhere**
- **No** fire control, combat-system internals, seekers, guidance, warheads, or fuzing
- Catapult / arresting = load/mass stubs only (no classified plant design)
- **No** ITAR/EAR content
- **Not** a production fab release — study Gerbers for CI/fab-diff practice

## Regenerate

```bash
PCB=aircraft-carrier/kicad/ism-carrier-deck.kicad_pcb
mkdir -p aircraft-carrier/fab/gerbers_tmp
kicad-cli pcb export gerbers -o aircraft-carrier/fab/gerbers_tmp/ \
  -l F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste "$PCB"
kicad-cli pcb export drill -o aircraft-carrier/fab/gerbers_tmp/ --format excellon --excellon-units mm "$PCB"
(cd aircraft-carrier/fab/gerbers_tmp && zip -q ../ism-carrier-deck-gerbers.zip *)
rm -rf aircraft-carrier/fab/gerbers_tmp
kicad-cli pcb export pos -o aircraft-carrier/fab/ism-carrier-deck-cpl.csv \
  --format csv --units mm --side both "$PCB"
```
