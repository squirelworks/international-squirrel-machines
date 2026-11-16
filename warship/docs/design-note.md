# Warship design note — B2 (#43)

**Product:** ISM-WS-1 study (surface combatant class)  
**Hydrodynamics:** public-domain / textbook naval architecture only.

## Out of scope (hard limits)

- Weapons interfaces, fire control, combat-system internals
- Seeker / guidance / warhead / fuzing / arming content
- Export-controlled (ITAR/EAR) signatures, quieting, or combat data
- Acoustic / quieting design (see submarine B3 later)

Weapons and combat sensors exist in-repo **only** as mass and deck-footprint placeholders — see `../interfaces/mass-placeholders.yaml`.

---

## 1. Hull form (study)

| Feature | Baseline study | Notes |
|---------|----------------|-------|
| Type | Displacement monohull | Scale-model friendly; no stealth-faceting claims |
| L/B | ~7–8 | Slender combatant-class proportions (public encyclopedia order) |
| B/T | ~3 | Draft vs stability trade |
| Sections | Soft U midbody; finer entrance | Teaching fairing — not a classified hull |
| Appendages | Twin shaft stubs + rudder stub | Packaging only |

Study solid: `../shell/hull_study.scad` (mm study model; not structural authority).

---

## 2. Hydrostatics (textbook)

Displacement in seawater:

\[
\Delta = \rho \, \nabla
\]

with \(\rho \approx 1025\,\mathrm{kg/m^3}\) (standard seawater teaching value) and \(\nabla\) the molded submerged volume.

| Symbol | Meaning | Study use |
|--------|---------|-----------|
| \(\nabla\) | Displaced volume | From study offsets / prismatic estimate |
| \(\Delta\) | Mass displacement | \(\rho\nabla\) |
| LCB / VCB | Longitudinal / vertical center of buoyancy | Balance vs LCG / VCG |
| KB | Height of B above keel | Approximate midship section |
| BM | Metacentric radius \(\approx I_T / \nabla\) | Transverse inertia of waterplane / volume |
| GM | \(KM - KG\) with \(KM = KB + BM\) | Intact stability teaching metric |

Machine-readable stubs: `../interfaces/hydrostatics.yaml`.  
Recompute teaching table: `python3 warship/docs/hydrostatics_examples.py`.

**Citations:** Principles of Naval Architecture (SNAME) public teaching summaries; basic hydrostatics textbooks. No classified offsets.

---

## 3. Stability (intact, qualitative)

| Topic | B1/B2 stance |
|-------|----------------|
| Intact GM | Target positive GM with margin; numbers provisional in YAML |
| Free surface | Flag tanks as KG/GM modifiers later — not designed here |
| Damage stability | Out of B2 (requires subdivision plan) |
| Wind heeling | Qualitative note only |

Combat topside mass (radar houses, gun mounts as **boxes**) enters only through `mass-placeholders.yaml` → KG / footprint — not through fire-control models.

---

## 4. Propulsion / powering (interface level)

| Item | Baseline |
|------|----------|
| Class | Twin-shaft diesel or CODAG **class** (public naming) |
| Powering | Holtrop/Menon-style **order-of-magnitude** resistance later; B2 stores installed power stub only |
| Interfaces | Engine-room volume, shaft line keep-out, electrical MW-class bus stub |
| Not in B2 | Propeller detailed design, cavitation recipes, classified quieting |

---

## 5. Mass / footprint placeholders (weapons & combat sensors)

| Placeholder ID | Kind | Mass (t) | Footprint (m) | Role |
|----------------|------|----------|---------------|------|
| WP-GUN-FWD | Weapon mass box | 25 | 6 × 4 | Forward mount mass/KG only |
| WP-VLS-MID | Weapon mass box | 40 | 8 × 6 | Midships vertical-launch **mass** only — no cell internals |
| SEN-RADAR-MAIN | Combat sensor mass box | 12 | 5 × 5 × 8 H | Mast/radar house mass & windage box |
| SEN-EO-DIR | Combat sensor mass box | 2 | 1.5 × 1.5 × 2 H | Director mass only — no fire-control logic |
| SEN-SONAR-BOW | Sensor mass box | 15 | 4 × 3 × 3 | Bow dome mass/volume — no acoustic processing |

Authoritative rows: `../interfaces/mass-placeholders.yaml`.  
**Forbidden in this file family:** interfaces to weapons, FC loops, track files, engagement doctrine.

---

## 6. Carrier sibling
Flight-deck / aviation elevators as mass and area placeholders: `../../aircraft-carrier/docs/design-note.md` (same combat-system boundary). Full carrier roadmap remains [#45](https://github.com/squirelworks/international-squirrel-machines/issues/45).

## 7. Next steps (not B2)
KiCad nav/power/scale-model control, structure, Gerbers/STLs, BOM, validation.
