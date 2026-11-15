# Control Surfaces & Hinges — ISM-FJ-1

## Surfaces

| Surface | Location | Actuation | Notes |
|---------|----------|-----------|-------|
| Aileron | Outboard trailing edge | EHA at WS-8 | Differential for roll; may blend with flaperon |
| Flaperon / flap | Inboard TE | EHA | Takeoff/landing; limited in-flight maneuvering use |
| Horizontal tail | FS-92 | EHA (pitch) | Baseline all-moving; see airframe decision |
| Rudder | Fin TE | EHA | Yaw; coordinate with differential thrust stub |
| Leading-edge device | Optional LE flap/slat | EHA or rotary | Envelope-dependent; may defer to Block 2 |

## Hinges & bearings
- Self-aligning spherical bearings in Ti fittings for primary surfaces.
- Free-play budget allocated in FBW gain schedule (see `flight-controls/`).
- Mass balance where flutter analysis demands; otherwise actuator stiffness design.

## Load introduction
Actuator attach → spar/rib fitting → primary structure. No actuator load solely into thin skins.

## Maintainability
- Hinge pins accessible via TE panels.
- Actuator LRU replaceable without wing removal (connector + two structural bolts concept).
