# Fab package — ISM Fighter Jet bay board (#85)

| File | Use |
|------|-----|
| `ism-fighter-jet-gerbers.zip` | Study Gerber + Excellon upload package |
| `ism-fighter-jet-cpl.csv` | Centroid / pick-and-place |
| `BOM.csv` | SMT BOM stub (educational) |

## Scope limits (hard)

- Avionics-bay **electrical slice** only (surface / throttle stubs)
- Stores / weapons = **mass / footprint / SAFE / INHIBIT** elsewhere in-program — this board has **no** stores fire channels
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming
- **No** ITAR/EAR weapon or fire-control designs
- **Not** a production fab release — study Gerbers for CI/fab-diff practice

## Regenerate

```bash
PCB=fighter-jet/kicad/ism-fighter-jet.kicad_pcb
mkdir -p fighter-jet/fab/gerbers_tmp
kicad-cli pcb export gerbers -o fighter-jet/fab/gerbers_tmp/ \
  -l F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste "$PCB"
kicad-cli pcb export drill -o fighter-jet/fab/gerbers_tmp/ --format excellon --excellon-units mm "$PCB"
(cd fighter-jet/fab/gerbers_tmp && zip -q ../ism-fighter-jet-gerbers.zip *)
rm -rf fighter-jet/fab/gerbers_tmp
kicad-cli pcb export pos -o fighter-jet/fab/ism-fighter-jet-cpl.csv \
  --format csv --units mm --side both "$PCB"
```
