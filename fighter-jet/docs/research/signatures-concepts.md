# Signature concepts — textbook design rationale (A3 #121)

**Audience:** ISM designers who need plain-language *why* shaping and packaging choices matter.  
**Level:** standard textbooks / peer-reviewed reviews only.  
**Claim boundary:** nothing here is a signature prediction for ISM-FJ-1. Numbers are canonical-shape **teaching examples** only.

## Out of scope (hard limits)

This note does **not** cover:

- Any guidance on reducing observability against a named or classed sensing system.
- Operational employment detail (tactics, mission planning, geometry of opposing forces).
- Absorber / coating formulations, wavelength-specific treatments, or measurement/prediction of real aircraft.
- Plume or nozzle treatments framed as countermeasure design (plume stays at textbook heat-transfer level).
- Export-controlled (ITAR/EAR) technical data, classified material, or “derived from leaks” sources.

**Sign-off:** Sarah or Victor reviews this section before merge (acceptance criterion).

---

## 1. What textbooks call out as main RCS contributors

Radar cross section (RCS) is a far-field scattering measure for a body illuminated by an electromagnetic wave. Standard texts (Knott, Shaeffer & Tuley; Jenn) group fighter-class contributions roughly as:

| Mechanism | Plain words | Typical places on a generic fighter-class shape |
|-----------|-------------|--------------------------------------------------|
| **Specular** | Mirror-like bounce from a smooth face when the face is nearly normal to the line of sight | Flat skins, canopy facets, control-surface faces |
| **Edge / tip** | Diffraction from discontinuities (leading/trailing edges, panel breaks, tips) | Wing/fin edges, inlet lips, door gaps |
| **Cavity** | Energy that enters an opening, bounces inside, and re-radiates | Inlets, exhaust cavities, open gear wells, canopy volume |
| **Creeping / traveling wave** | Energy that travels along a curved surface and sheds from the far side or from discontinuities | Rounded fuselage, ogives, long smooth bodies |

Creeping-wave language is textbook electromagnetics (Knott/Jenn chapters on asymptotic methods); it is not an operational claim about any particular aircraft.

**Citations:** Knott et al., *Radar Cross Section*, 2nd ed., SciTech/IET (2004), introductory / mechanisms chapters. Jenn, *Radar and Laser Cross Section Engineering*, 2nd ed., AIAA (2005), DOI 10.2514/4.477027, conceptual shaping chapters.

---

## 2. Shaping principles vs the current ISM OML

Raymer’s conceptual survivability notes and the RCS texts agree on **general** geometric hygiene (not a performance guarantee):

| Principle (textbook) | Compatible with current ISM OML? | Tension with other ISM decisions |
|----------------------|----------------------------------|----------------------------------|
| Prefer continuous slopes; avoid large surfaces that face many look angles at once | Partially — swept wing LE (~35°) and tapered aft body help | Flat canopy / HUD optics want transparency and FOV, not aggressive faceting |
| Align major edges (wing, inlet lip, panel lines) where practical | Partially — wing LE sweep is a single dominant family | External stores on STA-1…9 add their own edges and cavities unless carried flush/internal |
| Avoid deep right-angle dihedral corners in the plan/side silhouette | Study shell is soft-faired; still watch wing–fuse join | Carry-through and gear wells force structural corners |
| Treat inlets and canopy as **cavities** | Side/under intakes + dorsal bay hatch are called out as packaging constraints (A2) | Side intakes trade LO hygiene vs bay/gear packaging; canopy is a cavity + specular surface |
| Hide hot / complex aft hardware in the body where possible | Twin nozzles are aft stubs (A2) | Twin layout widens aft body; single-engine alternate shrinks it (trade only) |

**Citations:** Raymer, *Aircraft Design*, 6th ed., AIAA, DOI 10.2514/4.104909 (survivability / signature considerations at conceptual level). Knott; Jenn (shaping chapters).

