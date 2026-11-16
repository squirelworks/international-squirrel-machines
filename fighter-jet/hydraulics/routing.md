# Actuation Routing & Keep-outs — ISM-FJ-1 (#73)

**Machine-readable corridors:** `../interfaces/hydraulics.yaml`  
**Systems overview drawing:** `ISM-FJ-DWG-070`

Baseline has **no** aircraft-length pressurized tubes — only local EHA packs plus **28 V / cmd / feedback** harnesses.

## Keep-out rules
1. **Avionics bay FS-48:** signal/power feedthroughs only — no EHA fluid reservoirs inside the bay.
2. **Engine bay FS-82+:** aft HT/rudder harness heat-shielded; avoid nozzle plume.
3. **Gear bays:** harness along keel; do not occupy NLG/MLG stow volumes (`mechanical-airframe.yaml`).
4. **Fuel cells / wing box cores:** harness in leading/trailing edge or spar raceways, not through wet bays without sealed conduits.

## Corridor sketch (study mm, top view)

```
FS-0 nose ---- FS-48 bay ---- FS-62 box ---- FS-92 HT ---- FS-100
         |              |              |             |
      gear harness   wing L/R EHA   spar raceways   empennage EHA
      along keel     y± corridors   (ail/flap)      (HT + rudder)
```

| Corridor | Approx box (study mm) | Serves |
|----------|----------------------|--------|
| Left wing | x 160–280, y −140…−20, z 15–45 | Aileron/flaperon L |
| Right wing | mirror | Aileron/flaperon R |
| Aft empennage | x 340–410, y ±20, z 25–70 | HT, rudder |
| Gear | x 55–260, y ±35, z 0–40 | NLG/MLG/NWS |

EHA pack bounding boxes: see `hydraulics.yaml` `eha_pack_envelopes_study_mm`.

## SVG
Optional visual: `routing-keepout.svg` (schematic, not lofted OML).
