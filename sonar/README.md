# ISM Sonar — (#40)

**Program ID:** ISM-SNR-1 (study name TBD)  
**This PR:** design-note slice — transducers, signal-processing blocks, display, enclosure.

## Scope limits (hard) — same spirit as submarine B3

- **Educational / public** echo-sounder and fish-finder class language only
- Transducers and arrays = **mass / footprint / frequency-class stubs**
- Signal processing = **block-diagram teaching** only (TX → medium → RX → envelope)
- Display and enclosure = packaging / UI stubs
- **No** quieting or acoustic signature design
- **No** classified beamforming, ASW tactics, or combat employment
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) sonar or acoustic-warfare content

## Deliverables

| Path | Role |
|------|------|
| `docs/design-note.md` | Transducers, SP blocks, display, enclosure |
| `docs/citations.yaml` | Open / public citations |
| `docs/range_equation_examples.py` | Teaching active-sonar equation stub |
| `interfaces/transducer-placeholders.yaml` | Mass / footprint / frequency class |
| `interfaces/signal-chain.yaml` | Block-diagram SP stubs only |
| `shell/enclosure_study.scad` | Handheld / hull-mount enclosure study |

## Roadmap (#40) status
- [x] Design note (transducers, signal processing, display, enclosure)
- [ ] KiCad boards (analog front-end, DSP, power)
- [ ] Mechanical enclosure / array mount
- [ ] Gerbers + STLs / mechanical files
- [ ] BOM / assembly
- [ ] Polish and inquire for release
