# Satellite bus + payload — design note (B5 #31)

**Product:** ISM-SAT-1 study (3U-class smallsat teaching form)  
**Level:** public cubesat / smallsat architecture language.

## Out of scope (hard limits)

- Weapons, munitions, seekers, guidance-to-target, warheads, fuzing, arming
- Export-controlled (ITAR/EAR) bus or payload technical data
- Classified sensors or crypto
- Hostile EW / counterspace employment

Payloads appear as **mass / power / data** stubs only — see `../interfaces/payload-placeholders.yaml`.

---

## 1. Bus architecture

| Subsystem | Baseline study | Notes |
|-----------|----------------|-------|
| OBC | Dual-redundant MCU class (later KiCad) | Flight software out of B5 |
| EPS | Solar → battery → regulated rails | Power budget teaching |
| ADCS | Passive / coarse (magnetorquer class) | Detumble + coarse point — **not** weapons pointing |
| Comms | UHF/VHF or S-band amateur/educational class | Beacon + command — public bands |
| Structure | 3U aluminum / additive frame | `shell/bus_study.scad` |
| Thermal | Passive radiation + MLI stub | No classified coatings |

Machine-readable: `../interfaces/bus.yaml`.

---

## 2. Power

Teaching budget (orbit-average, provisional):

| Load | W (orbit avg) |
|------|---------------|
| OBC | 0.8 |
| Comms (duty-cycled) | 1.2 |
| ADCS | 0.5 |
| Payload stub | 1.0 |
| Margin / battery charge | 1.5 |
| **Total** | **~5.0** |

Solar array class sized for ~6–8 W peak BOL teaching; battery Wh class stores eclipse.  
Check: `python3 satellite/docs/power_budget_examples.py`.

---

## 3. Comms

| Link | Role | B5 stance |
|------|------|-----------|
| Beacon | Health / ID | Continuous low-rate |
| Command uplink | Safe modes | Authenticated later — stub only |
| Telemetry downlink | Housekeeping + payload data stubs | No weapons telemetry |
| Not in B5 | Inter-satellite combat nets, encrypted mil waveforms | — |

---

## 4. Structure

| Item | Baseline |
|------|----------|
| Form factor | 3U (100 × 100 × 340 mm class) |
| Rails | Standard cubesat rail keep-outs (public CubeSat Design Spec language) |
| Panels | Deployable or body-mounted solar |
| Launch loads | Placeholder — structural PR later |

---

## 5. Payload (placeholders)

| ID | Mass (kg) | Power (W avg) | Data (kbps stub) | Purpose |
|----|-----------|---------------|------------------|---------|
| PL-EO-EDU | 0.35 | 1.0 | 10 | Educational imager mass/power only — no targeting |
| PL-SCI-RADIO | 0.20 | 0.5 | 5 | Science radio experiment stub |
| PL-TECH-DEMO | 0.15 | 0.3 | 2 | Bus tech demo mass |

**No** kinetic, directed-energy, or munition payloads.

---

## 6. Next steps
KiCad OBC/EPS/radio, mechanical panels, Gerbers/STLs, BOM, polish.
