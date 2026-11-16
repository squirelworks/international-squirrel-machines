# OpenVSP / VSPAERO — ISM-FJ-1

Steve converts this parametric description (or builds `.vsp3` from it). Study millimetres match `shell/airframe.scad` / `interfaces/aircraft-geometry.yaml`. Full-scale = study × **36.9**.

## Parametric OML (`ism-fj1-parametric.yaml`)
Fuselage length, span, chords, sweep, empennage — enough to recreate a vortex-lattice / panel model without proprietary CAD.

Comments mark **signature-relevant** packaging parameters (edge sweep, inlet/nozzle stations) for A3 #121 — qualitative only; no predicted signature.

## VSPAERO cases (`vspaero-cases.yaml`)
Alpha / Mach / altitude sweeps for CL/CD/Cm; expected band pointers into `viability-criteria.yaml`.
