# Aircraft carrier — structural study (#45)

**Product:** ISM-CV-1  
**Slice:** educational primary-structure layout (keel, frames, hangar decks, elevator trunks, island foundations).  
**Not** a certified naval architecture or flight-deck strength package.

## Scope limits (hard)

- Weapons / combat sensors / CIWS = **mass / footprint boxes** only
- Aviation ordnance = **inert mass boxes** only
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- Catapult / arresting = load/keep-out stubs only (no classified plant)
- **No** ITAR/EAR combat data

## Load path sketch (study)

| Member | Role | Study note |
|--------|------|------------|
| Keel / centerline girder | Axial stub | Along hull |
| Transverse frames | Hull stations | Midbody spacing study |
| Hangar deck | Intermediate deck stub | Below flight deck |
| Flight-deck beams | Weather-deck support | Under flight deck plate |
| Elevator trunks | Vertical well stubs | Align with openings |
| Island foundations | Superstructure attach | Starboard island |
| Catapult / wire keep-outs | Load path placeholders | No plant design |

Stations: `../interfaces/aviation.yaml` + `../interfaces/structural.yaml`.  
Shell: `../shell/deck_study.scad` (ghost structure under deck).  
Combat placeholders stay mass boxes — **no combat interfaces**.

## Next (not this PR)

Gerbers / STLs, master BOM, polish / inquire-for-release.
