# Rocket — structural / mechanical study (#41)

**Product:** ISM-RK-1  
**Slice:** educational airframe structure (bulkheads, centering rings, motor mount, fin roots).  
**Not** a certified high-power build or TRA/NAR flight card.

## Scope limits (hard)

- **Certified commercial hobby motors only**
- **No** guidance, steering, or active flight control
- **No** ballistic-missile or reentry-vehicle content
- **No** ITAR/EAR data
- Avionics remain **passive** logger / recovery — see KiCad board

## Load path sketch (study)

| Member | Role | Study note |
|--------|------|------------|
| Nose bulkhead | Coupler / payload bay stub | Forward of body tube |
| Avionics bay bulkheads | Logger tray support | Passive logger board packaging |
| Centering rings | Motor-tube support | Mid / aft stations |
| Motor mount tube | Certified-motor keep-out | Packaging diameter only |
| Fin roots / spars | Fixed-fin attach stubs | No actuated surfaces |
| Recovery bulkhead | Shock-cord / chute attach | Passive of motor |

Stations: `../interfaces/airframe.yaml` + `../interfaces/structural.yaml`.  
Shell: `../shell/airframe_study.scad` (ghost rings / mount / fin roots).

## Next (not this PR)

Gerbers / STLs, master BOM, polish / inquire-for-release.
