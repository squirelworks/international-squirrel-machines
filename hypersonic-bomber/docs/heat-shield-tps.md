# Heat-shield / TPS classes — educational note (B1 #37)

**Companion:** `aerothermal-concepts.md`  
**Claim boundary:** material **classes** and textbook selection logic only — not a flight-cleared TPS stack-up for ISM-HB-1.

## Out of scope (hard limits)

- Exact proprietary coating recipes, fiber layups, or classified allowables
- Weapons, munitions, or warhead thermal design
- Propulsion combustor liners or fuel chemistry
- “How to defeat” any sensing or defense system

---

## 1. Three textbook TPS strategies

Public aerospace teaching material groups thermal protection roughly as:

| Class | Idea | Typical teaching context |
|-------|------|--------------------------|
| **Heat sink** | Absorb heat in a thick, high-conductivity skin; dump later | Short pulses; metallic leading edges in classroom examples |
| **Ablative** | Sacrifice outer material (pyrolysis / char / melt) to carry energy away | Entry capsules; high peak \(q\) with limited reuse |
| **Reusable radiative** | Hot structure or tiles that radiate \( \sigma \varepsilon T_w^4 \) at high \(T_w\) | Shuttle-era tile / RCC teaching examples; modern CMC discussions |

**Citations:** NASA educational TPS overviews; Bertin *Hypersonic Aerothermodynamics*; Anderson high-temperature chapters. Specific flight-vehicle numbers are **not** copied as ISM design requirements.

---

## 2. Material classes (public)

| Class | Role in teaching notes | Notes for ISM study |
|-------|------------------------|---------------------|
| Carbon–carbon (C/C) | High-temperature structural / leading-edge class | Class name only; no proprietary weave |
| Ceramic-matrix composite (CMC / SiC-class) | Reusable hot-structure candidate class | Public literature class |
| Refractory metals / coated metals | Heat-sink or locally protected edges | Oxidation coatings are a research topic — no recipes here |
| Ablator families (phenolic / PICA-class names in public lit) | Single-use high-enthalpy teaching | Cite public NASA/encyclopedia class names only |
| Insulating tiles / blankets | Reusable acreage TPS teaching | Geometry packaging, not coating chemistry |

ISM product IDs (when assigned later) will be original; class references seed **education**, not copies of national vehicle stack-ups.

---

## 3. Product-decision questions (qualitative)

| Decision | Aerothermal driver | Structural / mass tension |
|----------|--------------------|---------------------------|
| Sharp vs blunt nose | Peak \(q\) vs drag | Blunt helps heat; hurts L/D |
| Acreage reusable vs ablative nose cap | Pulse duration / reuse goals | Ablative mass vs turnaround |
| Leading-edge material class | Local \(T_w\) and oxidation | Attach fittings into cool structure |
| Control-surface edges | Shock impingement heating | Actuation keep-outs (later systems notes) |

No row implies a weapons or employment choice.

---

## 4. Study OML link

`shell/blunt_cone_study.scad` is a parametric blunt sphere-cone for **TPS packaging sketches** (nose radius, cone angle). It is not a bomber weapons airframe and carries no stores geometry.
