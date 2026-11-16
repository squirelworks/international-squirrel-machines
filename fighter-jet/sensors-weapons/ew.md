# Electronic Warfare stubs — ISM-FJ-1 (textbook / packaging)

**Program:** ISM-EW-1 self-protect suite (fictional brochure names)  
**Level:** public / educational self-protect language only.  
**Related:** stores integration for jammer/CMDS mass-drag (`hardpoints.yaml`, `inert-stores.yaml`).

## Out of scope (hard limits)

- Real-world classified waveforms, frequencies, or national system names
- Seekers, guidance, munition propulsion, warheads, fuzing, arming codes
- Live dispense / jam employment sequences or tactics doctrine
- Export-controlled (ITAR/EAR) EW techniques or threat libraries

---

## 1. Elements (stubs)

| Element | Intent | Packaging |
|---------|--------|-----------|
| RWR / ESM | Detect emitters; cue LAD | Tip/fin + aft mass boxes |
| CMDS | Flare/chaff **class** dispensers | Fuselage bay mass/footprint |
| RF jammer pod | Optional centerline / WS station | Inert store mass/drag on STA-9 class |
| Towed decoy stub | Block 2 optional | Mass/reel footprint only |

Machine-readable: `../interfaces/ew-placeholders.yaml`.

---

## 2. Integration

- MC owns EW tactics UI stubs; FCC unaffected except mass/drag stores config
- Jammer pod / CMDS cartridges are **inert integration** placeholders (same weapons boundary as stores)
- Dispense / radiate paths are **SAFE / INHIBIT** only — no ARM or live fire

### SAFE / INHIBIT (dispense / radiate) — lab truth table

| Condition | SAFE | INHIBIT dispense/radiate |
|-----------|------|--------------------------|
| Ground maintenance | asserted | asserted |
| Weight-on-wheels | asserted | asserted |
| Among friendlies / range unsafe (sim) | asserted | asserted |
| Airborne, sim consent only | deasserted* | deasserted* |

\*Simulated consent for Flight Lab / HIL only — **no** live expendables or classified RF.

Teaching check: `../docs/ew_inhibit_examples.py`.

---

## 3. Rules for this repository

- Contemporaries studied as reference only; ISM names are original (`ISM-EW-1`, `ISM-EW-RWR`, …)
- No waveforms, pulse libraries, or national threat emitters
- Carriage of jammer pod follows inert-stores / carriage-drag patterns

## 4. Next steps
KiCad bay discretes for CMDS SAFE lines; Soft EW UI (Steve); physical fit of jammer inert model.
