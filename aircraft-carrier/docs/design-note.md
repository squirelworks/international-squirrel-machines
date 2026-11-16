# Aircraft carrier — design note (#45 deepen)

**Product:** ISM-CV-1 study  
**Level:** public / textbook naval-architecture and carrier-arrangements language.  
**Prior:** B2 light slice with warship #43; this revision completes the #45 design-note checkbox.

## Out of scope (hard limits)

- Weapons interfaces, fire control, combat-system internals
- Seekers, guidance, warheads, fuzing, arming codes, engagement doctrine
- Export-controlled (ITAR/EAR) combat, acoustic, or nuclear-plant design detail
- Classified catapult / EMALS plant internals (keep-out / load class only)

Weapons and combat sensors exist **only** as mass and deck-footprint placeholders — see `../interfaces/mass-placeholders.yaml`.

---

## 1. Flight deck

| Feature | Baseline study | Notes |
|---------|----------------|-------|
| Deck plan | Long rectangle + angled landing stub | `../shell/deck_study.scad` |
| Landing area | Aft angled keep-out | Packaging — no ops doctrine |
| Launch zone | Forward catapult keep-outs | Mass / length class stubs |
| Arresting | Aft wire zone keep-out | Load-class stub only |
| Island | Starboard superstructure | KG / windage mass box |
| Elevators | Two deck openings | Mass + footprint in aviation stubs |

Teaching deck-area parking budget: `deck_area_examples.py`.

---

## 2. Aviation systems

| ID | Kind | Mass (t) | Footprint | Purpose |
|----|------|----------|-----------|---------|
| AV-ELEV-1 | Elevator mass box | 80 | 15 × 12 m | Structure mass |
| AV-ELEV-2 | Elevator mass box | 80 | 15 × 12 m | Structure mass |
| AV-JP5 | Fuel mass stub | 500 | tank volume class | Aviation fuel — no weapons |
| AV-ORD-INERT | Inert ordnance mass box | 50 | magazine footprint | **Inert** mass only |
| AV-HANGAR | Hangar deck volume stub | — | area class | Parking / service |
| AV-CAT-1/2 | Catapult keep-out | 40 each | length class | Mass / keep-out — no plant design |
| AV-ARREST | Arresting gear mass | 30 | zone footprint | Load-class stub |

Machine-readable: `../interfaces/aviation.yaml`. Air-vehicle ICD remains with `fighter-jet/`.

---

## 3. Combat systems (placeholders only)

Carrier-specific combat boxes (same policy as warship B2):

| ID | Kind | Purpose |
|----|------|---------|
| WP-CIWS-FWD / AFT | weapon_mass_box | Point-defense mount mass only |
| WP-VLS-FWD | weapon_mass_box | Launch mass/volume only — no cells/FC |
| SEN-RADAR-ISLAND | combat_sensor_mass_box | Radar house mass / windage |
| SEN-EO-DIR | combat_sensor_mass_box | Director mass only |
| SEN-TACAN-IFF | sensor_mass_box | Nav/ident mass stub — no waveforms |

No track files, fire-control logic, or engagement doctrine. See `../interfaces/mass-placeholders.yaml`.

---

## 4. Propulsion / powering

| Topic | Study stance |
|-------|--------------|
| Plant class | Nuclear **or** conventional island-power — product decision later |
| Machinery box | Volume / mass stub amidships–aft |
| Electrical | MW-class hotel + aviation load stub |
| Propulsors | Twin/quad shaft stubs — packaging only |

No nuclear-plant design, no classified EMALS power electronics.

---

## 5. Structure study

`../shell/deck_study.scad` — hull + flight deck + island + elevator openings + topside radar/CIWS mass boxes (geometry packaging only).

## 6. Next steps
KiCad, structural design, Gerbers/STLs, BOM, polish.
