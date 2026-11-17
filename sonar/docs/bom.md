# Sonar — educational master BOM (#40)

**Product:** ISM-SNR-1  
**Slice:** study BOM tying the echo-board fab package to the enclosure STL / structural stubs.

## Scope / weapons boundary (hard)

- Educational / public echo-sounder and fish-finder class only
- Transducers / arrays = **mass / footprint / frequency-class** stubs
- Signal processing = block-diagram teaching only
- **No** quieting or acoustic signature design
- **No** classified beamforming, ASW tactics, or combat employment
- **No** weapons, fire control, seekers, guidance, warheads, or fuzing
- **No** ITAR/EAR sonar content
- **Not** a procurement order — PNs freeze at inquire-for-release

## Board (SMT) — from `../fab/BOM.csv`

| Ref | Qty | Value | Role |
|-----|-----|-------|------|
| U1 | 1 | RP2040 | Echo DSP / control MCU stub |
| U2 | 1 | IMU-6DOF | Packaging attitude stub |
| U3 | 1 | RADIO | Telemetry stub |
| J1 | 1 | PinHeader 1×03 | Educational TX pulse enable stub |
| J2 | 1 | PinHeader 1×03 | Analog front-end envelope stub |
| J3 | 1 | PinHeader 1×03 | DSP range UART stub |
| J4 | 1 | PinHeader 1×03 | Display backlight stub |
| H1–H4 | 4 | M3 hole | Board mounting |

## Mechanical / study article

| ID | Qty | Item | Source |
|----|-----|------|--------|
| MECH-ENC-STL | 1 | `enclosure_study.stl` print (enclosure / transducer face / ribs) | `../mechanical/` |
| MECH-SCAD | 1 | `enclosure_study.scad` parametric source | `../shell/` |
| MECH-FAST-M3 | lot | M3 hardware for board tray | study |
| MECH-TRAY | 1 | Echo-board tray stub | `structural.yaml` |
| XDCR-STUB | 1 | Transducer mass/footprint/frequency-class placeholder | `transducer-placeholders.yaml` |

## Electrical harness (study)

| ID | Qty | Item | Notes |
|----|-----|------|-------|
| HAR-TX | 1 | TX pulse enable lead | J1 — educational pulse only |
| HAR-AFE | 1 | AFE envelope lead | J2 — teaching block diagram |
| HAR-DSP | 1 | DSP range UART lead | J3 |
| HAR-DISP | 1 | Display backlight lead | J4 |
| HAR-PWR | 1 | Bench / EPS stub | Current-limited |

## Out of BOM (explicit)

Quieting / acoustic-signature kits, classified beamforming hardware, ASW tactics gear, weapons interfaces, fire control, seekers, guidance, warheads, fuzing, ITAR/EAR sonar designs.
