# Hypersonic aerothermal concepts — educational note (B1 #37)

**Audience:** ISM designers who need plain-language *why* heat load and nose bluntness matter.  
**Level:** standard textbooks / public NASA educational material only.  
**Claim boundary:** nothing here is a trajectory, signature, or vehicle performance prediction for ISM-HB-1.

## Out of scope (hard limits)

This note does **not** cover:

- Weapons, munitions, guidance, seekers, warheads, fuzing, or targeting
- Operational employment or mission planning
- Propulsion cycle design (scramjet internals, fuel chemistry recipes)
- Classified or export-controlled thermal-protection formulations
- CFD recipes tuned to a named operational vehicle

---

## 1. What “hypersonic” means for heat

Textbooks usually reserve **hypersonic** for flight where Mach number \(M \gtrsim 5\) and real-gas / high-enthalpy effects start to matter for **heating**, not only for compressible aerodynamics (Anderson; Bertin).

At those speeds, kinetic energy of the freestream converts to thermal energy near the body. Designers care about:

| Quantity | Plain words | Why it matters |
|----------|-------------|----------------|
| Stagnation temperature | Temperature reached if flow is brought isentropically to rest | Sets an upper bound on gas temperature at the nose |
| Stagnation / recovery enthalpy | Energy per mass available to heat the surface | Drives heat flux into the skin / TPS |
| Heat flux \(q\) | Power per area into the wall | Sizes TPS thickness and mass |
| Wall temperature \(T_w\) | Surface temperature the structure/TPS must survive | Material and coating class selection |

**Citations:** Anderson, *Hypersonic and High-Temperature Gas Dynamics*, AIAA. Bertin, *Hypersonic Aerothermodynamics*, AIAA.

---

## 2. Teaching example — isentropic stagnation temperature

For a perfect gas with ratio of specific heats \(\gamma\) and freestream static temperature \(T_\infty\):

\[
T_0 = T_\infty \left(1 + \frac{\gamma-1}{2} M^2\right)
\]

This is a **classroom identity**, not a vehicle prediction. Real hypersonic flow has shocks, dissociation, and non-equilibrium chemistry; textbooks introduce those after the perfect-gas form (Anderson high-temperature chapters).

| \(M\) | \(T_\infty\) (K) | \(\gamma\) | \(T_0\) (K) |
|-------|------------------|------------|-------------|
| 5 | 220 | 1.4 | 1320 |
| 8 | 220 | 1.4 | 3040 |
| 10 | 220 | 1.4 | 4620 |

Recompute with `python3 hypersonic-bomber/docs/stagnation_examples.py` (3 sig figs).

---

## 3. Nose bluntness and heat flux (qualitative)

A classic teaching result: for a given freestream, a **blunter** nose lowers peak convective heat flux relative to a sharp tip, at the cost of more drag (Bertin; NASA educational TPS overviews). Sphere-cone and blunt-ogive study shapes exist to explore that trade — see `shell/blunt_cone_study.scad`.

ISM B1 uses that geometry only as a **heat-shield packaging sketch**, not as a weapons or strike airframe.

---

## 4. Flow regimes (names only)

| Regime | Plain words |
|--------|-------------|
| Continuum | Mean free path ≪ body size — Navier–Stokes / CFD textbooks |
| Transitional / rarefied | Mean free path comparable to body features |
| Free-molecular | Mean free path ≫ body size — orbital-entry teaching cases |

ISM study models stay in continuum classroom language unless a later note explicitly changes regime.

---

## 5. What B1 takes into the heat-shield note

- Peak heating is a **nose / leading-edge** problem first.
- TPS class (heat sink / ablative / reusable radiative) follows from heat load duration and peak \(q\), not from weapons roles.
- See `heat-shield-tps.md` for material **classes** only.
