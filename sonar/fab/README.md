# Fab package — ISM Sonar echo board (#40)

| File | Use |
|------|-----|
| `ism-sonar-echo-gerbers.zip` | Study Gerber + Excellon upload package |
| `ism-sonar-echo-cpl.csv` | Centroid / pick-and-place |
| `BOM.csv` | SMT BOM stub (educational) |

## Scope limits (hard) — B3-style

- Educational / public echo-sounder and fish-finder class only
- Transducers = **mass / footprint / frequency-class** stubs
- **No** quieting or acoustic signature design
- **No** classified beamforming, ASW tactics, combat employment
- **No** weapons, fire control, seekers, guidance, warheads, or fuzing
- **No** ITAR/EAR sonar content
- **Not** a production fab release

## Regenerate

```bash
PCB=sonar/kicad/ism-sonar-echo.kicad_pcb
mkdir -p sonar/fab/gerbers_tmp
kicad-cli pcb export gerbers -o sonar/fab/gerbers_tmp/ \
  -l F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste "$PCB"
kicad-cli pcb export drill -o sonar/fab/gerbers_tmp/ --format excellon --excellon-units mm "$PCB"
(cd sonar/fab/gerbers_tmp && zip -q ../ism-sonar-echo-gerbers.zip *)
rm -rf sonar/fab/gerbers_tmp
kicad-cli pcb export pos -o sonar/fab/ism-sonar-echo-cpl.csv \
  --format csv --units mm --side both "$PCB"
```
