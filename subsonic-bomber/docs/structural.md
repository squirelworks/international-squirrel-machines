# Subsonic bomber — structural study (#38)

**Product:** ISM-SB-1  
**Slice:** educational primary-structure layout (spars, ribs, frames, gear attach).  
**Not** a certified airframe or stress report.

## Weapons boundary (hard)

- Bay = **inert volume / mass keep-out** only
- **No** munition structure, ejectors, pylons for live stores, seekers, or warheads
- SAFE/INHIBIT remain integration discretes — see `../interfaces/bay-board.yaml`

## Load path sketch (study)

| Member | Role | Study note |
|--------|------|------------|
| Wing carry-through | Spar box across fuselage | Shares station with wing root |
| Wing spars (front/rear) | Bending / torsion stub | Sweep-aligned; packaging only |
| Wing ribs | Chordwise shape stubs | Count is study-class, not sizing |
| Fuselage frames | Bay / gear / empennage stations | Clear bay keep-out |
| Keel / longerons | Axial load stubs | Around bay cutout |
| MLG / NLG attach | Tricycle gear hardpoints | Runway ops only — no carrier claim |
| Empennage spars | Fin + stabilizer stubs | Conventional layout |

Stations and dimensions: `../interfaces/airframe.yaml` + `../interfaces/structural.yaml`.  
Shell visualization: `../shell/airframe_study.scad` (ghost spars/ribs/frames).

## Bay cutout

The main bay is a **volume keep-out**. Longerons and frames route around it; no weapons-bay mechanisms beyond the inert door actuator stub on the KiCad board.

## Next (not this PR)

Gerbers / STLs export, master BOM, polish / inquire-for-release.
