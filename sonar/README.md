# ISM Sonar — (#40)

**Program ID:** ISM-SNR-1 (study name TBD)  
**Status:** design note → KiCad → structural → Gerbers/STL → BOM/assembly in-tree; polish / inquire still open.

## Prior slices
Design-note (transducers / SP / display / enclosure). KiCad echo board. Mechanical enclosure / array-mount. Gerbers + STL. This PR adds educational master BOM + assembly sequence.

## Scope limits (hard) — same spirit as submarine B3

- **Educational / public** echo-sounder and fish-finder class language only
- Transducers and arrays = **mass / footprint / frequency-class stubs**
- Signal processing = **block-diagram teaching** only (TX → medium → RX → envelope)
- Display and enclosure = packaging / UI stubs
- **No** quieting or acoustic signature design
- **No** classified beamforming, ASW tactics, or combat employment
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) sonar or acoustic-warfare content
- Fab/STL/BOM outputs are **educational enclosure stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Transducers, SP blocks, display, enclosure |
| `docs/structural.md` | Enclosure ribs / transducer face / board tray |
| `docs/fab-mechanical.md` | Gerber + STL notes |
| `docs/bom.md` | Educational master BOM |
| `docs/assembly.md` | Study assembly sequence |
| `docs/citations.yaml` | Open / public citations |
| `docs/range_equation_examples.py` | Teaching active-sonar equation stub |
| `interfaces/transducer-placeholders.yaml` | Mass / footprint / frequency class |
| `interfaces/signal-chain.yaml` | Block-diagram SP stubs only |
| `interfaces/echo-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-sonar-echo.*` | Study KiCad echo board |
| `fab/` | Study Gerbers + CPL + BOM stub |
| `shell/enclosure_study.scad` | Enclosure + ghost structure |
| `mechanical/enclosure_study.stl` | Exported study STL |

## Roadmap (#40) status
- [x] Design note (transducers, signal processing, display, enclosure)
- [x] KiCad boards (analog front-end, DSP, power)
- [x] Mechanical enclosure / array mount
- [x] Gerbers + STLs / mechanical files
- [x] BOM / assembly
- [ ] Polish and inquire for release
