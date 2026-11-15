# Actuation Architecture — ISM-FJ-1

## Baseline: distributed EHA
Each primary surface (aileron L/R, HT, rudder, flaperon L/R) has a local EHA pack:
- Electric motor + pump + compact reservoir + actuator ram
- Commanded by FCC lanes over digital + analog backup PWM (bay PCB headers J1–J4 are the study-scale stand-in)

```
[Generators] --P--> [PDU] --power--> [EHA packs]
[FCC lanes]  --cmd--> [EHA controllers]
[Bay PCB]    --PWM/debug study path--> (maps to same logical channels)
```

### Why EHA for ISM
- Removes long pressurized tubing runs (leak/fire/maintenance).
- Fits “pure hardware” modular LRU story.
- Scales from study model servos → full EHA without changing FBW topology.

## Optional central hydraulic stub
If product decision retains central hydro (e.g., gun drive, special utilities):
- Engine-driven pumps (EDP) on each engine + electric backup pump.
- Dual independent circuits (System A / B) with isolated reservoirs.
- Accumulators for transient and emergency.
- Stainless / titanium lines in hot bay; flexible jumpers at splices FS-42 / FS-72.

| Element | Central-hydro stub role |
|---------|-------------------------|
| Reservoirs | A/B, boot-strap or pressurized |
| Pumps | EDP + EMDP |
| Filters / coolers | Per circuit |
| Priority valve | Flight controls > utilities |

## Interfaces to flight controls
- Position feedback LVDT/resolver per surface → FCC.
- Motor current / pressure monitors → health.
- Mode: normal / damped bypass / hardover protect (see failure-modes).

## Study-scale mapping
OpenSCAD shell and KiCad PWM channels represent the **same logical surfaces** as full EHA. Do not invent a second control topology for the model.
