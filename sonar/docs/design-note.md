# Sonar — design note (#40)

**Product:** ISM-SNR-1 study (educational echo-sounder class)  
**Level:** public / textbook active-sonar language (fish-finder / depth-sounder teaching).

## Out of scope (hard limits — B3 spirit)

- Quieting, acoustic signature control, or stealth coatings
- Classified beamforming, ASW tactics, or combat employment
- Weapons interfaces, fire control, seekers, guidance, warheads, fuzing
- Export-controlled (ITAR/EAR) sonar or acoustic-warfare designs
- Detailed hydrophone array processing beyond a teaching block diagram

---

## 1. Transducers

| ID | Role | Placeholder fields |
|----|------|--------------------|
| XDCR-TX | Active projector class | Mass, footprint, frequency class |
| XDCR-RX | Hydrophone / receive class | Mass, footprint |
| ARRAY-HULL | Optional hull-strip mass box | Footprint only — **no** array processing design |

Frequency class for this study: **~200 kHz** teaching echo-sounder band (public fish-finder order of magnitude). See `../interfaces/transducer-placeholders.yaml`.

---

## 2. Signal processing (block diagram only)

```
TX pulse → transducer → water path → echo → RX → envelope detect → range display
```

| Block | Teaching role |
|-------|---------------|
| Pulse generator | Fixed-width TX stub |
| Transmit amp | Power class stub |
| Receive preamp | Gain class stub |
| Envelope / peak detect | Depth from time-of-flight |
| Display driver | Range / depth readout |

**Not in this PR:** adaptive beamforming, matched-filter libraries for combat sonar, quieting filters, or classified SP. Machine-readable stubs: `../interfaces/signal-chain.yaml`.

---

## 3. Display

| Element | Stub |
|---------|------|
| Depth readout | Digits + simple A-scope class |
| Bottom lock | Teaching latch flag |
| Alerts | Shallow / deep thresholds |

UI is packaging-level for later KiCad / firmware — no combat HMI.

---

## 4. Enclosure

| Mode | Study |
|------|-------|
| Handheld / portable | Box + transducer face |
| Hull-mount flange | Mount plate mass/footprint |

`../shell/enclosure_study.scad` — printable enclosure sketch with transducer face keepout.

---

## 5. Teaching range equation

Public active-sonar equation (simplified):

\[
\text{SL} - 2\,\text{TL} + \text{TS} - \text{NL} + \text{DI} \ge \text{DT}
\]

Study uses a **toy numeric** check in `range_equation_examples.py` (classroom dB stubs, not a survey product). Time-of-flight depth:

\[
d = \frac{c\,t}{2},\quad c \approx 1500\,\text{m/s}
\]

## 6. Next steps
KiCad AFE/DSP/power, mechanical array mount, Gerbers/STLs, BOM, polish.
