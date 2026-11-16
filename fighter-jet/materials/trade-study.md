# Materials Trade Study — ISM-FJ-1

**Issue:** [#92](https://github.com/squirelworks/international-squirrel-machines/issues/92) · Related [#71](https://github.com/squirelworks/international-squirrel-machines/issues/71)  
**Machine-readable zone map:** `../interfaces/materials-zones.yaml`  
**Candidate scores:** `candidates.yaml`

Public alloy *families* are reference only. ISM designations (`ISM-Ti-6`, `ISM-Al-7xxx`, …) are internal product choices — not claimed OEM equivalents.

## Criteria (1–5 scores; higher is better for the program)

| Criterion | Meaning for ISM-FJ-1 |
|-----------|----------------------|
| Strength-to-weight | Specific strength / stiffness for flight structure |
| Temperature | Useful strength after soak (avionics bay → nozzle-adjacent) |
| Fatigue | Hole / spectrum fatigue friendliness |
| Carrier/salt corrosion | Arrestment/deck salt, hold-down, wet bilge paths |
| Cost | Raw + buy-to-fly + machining |
| Manufacturability | Forming, machining, bonding, field repair |

## Candidate families

| ID | Family (public ref) | Typical ISM use |
|----|---------------------|-----------------|
| `ISM-Ti-6` | Ti-6Al-4V class | Gear, fittings, hook/keel fittings, hot-adjacent |
| `ISM-Al-2xxx` | 2xxx Al (e.g. 2024-class) | Fatigue-critical skins/panels where toughness matters |
| `ISM-Al-7xxx` | 7xxx Al (e.g. 7075-class) | High-strength bulkheads, spar caps (hybrid baseline) |
| `ISM-Al-Li` | Al-Li class | Weight-critical spar caps / fuselage where cost allows |
| `ISM-Steel-HS` | High-strength steel (300M-class ref) | Gear legs / arresting hook alternate; cost lever |
| `ISM-CFRP-A` | Carbon/epoxy | Skins, ribs, surfaces, fin |
| `ISM-RF-Q` | Quartz/epoxy | Radome |
| `ISM-Ni-HT` | Ni / high-temp stub | Firewall / nozzle-adjacent panels |

## Score matrix (design judgment — provisional)

Scores are **ISM program judgments** for conceptual selection, not coupon data. Replace after #78 validation.

| Candidate | S/W | Temp | Fatigue | Salt/carrier | Cost | Mfg | Notes |
|-----------|-----|------|---------|--------------|------|-----|-------|
| ISM-Ti-6 | 5 | 4 | 4 | 5 | 2 | 2 | Prefer fittings, gear, hook path |
| ISM-Al-2xxx | 3 | 2 | 4 | 2 | 4 | 4 | Fatigue skins; needs coating system |
| ISM-Al-7xxx | 4 | 2 | 3 | 2 | 4 | 4 | Hybrid spar caps / bulkheads baseline |
| ISM-Al-Li | 5 | 2 | 3 | 2 | 3 | 3 | Weight win; supply/repair maturity watch |
| ISM-Steel-HS | 3 | 3 | 4 | 2 | 5 | 3 | Hook/gear cost option; corrosion care |
| ISM-CFRP-A | 5 | 2* | 4 | 4† | 3 | 3 | *resin Tg limit †with seal/isolation |
| ISM-RF-Q | 2 | 2 | 3 | 3 | 3 | 3 | RF first; not primary structure |
| ISM-Ni-HT | 2 | 5 | 3 | 4 | 1 | 2 | Hot bay only |

\* CFRP temperature limited by resin system; not metal melt.  
† Galvanic isolation required at CFRP–Al joints (see `metallurgy-composites.md`).

## Zone recommendations (baseline)

| Zone | Primary | Alternate | Rationale |
|------|---------|-----------|-----------|
| Radome | ISM-RF-Q | — | RF transparency |
| Forward fuselage skins | ISM-Al-2xxx + CFRP panels | Al-Li panels | Fatigue + repair access |
| Pressure bulkheads | ISM-Al-7xxx | ISM-Al-Li | Strength + machined frames |
| Avionics bay trays | Al honeycomb / CFRP | — | Stiffness + thermal path |
| Wing skins | ISM-CFRP-A | — | S/W, fatigue |
| Wing spar caps | ISM-Al-7xxx | ISM-Al-Li / CFRP | Hybrid baseline (# product decision) |
| Wing spar webs / ribs | ISM-CFRP-A | Al sheet ribs | Shape + mass |
| Carry-through fittings | ISM-Ti-6 | — | Side-of-body loads |
| Landing gear | ISM-Ti-6 | ISM-Steel-HS | Corrosion vs cost |
| Arresting hook / keel fittings | ISM-Ti-6 | ISM-Steel-HS | Carrier track #93 |
| Empennage skins | ISM-CFRP-A | — | Flutter mass |
| Aft / hot structure | ISM-Ti-6 + ISM-Ni-HT | — | Heat |
| Fasteners (into CFRP) | Ti / CRES | — | Galvanic |

## Carrier / salt emphasis
Naval suitability (#93) biases **Ti** for gear, hook, and keel fittings; demands sealed dissimilar joints and chromate-free primer path on Al. Steel hook/gear remains a **cost alternate** with explicit corrosion maintenance burden in `materials-zones.yaml`.

## Acceptance (#92)
- [x] Trade-study note with criteria matrix
- [x] Machine-readable zone→material table (`interfaces/materials-zones.yaml`)
- [x] Cross-links from structure / metallurgy docs
- [x] Carrier/salt corrosion column present
