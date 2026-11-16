# ISM Sonar — (#40)

**Program ID:** ISM-SNR-1 (study name TBD)  
**This PR:** mechanical enclosure / array-mount structural study.

## Scope limits (hard) — same spirit as submarine B3

- **Educational / public** echo-sounder and fish-finder class language only
- Transducers and arrays = **mass / footprint / frequency-class stubs**
- Signal processing = **block-diagram teaching** only (TX → medium → RX → envelope)
- Display and enclosure = packaging / UI stubs
- **No** quieting or acoustic signature design
- **No** classified beamforming, ASW tactics, or combat employment
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) sonar or acoustic-warfare content
- Structural outputs are **educational enclosure stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Transducers, SP blocks, display, enclosure |
| `docs/structural.md` | Enclosure ribs / transducer face / board tray |
| `docs/citations.yaml` | Open / public citations |
| `docs/range_equation_examples.py` | Teaching active-sonar equation stub |
| `interfaces/transducer-placeholders.yaml` | Mass / footprint / frequency class |
| `interfaces/signal-chain.yaml` | Block-diagram SP stubs only |
| `interfaces/echo-board.yaml` | KiCad channel map |
| `interfaces/structural.yaml` | Structural member map |
| `kicad/ism-sonar-echo.*` | Study KiCad echo board |
| `shell/enclosure_study.scad` | Enclosure + ghost structure |

## Roadmap (#40) status
- [x] Design note (transducers, signal processing, display, enclosure)
- [x] KiCad boards (analog front-end, DSP, power)
- [x] Mechanical enclosure / array mount (this PR)
- [ ] Gerbers + STLs / mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
