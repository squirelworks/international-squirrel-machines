# Fab package — ISM Space Station habitat board (#42)

| File | Use |
|------|-----|
| `ism-station-hab-gerbers.zip` | Study Gerber + Excellon upload package |
| `ism-station-hab-cpl.csv` | Centroid / pick-and-place |
| `BOM.csv` | SMT BOM stub (educational) |

## Scope limits (hard)

- Habitat / civil station board only
- Docking = **mass / volume / power** stubs — no weapons, seekers, guidance-to-target, warheads, or fuzing
- **No** ITAR/EAR station or combat designs
- **Not** a production fab release — study Gerbers for CI/fab-diff practice

## Regenerate

```bash
PCB=space-station/kicad/ism-station-hab.kicad_pcb
mkdir -p space-station/fab/gerbers_tmp
kicad-cli pcb export gerbers -o space-station/fab/gerbers_tmp/ \
  -l F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste "$PCB"
kicad-cli pcb export drill -o space-station/fab/gerbers_tmp/ --format excellon --excellon-units mm "$PCB"
(cd space-station/fab/gerbers_tmp && zip -q ../ism-station-hab-gerbers.zip *)
rm -rf space-station/fab/gerbers_tmp
kicad-cli pcb export pos -o space-station/fab/ism-station-hab-cpl.csv \
  --format csv --units mm --side both "$PCB"
```
