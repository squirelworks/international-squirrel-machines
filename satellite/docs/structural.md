# Satellite — mechanical structure / panels (#31)

**Product:** ISM-SAT-1  
**Slice:** educational 3U-class primary structure (rails, panels, trays, solar-panel hinge stubs).  
**Not** a flight-qualified cubesat structure or launch-provider ICD.

## Scope / weapons boundary (hard)

- Civilian / educational **bus + payload** only
- Payload = **mass / power / data stubs** — no weapons, seekers, guidance-to-target, warheads, or fuzing
- **No** ITAR/EAR bus or payload designs

## Load path sketch (study)

| Member | Role | Study note |
|--------|------|------------|
| Corner rails | Primary longerons | 3U envelope |
| Side panels | Shear / closeout stubs | ±Y faces |
| Avionics trays | Board stack support | OBC/EPS/radio packaging |
| Payload deck | Mass/power attach stub | Non-weapon payload only |
| Solar-panel hinges | Deployable panel stubs | Packaging only |
| Antenna mounts | Comms attach stubs | Radio keep-out |

Stations: `../interfaces/bus.yaml` + `../interfaces/structural.yaml`.  
Shell: `../shell/bus_study.scad` (ghost trays / hinges under rails).

## Next (not this PR)

Gerbers / STLs, master BOM, polish / inquire-for-release.
