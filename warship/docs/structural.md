# Warship — structural study (#43)

**Product:** ISM-WS-1  
**Slice:** educational primary-structure layout (keel, frames, decks, bulkheads).  
**Not** a certified naval architecture package or scantling study.

## Scope limits (hard)

- Weapons / combat sensors = **mass / footprint placeholders** only
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- **No** export-controlled (ITAR/EAR) data
- Public-domain hydrodynamics / arrangements language only

## Load path sketch (study)

| Member | Role | Study note |
|--------|------|------------|
| Keel / centerline girder | Axial / grounding stub | Along hull length |
| Transverse frames | Circumferential stations | Midbody spacing study |
| Deck beams | Weather-deck support stubs | Under deck box |
| Longitudinal bulkheads | Subdivision stubs | Port/stbd study |
| Transverse bulkheads | Compartment stubs | Clear of weapon placeholders |
| Superstructure foundations | Bridge house attach stubs | Mass only |
| Thruster / rudder foundations | Scale-model actuator mounts | KiCad control stubs |

Stations: `../interfaces/hydrostatics.yaml` + `../interfaces/structural.yaml`.  
Shell: `../shell/hull_study.scad` (ghost frames / keel / decks).  
Combat placeholders stay in `../interfaces/mass-placeholders.yaml` — **no solids**.

## Next (not this PR)

Gerbers / STLs, master BOM, polish / inquire-for-release.
