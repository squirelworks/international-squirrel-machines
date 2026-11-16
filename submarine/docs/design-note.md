# Submarine design note — B3 (#44)

**Product:** ISM-SS-1 study (printable scale-model hull)  
**Hydrodynamics:** public-domain / textbook only.

## Out of scope (hard limits)

- Quieting, acoustic signature, sonar signal processing
- Life-support / atmosphere / habitability design
- Weapons interfaces, fire control, combat-system internals
- Seekers, guidance, warheads, fuzing, arming
- Export-controlled (ITAR/EAR) data

Sonar and other sensors appear **only** as mass/footprint placeholders — `../interfaces/mass-placeholders.yaml`.

---

## 1. Hull form (study)

| Feature | Baseline study | Notes |
|---------|----------------|-------|
| Type | Axisymmetric teardrop / Albacore-class teaching form | Smooth of-revolution study; not a classified offset |
| L/D | ~7–9 | Scale-model printable proportions |
| Sail / fairwater | Small stub | Mass/KG and appendage drag flag later |
| Control surfaces | Cruciform stern stubs | Scale-model actuators later (KiCad) |

Study solid: `../shell/hull_study.scad` (mm; printable proportion sketch).

---

## 2. Pressure hull concept (qualitative)

| Topic | B3 stance |
|-------|-----------|
| Concept | Inner pressure hull + outer free-flooding casing (textbook two-hull language) |
| Material class | Steel or Al study class for **scale model** — not a certified pressure vessel |
| Frames / rings | Study spacing in `structural.md` / `structural.yaml` / shell |
| Not in B3 | Collapse pressure calculation as a certified design; life-support penetrations |

Study structural / pressure-hull layout: `structural.md` + `interfaces/structural.yaml` (still not a certified vessel).

---

## 3. Ballast / trim (textbook)

Surfaced and submerged conditions use public teaching identities:

| Symbol | Meaning | Study use |
|--------|---------|-----------|
| \(\nabla\) | Displaced volume (submerged) | Hull volume estimate |
| \(\Delta\) | Mass displacement \(\rho\nabla\) | Freshwater scale-model \(\rho \approx 1000\) |
| Reserve buoyancy | Surfaced \(\Delta_\mathrm{surf} < \Delta_\mathrm{sub}\) | Positive reserve for surfaced float |
| Trim | Longitudinal balance of LCG vs LCB | Ballast tank pair fore/aft stubs |
| Neutral buoyancy | Submerged weight ≈ displacement | Scale-model lead/foam trim plan later |

Machine-readable stubs: `../interfaces/hydrostatics.yaml`.  
Teaching check: `python3 submarine/docs/trim_examples.py`.

**No** acoustic / quieting content in ballast system notes.

---

## 4. Propulsion packaging

| Item | Baseline |
|------|----------|
| Class | Single shaft + ducted propulsor **class** (public naming) for scale model |
| Packaging | Aft machinery volume stub; shaft keep-out |
| Scale-model controls | ESC / servo channels deferred to KiCad roadmap step |
| Not in B3 | Propeller cavitation design, pump-jet recipes, or quieting |

---

## 5. Scale-model controls (interface stub)

| Channel | Role | B3 status |
|---------|------|-----------|
| Rudder / sternplanes | Attitude | Named for later KiCad |
| Ballast pump / valve | Surfaced↔submerged demo | Named only — no plumbing design |
| Propulsor ESC | Ahead/astern | Named only |
| Depth / IMU | Telemetry stub | Soft/HIL later — not this tree |

---

## 6. Sonar / sensor mass placeholders

| ID | Kind | Mass (kg) scale-model | Footprint | Purpose |
|----|------|----------------------|-----------|---------|
| SEN-SONAR-BOW | Sensor mass box | 0.15 | Ø40 × 30 mm | Bow dome mass only |
| SEN-SONAR-FLANK | Sensor mass box | 0.08 | 80 × 20 × 10 mm | Flank array **mass** only — no acoustic processing |
| SEN-MAST-OPTO | Sensor mass box | 0.05 | 20 × 20 × 40 mm | Mast/optics mass stub |

Authoritative rows: `../interfaces/mass-placeholders.yaml`.

## 7. Next steps
Gerbers/STLs, BOM, polish remain open after structural study.
