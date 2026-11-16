# Hypersonic bomber — design note (#37 deepen)

**Product:** ISM-HB-1 study  
**Scope:** educational **aerothermal** and **heat-shield / TPS class** language only.  
**Prior:** B1 notes + stagnation examples; this revision adds interfaces and a teaching heat-flux check.

## Out of scope (hard limits)

- Weapons, munitions, guidance, seekers, warheads, fuzing, arming, employment
- Scramjet / propulsion design recipes or vehicle performance prediction
- Export-controlled (ITAR/EAR) TPS formulations or classified allowables
- CFD recipes tuned to a named operational vehicle

Detail narratives: `aerothermal-concepts.md`, `heat-shield-tps.md`.

---

## 1. Aerothermal teaching stack

| Layer | Content |
|-------|---------|
| Stagnation temperature | Perfect-gas \(T_0 = T_\infty(1+\frac{\gamma-1}{2}M^2)\) — `stagnation_examples.py` |
| Heat flux class | Cold-wall order-of-magnitude stub — `heat_flux_examples.py` |
| Bluntness | Sphere-cone nose radius vs peak heating (qualitative) |
| Machine-readable | `../interfaces/aerothermal.yaml` |

---

## 2. TPS classes (placeholders)

| Class | Teaching role |
|-------|---------------|
| Heat sink | Short-pulse metallic leading-edge class |
| Ablative | High-peak \(q\) single-use class |
| Reusable radiative | Tile / CMC / hot-structure class |

No proprietary weaves, coatings, or ITAR stack-ups. See `../interfaces/tps-placeholders.yaml`.

---

## 3. Geometry study

`../shell/blunt_cone_study.scad` — blunt sphere-cone with an outer **TPS shell offset** (packaging sketch only).

## 4. Next steps
KiCad (if any ECS/sensors), structural design beyond study OML, Gerbers/STLs, BOM, polish — still without weapons or propulsion recipes.
