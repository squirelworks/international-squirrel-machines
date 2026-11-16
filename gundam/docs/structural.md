# Gundam — mechanical / structural study (#46)

**Product:** ISM-MS-1  
**Slice:** educational mecha primary structure (torso frame spars, limb spars, joint stubs, armor keep-outs, control-board tray).  
**Not** a flight/combat-qualified suit structure or fire-control ICD.

## Weapons boundary (hard)

- Stores / hardpoints = **mass, footprint, SAFE/INHIBIT integration stubs** only
- **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming codes
- **No** live launch / fire sequences or engagement doctrine
- **No** ITAR/EAR weapon or fire-control designs

## Load path sketch (study)

| Member | Role | Study note |
|--------|------|------------|
| Torso frame spars | Primary torso stiffening | Spine / rib stubs |
| Limb spars | Arm/leg tube stiffening | Packaging only |
| Joint stubs | Hip / shoulder / knee placeholders | Motion packaging |
| Armor keep-outs | Outer shell volume stubs | Not ballistic design |
| Control-board tray | KiCad board mount | SAFE/INHIBIT packaging |
| Stores hardpoint pads | Inert mass/footprint only | From stores-placeholders |

Stations: `../interfaces/suit.yaml` + `../interfaces/structural.yaml`.  
Shell: `../shell/frame_study.scad` (ghost spars / joints / tray / pads).

## Next (not this PR)

Gerbers / STLs, master BOM, polish / inquire-for-release.
