# Signature-related product-decision tradeoffs (A3 #121)

Qualitative **considerations only**. No RCS/IR numbers for ISM-FJ-1. No operational employment content.

Companion explainer: `signatures-concepts.md`. Sources: Knott; Jenn; Raymer; Mahulikar et al. (see that note).

## Trade table

| Existing ISM decision | Signature consideration (textbook language) | Conflicts / notes | Related docs |
|----------------------|---------------------------------------------|-------------------|--------------|
| **External stores on STA-1…9** vs future internal bay | External shapes add specular faces, edges, and local cavities; an internal bay trades structural volume and doors for a cleaner cruise OML | Bay volume fights fuel, landing gear, and avionics packaging | `hardpoints`, stores integration |
| **Twin side/under inlets** (A2 packaging) | Inlets are textbook **cavities**; line-of-sight into the duct and lip edges matter in shaping hygiene | Duct routing already constrained by bay and gear wells | `propulsion.yaml`, `propulsion_keepouts.scad` |
| **Twin vs single engine** (open product decision) | Twin widens aft body and duplicates nozzle cavities; single narrows aft wetted area but removes asymmetric-thrust backup | See twin-vs-single mass/CG/wetted deltas — not signature metrics | `twin-vs-single.md` |
| **Variable-geometry nozzle stub** | Aft hot parts and plume are textbook IR contributors; stub keeps article FADEC/nozzle detail out of scope | No countermeasure-framed suppression design (A3 hard limit) | `propulsion.md` |
| **Transparent canopy + HUD volume** | Canopy is both a specular surface and a cavity; optics/FOV pull against aggressive faceting | Crew vision and HMI win unless product decision revisits canopy | avionics HMI notes |
| **Dorsal avionics hatch (FS-48)** | Panel breaks are edge/discontinuity contributors when open or poorly sealed | Maintainability wants large hatch | `maintainability.md` |
| **NLG/MLG wells** | Open wells are cavities; doors add edges when closed | Carrier/land gear envelopes dominate | `mechanical-airframe.yaml` |
| **Quartz/epoxy radome callout** | Nose transparency vs structural shaping — materials note only; no frequency-specific treatment design | Keep treatments out of scope | `materials/` |
| **Wing LE sweep ~35° (study)** | Sweep supports edge-alignment hygiene in planform terms | Sweep also serves aero/structural product goals | `aircraft-geometry`, OpenVSP params |
| **ISM badge / fin detail** | Small protrusions are minor edge/specular clutter at conceptual level | Branding stays; avoid adding large irregular fairings | shell / branding |

## Product-decision list (for Sarah / Victor)

Carry these as **open or watched** trades — still no performance claims:

1. External carriage vs internal bay timing.
2. Twin vs single propulsion packaging (already open).
3. Inlet placement vs bay/gear keep-outs vs cavity hygiene.
4. Canopy faceting vs pilot FOV / HUD.
5. Nozzle/aft treatment stays textbook-only unless a future brief reopens scope under the same hard limits.

## Out of scope reminder

No observability-reduction narrative against sensing systems, no wavelength-specific treatments, no real-aircraft signature numbers, no tactics. See `signatures-concepts.md` Out of scope.
