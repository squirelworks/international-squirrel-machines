# Airframe Structure — ISM-FJ-1

## Configuration
- Twin-engine, single-fin, mid-mounted swept wing (~35° leading-edge study).
- Semi-monocoque fuselage with discrete longerons and machined bulkheads at pressure and gear stations.
- Wing carry-through box through center fuselage (FS-62 region) — continuous bending path wing-to-wing.

## Primary structure
| Element | Intent |
|---------|--------|
| Forward fuselage | Pressure vessel (cockpit) + nose gear well + sensor bay; splice at FS-42 |
| Center fuselage | Avionics bay, fuel, MLG wells, carry-through |
| Aft fuselage | Engine mounts, inlet ducts, empennage attach, firewalls |
| Wing box | Front spar ~15% chord, rear spar ~65% chord; ribs at WS stations |
| Empennage | Fin torsion box; slab or conventional HT — **product decision: slab all-moving vs separate elevator** (baseline: all-moving HT with geared tab stub) |

## Load paths
1. **Wing bending:** skins → spars → root fittings → carry-through → opposite wing / fuselage frames.
2. **Landing:** gear → trunnion fittings → keel / bulkheads → longerons (never through avionics trays alone).
3. **Empennage:** hinge moments → fin/HT spars → aft bulkheads → engine-bay frames.
4. **Stores:** pylon fittings → spar-reinforced hardpoints (WS-2/4/6) → wing box.

## Flutter / stiffness (design-level)
- Aileron actuator stiffness and free-play limits TBD with first modes analysis.
- Fin with rudder mass-balance concept; ISM badge mass included in FEM later.

## OpenSCAD study
`shell/airframe.scad` is a **proportion study**, not FEA geometry. Next shell pass should expose spar/rib planes as separate modules matching WS/FS tables.
