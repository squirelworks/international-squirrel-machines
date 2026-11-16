# Space station — structural / mechanical study (#42)

**Product:** ISM-SSN-1  
**Slice:** educational habitat/node/lab primary structure (pressure shells, berthing rings, truss longerons, board tray).  
**Not** a flight-qualified station structure or berthing ICD.

## Weapons boundary (hard)

- Habitat / civil station only
- **No** weapons, seekers, guidance-to-target, warheads, fuzing, or combat employment
- Docked craft = mass/power/berthing stubs only
- **No** ITAR/EAR station or weapon designs

## Load path sketch (study)

| Member | Role | Study note |
|--------|------|------------|
| Habitat pressure shell | Cylindrical hab stub | Main volume |
| Node berthing rings | Common berthing stubs | Node sphere ports |
| Lab pressure shell | Cylinder stub | Aft of node |
| Truss longerons | External utility truss | Power / radiator packaging |
| Hab-board tray | KiCad board mount | EPS/ECLSS/CDH packaging |
| Docking keep-outs | Berthing volume stubs | From docking-placeholders |

Stations: `../interfaces/station.yaml` + `../interfaces/structural.yaml`.  
Shell: `../shell/module_study.scad` (ghost rings / longerons / tray).

## Next (not this PR)

Gerbers / STLs, master BOM, polish / inquire-for-release.
