# ISM-FJ-1 product decisions — FROZEN

**Status:** **FROZEN** 2026-11-17 — user approved D1–D5.  
**Freeze date:** 2026-11-17  
**Related:** `../README.md`, `docs/devices/fighter-jet.md`; trades in `research/twin-vs-single.md`, `materials/trade-study.md`, `hydraulics/architecture.md`, `mechanical/airframe.md`.

Soft Flight Lab (#79) and Soft HIL UI (#80) remain **Steve’s lane** — Soft inquire gates stay unticked until Soft accepts or waives.

---

## D1 — Twin vs single engine

| Field | Value |
|-------|-------|
| **FROZEN** | **Twin** low-bypass turbofan (side-by-side, FS-82–95) |
| Alternatives | Single centerline turbofan of matched wet class |
| Rationale | Asymmetric-thrust backup after engine-out; multirole payload / ferry margin; matches in-tree propulsion packaging and station drawings |
| Impacts | Higher empty mass and aft wetted area vs single; twin keep-outs and dual rails in `propulsion.yaml` / OpenSCAD; single alternate keeps Δmass / ΔCG / Δwetted table in `research/twin-vs-single.md` |
| Sources | `mechanical/propulsion.md`, `docs/research/twin-vs-single.md`, `docs/research/engine-class-bounds.md` |

**Approval:** ☑ approved · ☐ revise · ☐ deferred — frozen 2026-11-17  

---

## D2 — Empty-weight / scale class

| Field | Value |
|-------|-------|
| **FROZEN** | **Conceptual full-size air vehicle** for FS/WS tables and mass properties, with a **reduced-scale study shell** (`shell/airframe.stl`) for fab/print fit checks |
| Alternatives | Study-only scale as SoT (no full-size FS tables); or lock a specific empty-weight / length class band now |
| Rationale | Keeps Flight Lab / viability ladders usable at vehicle class while Gerbers/STL remain educational study articles; Eric scale-model targets stay under `geometry/scale-model/` |
| Impacts | Full-scale FEA/CFD and production tooling remain next-cycle; empty-weight number stays provisional until class is approved |
| Sources | `README.md` working assumptions, `docs/viability.md`, `geometry/` |

**Approval:** ☑ approved · ☐ revise · ☐ deferred — frozen 2026-11-17  

---

## D3 — Wing box: all-composite vs hybrid

| Field | Value |
|-------|-------|
| **FROZEN** | **Hybrid** — Al-7xxx / Al-Li spar caps + CFRP webs/skins (zone map baseline) |
| Alternatives | All-composite wing box (CFRP spars + skins) |
| Rationale | Matches materials trade (#92) damage-tolerance / attach-fitting practicality for carry-through; carrier/salt mitigation paths already written for hybrid metal fittings |
| Impacts | Materials zones and allowables stay hybrid-keyed; all-composite would reopen spar-cap allowables and fitting callouts |
| Sources | `materials/trade-study.md`, `materials/README.md`, `interfaces/materials-zones.yaml` |

**Approval:** ☑ approved · ☐ revise · ☐ deferred — frozen 2026-11-17  

---

## D4 — Horizontal tail: all-moving vs separate elevator

| Field | Value |
|-------|-------|
| **FROZEN** | **All-moving HT** with geared-tab stub |
| Alternatives | Conventional stabilizer + separate elevator |
| Rationale | Aligns FBW pitch law and hinge-moment path already documented (FS-92 pivot); fewer surface splits for EHA packaging |
| Impacts | Empennage spars / HT hinge at FS-92; control-laws pitch row stays all-moving; elevator alternate would need surface map + actuator revisits |
| Sources | `mechanical/airframe.md`, `mechanical/control-surfaces.md`, `flight-controls/control-laws.md` |

**Approval:** ☑ approved · ☐ revise · ☐ deferred — frozen 2026-11-17  

---

## D5 — Landing-gear retract: electric vs EHA

| Field | Value |
|-------|-------|
| **FROZEN** | **Electric linear** retract for gear / NWS / wing-fold; **EHA remains baseline for primary flight controls only** |
| Alternatives | EHA retract for gear as well; or mixed |
| Rationale | Keeps pressurized fluid localized to surface EHA packs (no long hydro runs into gear bays); matches hydraulics architecture preference |
| Impacts | Gear actuators on 28 V utility bus; FBW still commands via bay I/O / FCC; choosing gear-EHA would add fluid routing into gear wells |
| Sources | `hydraulics/architecture.md`, `hydraulics/README.md`, `mechanical/landing-gear.md` |

**Approval:** ☑ approved · ☐ revise · ☐ deferred — frozen 2026-11-17  

---

## Explicit non-decisions (this file)

- Soft MVP / HIL acceptance — **Steve** (#79 / #80)
- Coupon allowables replacing provisional Ftu/Fty — materials campaign
- Livery accent / renders — branding decision
- Inquire-for-release sign-off — Sarah / program after Soft waive or accept

## Weapons boundary (unchanged)

Stores / weapons remain **mass / footprint / SAFE / INHIBIT** only. No seekers, guidance, munition propulsion, warheads, fuzing, or arming codes.
