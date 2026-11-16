# Supersonic bomber — design note (B1 #39)

**Product:** ISM-XB-1 study  
**Regime:** supersonic cruise class (textbook M ≈ 1.5–3) — **not** hypersonic TPS (#37)

## Out of scope
Weapons boundary: inert payload only. No guidance, seekers, munition propulsion, warheads, fuzing, or employment. No scramjet / hypersonic TPS recipes here — see `hypersonic-bomber/docs/`.

---

## 1. Airframe layout (study)

| Feature | Baseline study choice | Rationale |
|---------|----------------------|-----------|
| Planform | Low-aspect swept or delta-ish | Wave-drag awareness at M>1 |
| Fuselage | Area-ruled slender body (qualitative) | Textbook Sears–Haack / area-rule hygiene |
| Inlets | Side or under-fuselage | Packaging vs bay volume — product decision |
| Empennage | Fin + all-moving stab or V-tail option | Later ICD |

Study OML: `../shell/airframe_study.scad`.

---

## 2. Avionics (conceptual)

Same partition idea as subsonic (#38): FCC safety-critical, MC owns bay/safeing discretes, nav/EO stubs without targeting employment. Bus topology TBD; may align patterns with `fighter-jet/interfaces/` later without copying weapons topics.

---

## 3. Thermal (cruise — not hypersonic TPS)

| Topic | B1 stance |
|-------|-----------|
| Kinetic heating | Present but milder than hypersonic; skin temperature rise is a materials/coatings **class** question |
| Hot spots | Leading edges, inlet lips, canopy — flag for materials note later |
| TPS | No ablative/reusable hypersonic TPS stack in this tree; point to #37 for educational hypersonic heat-shield classes |
| Avionics cooling | ECS / liquid cold-plate stubs when KiCad lands |

---

## 4. Propulsion interface

| Item | Baseline |
|------|----------|
| Class | Low-bypass turbofan or turbojet **class** with afterburner option (public class language) |
| Count | Twin — packaging preference for yaw on engine-out |
| Interfaces | Mounts, inlet duct keep-outs, nozzle clearance vs empennage |
| Not in B1 | Detailed cycle deck, plume IR prediction, or fuel chemistry |

---

## 5. Payload / bay
Internal inert bay volume reserved. Future stores work follows the fighter weapons boundary (integration / SAFE-INHIBIT only).

## 6. Next steps
KiCad, structure, Gerbers/STLs, BOM, validation — later PRs.
