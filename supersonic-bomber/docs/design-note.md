# Supersonic bomber — design note (#39 deepen)

**Product:** ISM-XB-1 study  
**Regime:** supersonic cruise class (textbook M ≈ 1.5–3) — **not** hypersonic TPS (#37).  
**Prior:** B1 design-note slice; this revision adds machine-readable stubs.

## Out of scope (hard limits)

- Guidance, seekers, munition propulsion, warheads, fuzing, arming codes
- Employment or targeting content
- Scramjet / hypersonic TPS recipes — see `hypersonic-bomber/docs/`
- Export-controlled (ITAR/EAR) munition or fire-control designs

Payload appears **only** as inert bay mass/volume/SAFE-INHIBIT stubs — see `../interfaces/payload-placeholders.yaml`.

---

## 1. Airframe layout (study)

| Feature | Baseline study | Notes |
|---------|----------------|-------|
| Planform | Low-aspect swept / delta-ish | Wave-drag awareness at M>1 |
| Fuselage | Area-ruled slender body (qualitative) | Sears–Haack / area-rule hygiene |
| Inlets | Side or under-fuselage | Packaging vs bay — product decision |
| Empennage | Fin + all-moving stab or V-tail option | Later ICD |

Stations / dimensions: `../interfaces/airframe.yaml`. Study OML: `../shell/airframe_study.scad`.

---

## 2. Avionics (conceptual)

Same partition idea as subsonic (#38): FCC safety-critical, MC owns bay/SAFE-INHIBIT discretes, nav/EO stubs without targeting employment. May align bus patterns with `fighter-jet/interfaces/` later without copying weapons topics.

---

## 3. Thermal (cruise — not hypersonic TPS)

| Topic | Stance |
|-------|--------|
| Kinetic heating | Milder than hypersonic; recovery-temperature **class** stub |
| Hot spots | Leading edges, inlet lips, canopy — materials flag |
| TPS | No ablative/reusable hypersonic stack here → #37 |
| Avionics cooling | ECS / cold-plate stubs when KiCad lands |

Teaching adiabatic recovery temperature: `thermal_examples.py` (classroom γ, M — not a materials allowables product).

---

## 4. Propulsion interface

| Item | Baseline |
|------|----------|
| Class | Low-bypass turbofan or turbojet **class** (+ afterburner option, public language) |
| Count | Twin — yaw on engine-out packaging |
| Interfaces | Mounts, inlet duct keep-outs, nozzle vs empennage |
| Not here | Cycle deck, plume IR prediction, fuel chemistry |

---

## 5. Payload / bay (inert only)

| ID | Kind | Purpose |
|----|------|---------|
| BAY-MAIN | volume stub | Internal bay keep-out |
| PLD-INERT-A/B | mass/CG boxes | Training / inert class |
| DOOR-SAFE | discrete stub | SAFE/INHIBIT only |

**SAFE / INHIBIT** (integration only — no arming or live release):

| Condition | SAFE | INHIBIT bay release |
|-----------|------|---------------------|
| Ground maintenance | asserted | asserted |
| Weight-on-wheels | asserted | asserted |
| Inert present, no sim auth | asserted | asserted |
| Sim inert release auth | deasserted* | deasserted* |

\*Simulated inert only — **no** live munitions.

## 6. Next steps
KiCad, structure, Gerbers/STLs, BOM, polish.
