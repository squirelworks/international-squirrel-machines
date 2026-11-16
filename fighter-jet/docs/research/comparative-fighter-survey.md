# Comparative Fighter Programme Survey (Public Sources)

**Issue:** [#95](https://github.com/squirelworks/international-squirrel-machines/issues/95)  
**Citations file:** `citations.yaml`  
**Purpose:** Extract *problem classes* and design lessons for ISM-FJ-1 “Nutcracker”. Contemporaries are **reference only** — do not copy proprietary geometry, pinouts, or classified data (`docs/design-principles.md`).

Themes per programme: airframe layout · materials · carrier variants · engines (high level) · lessons for ISM.

---

## Russia

**Representative types (public):** Su-27/30/35 “Flanker” family; Su-33 carrier Flanker; Su-57 LO twin-engine fighter (developmental/limited production in open literature).

| Theme | Public takeaway | Cite |
|-------|-----------------|------|
| Layout | Large twin-engine air superiority / multirole planforms; heavy external load; large signatures on legacy Flankers | rusi-ru-cn-2019, wiki-su57 |
| Materials | Legacy metal-primary Flankers; later types increase composites (public reporting varies — treat as trend, not allowables) | rusi-ru-cn-2019 |
| Carrier | Su-33 / MiG-29K class naval fighters for ski-jump carriers in open sources | rusi-ru-cn-2019 |
| Engines | Twin low-bypass turbofans; thrust vectoring discussed publicly on some Flanker/Su-57 variants | wiki-su57 |

**Lesson for ISM:** Twin-engine redundancy and long-range internal fuel are proven multirole enablers; legacy large-RCS layouts argue for ISM to keep signature/materials trades explicit even on a non-stealth-first product story. Carrier ops need dedicated gear/hook load paths (#93) — not shore gear with a hook bolted on.

---

## China

**Representative types (public):** J-11/J-16 Flanker-derived; J-20 LO fighter; J-15 carrier type.

| Theme | Public takeaway | Cite |
|-------|-----------------|------|
| Layout | Rapid iteration from Flanker derivatives to LO canard/delta (J-20); carrier Flanker derivative (J-15) | rusi-ru-cn-2019, wiki-j20, wiki-j15 |
| Materials | Open analyses credit increased composites and modern avionics on Chinese Flanker derivatives vs older Russian baselines | rusi-ru-cn-2019 |
| Carrier | Dedicated carrier fighter line (J-15) in open sources; future carrier LO types discussed publicly but not used as ISM SoT | wiki-j15 |
| Engines | Twin-engine for heavy fighters; indigenous engine maturation is a recurring public theme | rusi-ru-cn-2019 |

**Lesson for ISM:** Separate *land* and *carrier* structural cases early (ISM already tracks this in #93). Composites + modern sensors on a Flanker-class airframe show materials/avionics upgrades can outpace pure kinematic growth — aligns with ISM hybrid Al/CFRP baseline (#92).

---

## France

**Representative type (public):** Dassault Rafale (B/C land; M naval).

| Theme | Public takeaway | Cite |
|-------|-----------------|------|
| Layout | Close-coupled canard + delta; single-fin twin-engine omnirole | dassault-rafale-2023, wiki-rafale |
| Materials | OEM states composites ≈ **70% of wetted area**; improved empty-to-MTOW ratio vs traditional Al/Ti airframes | dassault-rafale-2023 |
| Carrier | Rafale M shares airframe/mission system with land variants; differences “mainly” undercarriage + arresting hook (OEM) | dassault-rafale-2023 |
| Engines | Twin Snecma/Safran M88-class turbofans (high-level public) | wiki-rafale |

**Lesson for ISM:** **Common airframe + naval deltas** (gear, hook, structure beef-up) is the right pattern for ISM twin-engine baseline — matches `carrier-suitability.md` / `carrier-loads.yaml`. Aggressive CFRP wetted area supports ISM skin/composite direction without forcing all-composite wing box (still a product decision).

---

## Germany (+ Eurofighter partners)

**Programme:** Eurofighter Typhoon — partner nations **Germany, UK, Spain, Italy**; industry Airbus / BAE Systems / Leonardo.

| Theme | Public takeaway | Cite |
|-------|-----------------|------|
| Layout | Twin-engine canard-delta, aerodynamically unstable, carefree FBW | eurofighter-aircraft, ef-tecguide-2013, wiki-typhoon |
| Materials | Public programme materials: ~70% carbon-fibre composite surface, ~12% GRP, ~15% metal, ~3% other | ef-tecguide-2013, eurofighter-features |
| Carrier | Land/shore based; not a catapult/arrest carrier type in partner service | eurofighter-programme |
| Engines | Twin Eurojet **EJ200** — dry ~60 kN class, reheat ~90 kN class (public TecGuide) | ef-tecguide-2013, eurofighter-features |

**Lesson for ISM:** Quadruplex digital FBW + unstable airframe is mainstream for agile twins — reinforces ISM FBW baseline (`flight-controls/`). High composite fraction validates CFRP skins; metal retained at hot/high-load edges (aligns with ISM-Ti / Al fittings). Multi-nation workshare is an industrial lesson, not an ISM geometry template.

---

## United Kingdom

**In-service / partnership lens (public):** Eurofighter Typhoon partner; future combat air with **GCAP** (UK–Italy–Japan) in open literature; historic naval Phantom/Sea Harrier eras are out of current survey scope except as carrier problem-class reminders.

| Theme | Public takeaway | Cite |
|-------|-----------------|------|
| Layout | Typhoon as above; GCAP/Tempest discussed as next-gen crewed fighter with collaborative combat aircraft (high-level only) | eurofighter-programme, wiki-gcap, iiss-eu-combat-2022 |
| Materials | Typhoon composite-heavy airframe; UK industry deep in composites/engines | eurofighter-features |
| Carrier | Current Typhoon not RN carrier fighter; UK carrier air today is F-35B (STOVL) in open sources — different problem class than ISM hook/catapult track | wiki-typhoon |
| Engines | EJ200 (Typhoon); public UK–Japan engine demonstrator cooperation for future fighters | iiss-eu-combat-2022 |

**Lesson for ISM:** Do not confuse **STOVL** carrier solutions with ISM’s arresting-hook / catapult load cases (#93). Twin-engine + FBW carefree handling remains the transferable Typhoon lesson. Future-programme politics (GCAP vs other EU efforts) are background only.

---

## Japan

**Representative types (public):** Mitsubishi **F-2** (F-16-derived); F-35A/B induction; GCAP partnership with UK/Italy.

| Theme | Public takeaway | Cite |
|-------|-----------------|------|
| Layout | F-2: single-engine, enlarged wing vs F-16 baseline for payload/range/STOL emphasis | mhi-f2, gao-f2-1997, wiki-f2 |
| Materials | Co-cured **composite wing** highlighted by MHI/GAO; composites ~20% empty weight class in open summaries | mhi-f2, gao-f2-1997 |
| Carrier | F-2 land-based; Japan F-35B for Izumo-class conversion discussed publicly (STOVL) — again distinct from ISM catapult/arrest | wiki-f2 |
| Engines | F-2: GE F110-class single; future GCAP propulsion cooperation with UK industry (public) | gao-f2-1997, iiss-eu-combat-2022 |

**Lesson for ISM:** Co-cured / highly integrated composite wing boxes are a manufacturability and repair trade — ISM’s open product decision (hybrid Al caps vs all-CFRP box) should weigh depot repair like Japan’s F-2 experience suggests. Single-engine F-2 shows a viable light fighter path; ISM baseline remains **twin** for asymmetric-thrust backup unless product decision flips.

---

## Cross-cutting comparison (high level)

| Topic | Pattern seen publicly | ISM-FJ-1 stance |
|-------|----------------------|-----------------|
| Twin vs single | Twins dominate heavy/omnirole & carrier conventional; singles for lighter F-16-class | Twin baseline; single documented alternate |
| Canard-delta vs aft-tail | Rafale/Typhoon canard-delta; Flanker/J-20/Su-57 aft-tail or canard-LO mixes | ISM original mid-swept + single fin (not a Rafale/Typhoon copy) |
| Composites | 70%-class wetted area claims (Rafale/Typhoon public) | CFRP skins + hybrid box (#92) |
| Carrier | Common airframe + gear/hook deltas (Rafale M) vs dedicated naval Flanker (J-15/Su-33) vs STOVL (F-35B) | Conventional hook/catapult path (#93) |
| FBW | Carefree quadruplex common on Eurocanards | Quadruplex FBW baseline |

---

## Lessons for ISM (actionable)

1. **Keep twin-engine + FBW** as the Nutcracker baseline; document single-engine only as an alternate (already in README).
2. **Push composites on skins/surfaces**; retain Ti/Al at gear, hook, carry-through fittings — matches public Rafale/Typhoon mixes and #92 zone map.
3. **Carrier = structural programme**, not a kit: Rafale-style commonality with gear/hook deltas; load cases already in `interfaces/carrier-loads.yaml`.
4. **Do not import STOVL** geometry or propulsion into ISM-FJ-1 without a separate product decision.
5. **Original planform:** survey informs trades; OpenSCAD/diagrams remain ISM proportions (DWG-010…070) — no tracing.
6. **Engines stay ICD-level** until a propulsion vendor story freezes (`mechanical/propulsion.md`).

## Acceptance (#95)
- [x] `fighter-jet/docs/research/` index README
- [x] Survey covering Russia, China, France, Germany/Eurofighter partners, UK, Japan
- [x] Citations (narrative + `citations.yaml`)
- [x] Explicit lessons for ISM; no proprietary CAD copy
