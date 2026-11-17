# Sonar — Gerbers + mechanical files (#40)

**Product:** ISM-SNR-1  
**Slice:** study Gerber package for the educational echo board + OpenSCAD enclosure STL export.

## Scope limits (hard)

- Educational / public echo-sounder class only
- Transducers / arrays = **mass / footprint / frequency-class** stubs
- Signal processing = block-diagram teaching only
- **No** quieting, acoustic signature, classified beamforming, ASW tactics
- **No** weapons, fire control, seekers, guidance, warheads, or fuzing
- **No** ITAR/EAR content
- Structural / STL outputs remain **educational enclosure stubs**

## Deliverables

| Path | Role |
|------|------|
| `../fab/ism-sonar-echo-gerbers.zip` | Gerber + drill study package |
| `../fab/ism-sonar-echo-cpl.csv` | Centroid |
| `../fab/BOM.csv` | Educational BOM stub |
| `../mechanical/enclosure_study.stl` | Enclosure / transducer face / ribs STL |

## Next

BOM / assembly notes: `bom.md`, `assembly.md` (this program track). Remaining: polish / inquire-for-release.
