# Subsonic bomber — design note (B1 #38)

**Product:** ISM-SB-1 study  
**Regime:** high-subsonic cruise (textbook transport/bomber class — not a fighter)

## Out of scope
Weapons boundary: inert payload / bay integration only. No guidance, seekers, munition propulsion, warheads, fuzing, or employment.

---

## 1. Airframe layout (study)

| Feature | Baseline study choice | Rationale |
|---------|----------------------|-----------|
| Planform | High-aspect swept wing | Efficient subsonic cruise; long range packaging |
| Fuselage | Slender tube + dorsal/ventral bay volume | Separates crew/avionics from inert bay |
| Empennage | Conventional fin + stabilizer (or T-tail option) | Clear aft for propulsion; product decision later |
| Gear | Tricycle, long-stroke | Runway ops; no carrier claim in B1 |

Study OML: `../shell/airframe_study.scad` (proportions only).

---

## 2. Avionics (conceptual)

| Partition | Owner (study) | Notes |
|-----------|---------------|-------|
| Flight controls / FCC | Safety-critical | Envelope for transport-class Nz/AOA — later ICD |
| Mission computer | MC | Navigation, bay door/safeing discretes — **no** weapons protocols |
| Sensors | Nav / weather / EO stub | Navigation and situational awareness; no targeting employment |
| Crew stations | Optional dual | Product decision vs single pilot + autonomy aids |

Bay I/O patterns may later borrow fighter `fighter-jet/firmware/` host-stub ideas — separate tree.

---

## 3. Payload / bay (inert)

| Item | B1 stance |
|------|-----------|
| Bay | Internal volume reserved; doors are structural/thermal packaging only |
| Stores | Future inert class models only (mass/CG/clearance) |
| Safeing | Lab/ICD philosophy later — SAFE/INHIBIT only, same as fighter SMS boundary |

---

## 4. Propulsion interface

| Item | Baseline |
|------|----------|
| Class | High-bypass turbofan **class** (public encyclopedia thrust/SFC order-of-magnitude later) |
| Count | Twin under-wing or rear-fuselage — product decision |
| Interfaces | Mount hardpoints, inlet capture area stub, electrical/bleed offtakes TBD |
| Not in B1 | Cycle design, combustor detail, or IR signature prediction |

---

## 5. Next steps (not this PR)
KiCad avionics bay, structural spars/ribs, Gerbers/STLs, BOM, validation.
