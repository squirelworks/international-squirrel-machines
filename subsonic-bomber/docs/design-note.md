# Subsonic bomber — design note (#38 deepen)

**Product:** ISM-SB-1 study  
**Regime:** high-subsonic cruise (textbook transport/bomber class — not a fighter).  
**Prior:** B1 design-note slice; this revision completes machine-readable stubs.

## Out of scope (hard limits)

- Guidance, seekers, munition propulsion, warheads, fuzing, arming codes
- Employment, targeting, or weapons-effectiveness content
- Export-controlled (ITAR/EAR) munition or fire-control designs
- Classified signatures or quieting

Payload appears **only** as inert bay mass/volume/SAFE-INHIBIT stubs — see `../interfaces/payload-placeholders.yaml`.

---

## 1. Airframe layout (study)

| Feature | Baseline study | Notes |
|---------|----------------|-------|
| Planform | High-aspect swept wing | Efficient subsonic cruise |
| Fuselage | Slender tube + internal bay | Crew/avionics forward of bay |
| Empennage | Conventional fin + stabilizer | T-tail optional product decision |
| Gear | Tricycle, long-stroke | Runway ops; no carrier claim |

Stations / dimensions: `../interfaces/airframe.yaml`. Study OML: `../shell/airframe_study.scad`.

---

## 2. Avionics (conceptual)

| Partition | Role |
|-----------|------|
| FCC | Transport-class envelope stubs |
| Mission computer | Nav + bay door / SAFE-INHIBIT discretes — **no** weapons protocols |
| Sensors | Nav / weather / EO stub — no targeting employment |
| Crew | Dual optional vs single + autonomy aids |

KiCad bay boards are the next roadmap step.

---

## 3. Payload / bay (inert only)

| ID | Kind | Purpose |
|----|------|---------|
| BAY-MAIN | volume stub | Internal bay keep-out |
| PLD-INERT-A | mass/CG box | Training / inert shape class |
| PLD-INERT-B | mass/CG box | Alternate inert class |
| DOOR-SAFE | discrete stub | SAFE/INHIBIT only |

**SAFE / INHIBIT** (integration only — no arming or release of live stores):

| Condition | SAFE | INHIBIT bay release |
|-----------|------|---------------------|
| Ground maintenance | asserted | asserted |
| Weight-on-wheels | asserted | asserted |
| Inert present, no sim auth | asserted | asserted |
| Sim inert release auth | deasserted* | deasserted* |

\*Simulated inert only — **no** live munitions.

---

## 4. Propulsion interface

| Item | Baseline |
|------|----------|
| Class | High-bypass turbofan **class** |
| Count | Twin under-wing or rear-fuselage — product decision |
| Interfaces | Mounts, inlet capture stub, electrical/bleed offtakes |
| Not here | Cycle design, combustor detail, IR signature prediction |

---

## 5. Teaching cruise check

Classroom Breguet range stub and payload mass fraction: `cruise_examples.py` (not a survey product).

## 6. Next steps
KiCad, structural spars/ribs, Gerbers/STLs, BOM, polish.
