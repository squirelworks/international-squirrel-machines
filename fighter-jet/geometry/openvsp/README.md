# OpenVSP / VSPAERO — ISM-FJ-1

Steve converts this parametric description (or builds `.vsp3` from it). Study millimetres match `shell/airframe.scad` / `interfaces/aircraft-geometry.yaml`. Full-scale = study × **36.9**.

## Parametric OML (`ism-fj1-parametric.yaml`)
Fuselage length, span, chords, sweep, empennage — enough to recreate a vortex-lattice / panel model without proprietary CAD.

## VSPAERO cases (`vspaero-cases.yaml`)
Alpha / Mach / altitude sweeps for CL/CD/Cm; expected band pointers into `viability-criteria.yaml`.
