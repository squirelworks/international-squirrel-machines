# Control Surfaces & Hinges — ISM-FJ-1 (#72)

**Hinge / actuator geometry:** `../interfaces/mechanical-airframe.yaml` → `control_surfaces_geometry`  
**Rates / laws / stops:** `../interfaces/flight-controls.yaml`  
**EHA channels:** `../interfaces/actuators.yaml`

## Surface schedule

| Surface | Span / station | Hinge | Actuator attach | Stops (design) |
|---------|----------------|-------|-----------------|----------------|
| Aileron L/R | WS 0.75–1.0 | ~75% chord @ WS-8 (0.92) | Rear-spar fitting @ WS ~0.88 | ±25° |
| Flaperon L/R | WS 0.15–0.70 | ~70% chord | Rear-spar @ WS ~0.40 | −15° / +35° |
| HT (all-moving) | FS-92 hinge | Pivot FS 0.92 | Aft bulkhead @ FS ~0.90 | −25° / +15° |
| Rudder | Fin TE | ~70% fin chord | Fin spar @ FS ~0.94, ~40% fin height | ±30° |
| LE device | Optional Block 2 | — | — | Deferred |

Deflection rates and FBW modes remain in `flight-controls.yaml` (authority of record for FCC).

## Hinges & bearings
- Self-aligning spherical bearings in **ISM-Ti-6** fittings for primary surfaces.
- Free-play budget allocated in FBW gain schedule (`flight-controls/`).
- Mass balance where flutter analysis demands; else actuator stiffness design.
- Shell: hinge-line grooves on wing TE / fin TE for study visualization.

## Load introduction
Actuator → spar/rib fitting → primary structure. **No** actuator load solely into thin skins.

## Maintainability
- Hinge pins via TE panels; actuator LRU without wing removal (connector + two structural bolts concept).
- See `maintainability.md`.
