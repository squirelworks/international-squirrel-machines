# ISM Sonar — (#40)

**Program ID:** ISM-SNR-1 (study name TBD)  
**This PR:** KiCad echo AFE / DSP / power board slice.

## Scope limits (hard) — same spirit as submarine B3

- **Educational / public** echo-sounder and fish-finder class language only
- Transducers and arrays = **mass / footprint / frequency-class stubs**
- Signal processing = **block-diagram teaching** only (TX → medium → RX → envelope)
- Display and enclosure = packaging / UI stubs
- **No** quieting or acoustic signature design
- **No** classified beamforming, ASW tactics, or combat employment
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) sonar or acoustic-warfare content
- KiCad outputs are **AFE / DSP / power / display stubs** only

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Transducers, SP blocks, display, enclosure |
| `docs/citations.yaml` | Open / public citations |
| `docs/range_equation_examples.py` | Teaching active-sonar equation stub |
| `interfaces/transducer-placeholders.yaml` | Mass / footprint / frequency class |
| `interfaces/signal-chain.yaml` | Block-diagram SP stubs only |
| `interfaces/echo-board.yaml` | KiCad channel map |
| `kicad/ism-sonar-echo.*` | Study KiCad echo board |
| `shell/enclosure_study.scad` | Handheld / hull-mount enclosure study |

## Roadmap (#40) status
- [x] Design note (transducers, signal processing, display, enclosure)
- [x] KiCad boards (analog front-end, DSP, power — this PR)
- [ ] Mechanical enclosure / array mount
- [ ] Gerbers + STLs / mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
