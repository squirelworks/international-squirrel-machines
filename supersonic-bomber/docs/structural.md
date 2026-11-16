# Supersonic bomber — structural study (#39)

**Product:** ISM-XB-1  
**Slice:** educational primary-structure layout (spars, ribs, frames, gear attach) for slender supersonic cruise OML.  
**Not** a certified airframe or stress report.

## Weapons boundary (hard)

- Bay = **inert volume / mass keep-out** only
- **No** munition structure, ejectors, pylons for live stores, seekers, or warheads
- SAFE/INHIBIT remain integration discretes — see `../interfaces/bay-board.yaml`
- No hypersonic TPS structural recipes (those live under `hypersonic-bomber/`)

## Load path sketch (study)

| Member | Role | Study note |
|--------|------|------------|
| Wing carry-through | Spar box across fuselage | High-sweep root station |
| Wing spars (front/rear) | Bending / torsion stub | Sweep-aligned; packaging only |
| Wing ribs | Chordwise shape stubs | Study-class count |
| Fuselage frames | Bay / gear / empennage stations | Clear bay keep-out |
| Keel / longerons | Axial load stubs | Around bay cutout |
| MLG / NLG attach | Tricycle gear hardpoints | Runway ops — no carrier claim |
| Empennage spars | Fin + stabilizer stubs | Conventional / tall-fin study |

Stations: `../interfaces/airframe.yaml` + `../interfaces/structural.yaml`.  
Shell: `../shell/airframe_study.scad` (ghost spars/ribs/frames).

## Bay cutout

Main bay is an **inert volume keep-out**. Frames/longerons route around it; no live-store mechanisms beyond KiCad door/SAFE/INHIBIT stubs.

## Next (not this PR)

Gerbers / STLs, master BOM, polish / inquire-for-release.
