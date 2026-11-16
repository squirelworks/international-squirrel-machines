# Hypersonic bomber — structural / mechanical study (#37)

**Product:** ISM-HB-1  
**Slice:** educational primary-structure layout under the blunt-cone OML / TPS packaging shell.  
**Not** a certified airframe, collapse design, or TPS formulation.

## Out of scope (hard)

- Weapons, munitions, guidance, seekers, warheads, fuzing, or arming
- Scramjet / propulsion **design recipes**
- Export-controlled (ITAR/EAR) TPS formulations or classified materials data
- Stress / thermal-structural certification

## Load path sketch (study)

| Member | Role | Study note |
|--------|------|------------|
| Nose bulkhead | Sphere-cone junction stub | Under blunt nose |
| Ring frames | Circumferential stations | Along aft cone length |
| Longerons / stringers | Axial load stubs | Under TPS shell keep-out |
| TPS attach rails | Packaging attach stubs | Class placeholder — not a recipe |
| Aft bulkhead | Base / empennage attach stub | Study station only |
| Thermal-board tray | KiCad board mount stub | Sense board packaging |

Stations: `../interfaces/aerothermal.yaml` + `../interfaces/structural.yaml`.  
Shell: `../shell/blunt_cone_study.scad` (ghost frames / rails under TPS shell).

## TPS vs structure

Outer shell remains a **TPS packaging offset** (`tps-placeholders.yaml`). This PR does not add material recipes, ablation models, or classified stack-ups.

## Next (not this PR)

Gerbers / STLs, master BOM, polish / inquire-for-release.
