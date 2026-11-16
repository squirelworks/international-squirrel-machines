# Aircraft carrier — B2 design-note slice (#45 with warship #43)

**Product:** ISM-CV-1 study  
**B2 role:** arrangements / mass placeholders only — not a full #45 delivery.

## Out of scope (hard limits)
Same as warship B2: no weapons interfaces, fire control, combat-system internals, seekers, guidance, warheads, fuzing, or ITAR/EAR combat data. Aviation ordnance appears only as inert mass/footprint boxes if listed later.

---

## 1. Flight deck (study)

| Feature | Baseline | Notes |
|---------|----------|-------|
| Deck area | Long rectangle study | Proportion sketch in `../shell/deck_study.scad` |
| Landing area | Aft angled stub (qualitative) | Geometry packaging — no ops doctrine |
| Catapult / launch | Forward zone keep-out box | Mass/volume stub only |
| Island | Starboard superstructure mass box | KG / windage — no combat consoles |

---

## 2. Aviation systems (placeholders)

| ID | Kind | Mass (t) | Footprint | Purpose |
|----|------|----------|-----------|---------|
| AV-ELEV-1 | Elevator mass box | 80 | 15 × 12 m | Elevator structure mass |
| AV-ELEV-2 | Elevator mass box | 80 | 15 × 12 m | Elevator structure mass |
| AV-JP5 | Fuel mass stub | 500 | tank volume TBD | Aviation fuel mass — no weapons |
| AV-ORD-INERT | Inert ordnance mass box | 50 | magazine footprint TBD | **Inert** mass only |

No aircraft combat-system internals; fighter program owns air-vehicle ICD separately (`fighter-jet/`).

---

## 3. Propulsion / powering
Nuclear or conventional island-power **class** as a product decision later. B2 stores only: machinery-box volume and electrical MW stub — no plant design.

## 4. Combat sensors / weapons
Inherit warship policy: mass/footprint placeholders only (`../../warship/interfaces/mass-placeholders.yaml` pattern). Carrier-specific combat boxes deferred until a dedicated #45 PR if needed.

## 5. Next (#45)
KiCad, structure, Gerbers/STLs, BOM, polish — not this slice.
