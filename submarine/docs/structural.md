# Submarine — structural / pressure-hull study (#44)

**Product:** ISM-SS-1  
**Slice:** educational pressure-hull rings, casing, sail structure, and control-surface spars.  
**Not** a certified pressure vessel or collapse-pressure design.

## Out of scope (hard)

- Quieting / acoustic signature / sonar signal processing
- Life-support / atmosphere penetrations as a design product
- Weapons interfaces, fire control, seekers, guidance, warheads, fuzing
- Export-controlled (ITAR/EAR) data
- Sensors remain **mass / footprint placeholders** only

## Pressure-hull layout (study)

| Member | Role | Study note |
|--------|------|------------|
| Inner pressure hull | Watertight cylinder/teardrop stub | Scale-model wall; not sized for depth |
| Ring frames | Circumferential stiffeners | Even spacing along length |
| Outer casing | Free-flooding fairing stub | Textbook two-hull language |
| Sail structure | Fairwater mast trunk stub | Mass/KG only — no sensor arrays |
| Sternplane spars | Cruciform control stubs | Scale-model actuator attach |
| Machinery foundations | Aft shaft / ESC keep-out | Packaging only |
| Ballast tank bays | Fore/aft volume stubs | Trim demo — no plumbing design |

Stations / dimensions: `../interfaces/hydrostatics.yaml` + `../interfaces/structural.yaml`.  
Shell visualization: `../shell/hull_study.scad` (ghost rings / casing / sail frame).

## Depth / certification

This PR does **not** claim collapse pressure, fatigue life, or naval architecture approval. Ring spacing and wall thickness are **teaching placeholders**.

## Next (not this PR)

Gerbers / STLs export, master BOM, polish / inquire-for-release.
