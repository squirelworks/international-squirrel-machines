# Airframe Structure — ISM-FJ-1 (#72)

**Machine-readable:** `../interfaces/mechanical-airframe.yaml`  
**Datum / stations:** `../interfaces/aircraft-geometry.yaml` · `ISM-FJ-DWG-050/060`  
**Materials:** `../materials/` · allowables `#71`

## Configuration
- Twin-engine, single-fin, mid-mounted swept wing (~35° LE study).
- Semi-monocoque fuselage with discrete longerons and machined bulkheads at pressure and gear stations.
- Wing carry-through box through center fuselage (**FS-62**) — continuous bending path wing-to-wing.
- Baseline HT: **all-moving** with geared tab stub (product decision).

## Primary structure

| Element | Intent | Key stations |
|---------|--------|--------------|
| Forward fuselage | Pressure vessel + NLG well + sensor bay; splice | FS-18 NLG, FS-22/42 bulkheads, splice FS-42 |
| Center fuselage | Avionics bay, fuel, MLG wells, carry-through | FS-48 bay, FS-55 MLG, FS-62 box |
| Aft fuselage | Engine mounts, ducts, empennage, firewalls | FS-90 mounts, FS-92 HT hinge |
| Wing box | Front spar ~15% chord, rear ~65%; ribs at WS | WS-0…10; fold latch **WS-4** |
| Empennage | Fin torsion box; all-moving HT | FS-88…96 VT spars; FS-92 HT |

Assemblies A01–A08 map to `../diagrams/assembly-breakdown.md`.

## Load paths

1. **Wing bending:** skins → spars → root fittings → carry-through (FS-62) → opposite wing / fuselage frames.  
2. **Landing:** tire → leg → trunnion (FS-18 / FS-55) → keel / bulkheads → longerons — **never** through avionics trays alone.  
3. **Empennage:** hinge moments → fin/HT spars → aft bulkheads → engine-bay frames.  
4. **Stores:** pylon fittings → spar-reinforced hardpoints (WS-2/4/6) → wing box (`ISM-FJ-DWG-040`).  
5. **Arrestment:** hook → damper → keel fittings (`carrier-suitability.md` / `carrier-loads.yaml`).

## Hardpoint / pylon pads
Structural pads at WS-2, WS-4, WS-6 tied into front/rear spars; mass limits in `hardpoints.yaml`. Wing-fold latch loads at WS-4 enter the same spar path (`LC-FOLD-01`).

## Flutter / stiffness (design-level)
- Aileron actuator stiffness and free-play limits TBD with first modes (AVL / #103 plan).
- Fin rudder mass-balance concept; ISM badge mass included in FEM later.

## OpenSCAD study
`../shell/airframe.scad` — proportion study with spar/rib planes, gear wells, surface hinge grooves, and export modules aligned to FS/WS tables. Not FEA geometry.
