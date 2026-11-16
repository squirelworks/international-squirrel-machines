# Hobby rocket design note — B4 (#41)

**Product:** ISM-RK-1 study (educational / hobby class)  
**Motors:** certified commercial hobby motors only.

## Out of scope (hard limits)

- Guidance, steering, thrust-vectoring, canards, or any **active** flight control
- Ballistic-missile or reentry-vehicle design
- Custom / uncertified propellant formulation
- Export-controlled (ITAR/EAR) data
- Weapons, warheads, fuzing, seekers

Avionics in this tree are **passive**: log altitude/acceleration and fire a recovery charge on a simple apogee/altitude rule — not a guidance loop.

---

## 1. Airframe (study)

| Feature | Baseline | Notes |
|---------|----------|-------|
| Body | Cardboard / fiberglass / 3D-print tube class | Study OD ~40 mm, L ~600–800 mm |
| Nose | Ogive / conical plastic | Mass for CG |
| Couplers / bulkheads | Recovery bay + avionics bay | Separate from motor |
| Motor mount | 24 mm / 29 mm class tubes | Matches common certified motor diameters |

Study OML: `../shell/airframe_study.scad`.

---

## 2. Fins and stability margin

Textbook hobby rule of thumb: keep **static margin** (CP aft of CG) on the order of **1–2 body calibers** for stable coast (public model-rocket teaching; not a certified flight analysis).

| Symbol | Meaning |
|--------|---------|
| CG | Center of gravity (weigh / balance) |
| CP | Center of pressure (Barrowman-class estimate later; B4 stores study stub) |
| Static margin | \((x_\mathrm{CP} - x_\mathrm{CG}) / D\) in calibers |

Teaching check: `python3 rocket/docs/stability_examples.py`.  
Machine-readable stubs: `../interfaces/airframe.yaml`.

Fins: 3- or 4-fin clipped delta / trapezoid — fixed; **no** actuated surfaces.

---

## 3. Recovery

| Mode | B4 baseline |
|------|-------------|
| Dual-event optional | Drogue at apogee + main at altitude (passive altimeter) |
| Single-event | Apogee chute only for small models |
| Deployment | Ejection charge via certified motor or separate charge well — mechanical packaging only |
| Not in B4 | Guided parafoil, active steering, or mid-course correction |

---

## 4. Passive avionics

| Function | Allowed | Forbidden |
|----------|---------|-----------|
| Barometric altimeter log | Yes | — |
| Accelerometer log | Yes | — |
| Apogee detect → pyro channel | Yes (recovery only) | Guidance or steering |
| Radio beacon / GPS log (optional later) | Recovery aid | Closed-loop flight control |
| Fin/TV C actuators | — | **No** |

ICD stub: `../interfaces/avionics-passive.yaml`. KiCad boards are the next roadmap step.

---

## 5. Motor mount (certified motors only)

| Item | Baseline |
|------|----------|
| Mount tubes | 18 / 24 / 29 mm class (public hobby sizes) |
| Retention | Engine hook or screw retention — mechanical |
| Allowed motors | NAR / TRA **certified** consumer and high-power catalog motors |
| Not allowed | Homemade motors, military surplus, uncertified propellant |

Thrust curves and impulse classes come from public certification documents / manufacturer data sheets — cited when numbers are used; B4 does not embed proprietary thrust tables.

---

## 6. Next steps
KiCad passive logger / recovery / power, structure, Gerbers/STLs, BOM, polish.