---

## 3. Canonical-shape teaching examples (analytic)

These are the usual first-course physical-optics / optical-region identities. They are **not** ISM-FJ-1 estimates. Analytic recomputation: `canonical_rcs_examples.py` (must match to 3 significant figures).

### 3.1 Perfectly conducting sphere (optical-region geometric cross section)

\[
\sigma_{\mathrm{sphere}} = \pi a^{2}
\]

Worked example: \(a = 1.00\,\mathrm{m}\) → \(\sigma = 3.14\,\mathrm{m}^{2}\).

**Citation:** Knott et al.; Jenn — sphere as the canonical calibration / teaching body.

### 3.2 Flat plate, normal incidence (physical optics)

\[
\sigma_{\mathrm{plate}} = \frac{4\pi A^{2}}{\lambda^{2}}
\]

where \(A\) is plate area and \(\lambda\) is free-space wavelength (a free parameter in the worked example — **no band name**).

Worked example: \(A = 1.00\,\mathrm{m}^{2}\), \(\lambda = 0.0300\,\mathrm{m}\) → \(\sigma = 1.40\times 10^{4}\,\mathrm{m}^{2}\).

**Citation:** Knott et al.; Jenn — flat-plate PO normal-incidence identity.

### 3.3 Circular cylinder, broadside (optical / PO teaching form)

A common textbook broadside form for a finite circular cylinder of radius \(a\) and length \(L\) is:

\[
\sigma_{\mathrm{cyl}} \approx \frac{2\pi a L^{2}}{\lambda}
\]

Worked example: \(a = 0.500\,\mathrm{m}\), \(L = 2.00\,\mathrm{m}\), \(\lambda = 0.0300\,\mathrm{m}\) → \(\sigma = 419\,\mathrm{m}^{2}\).

**Citation:** Knott et al.; Jenn — cylinder examples in optical / PO chapters (teaching form; exact series solutions are richer).

---

## 4. Infrared — qualitative textbook picture

Mahulikar, Sonawane & Rao’s review and heat-transfer textbooks describe aerospace-vehicle IR in **qualitative** buckets (no countermeasure design):

| Contributor | Qualitative role |
|-------------|------------------|
| **Hot metal / hot parts** | Exposed turbine / nozzle hardware and other high-temperature solids emit strongly; view factors and local temperature dominate |
| **Plume** | Exhaust gases emit and can be mixed/cooled by entrainment; chemistry and temperature matter at the textbook heat-transfer level |
| **Skin heating** | Aerodynamic heating and solar load raise skin temperature; emissivity and paint/finish change how much leaves the surface |

ISM uses this only as packaging rationale language (e.g. “nozzle is a stub; plume notes stay textbook”). **No** suppression architecture aimed at any sensing system.

**Citation:** Mahulikar, Sonawane & Rao, “Infrared signature studies of aerospace vehicles,” *Progress in Aerospace Sciences* 43 (2007), DOI 10.1016/j.paerosci.2007.06.002 — general review sections only.

---

## 5. How to read this next to the survey

The comparative survey mentions LO layouts at encyclopedia level for context. Those mentions are **not** sources for shaping rules here. Shaping language in this note comes only from the verified textbooks/review above.

---

## References (verified)

| ID | Work |
|----|------|
| knott-rcs-2004 | Knott, Shaeffer & Tuley, *Radar Cross Section*, 2nd ed., SciTech/IET (2004) |
| jenn-rlcse-2005 | Jenn, *Radar and Laser Cross Section Engineering*, 2nd ed., AIAA (2005), DOI 10.2514/4.477027 |
| mahulikar-ir-2007 | Mahulikar et al., *Prog. Aerosp. Sci.* 43 (2007), DOI 10.1016/j.paerosci.2007.06.002 |
| raymer-ads | Raymer, *Aircraft Design*, 6th ed., AIAA, DOI 10.2514/4.104909 |
