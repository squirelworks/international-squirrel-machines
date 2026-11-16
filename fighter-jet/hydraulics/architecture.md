# Actuation Architecture — ISM-FJ-1 (#73)

**Decision (recorded):** **Distributed electro-hydrostatic actuators (EHA)** for primary flight controls; **electric linear** preferred for landing gear / NWS / wing-fold. Central hydraulics = **optional stub only** (not baseline).

**Contracts:** `../interfaces/actuators.yaml` · `../interfaces/hydraulics.yaml`

## Architecture decision & rationale

| Option | Verdict | Why |
|--------|---------|-----|
| Distributed EHA | **Baseline** | No long pressurized runs; modular LRU; same FBW topology from bay-PCB PWM → full EHA |
| All-central hydro | Rejected | Leak/fire/mass; routing fights avionics bay (FS-48) |
| All-EMA (no local hydro) | Deferred Block 2 | HT/rudder hinge-moment margin TBD; revisit after #74/#78 |

```
[Generators] --P--> [PDU] --28V--> [EHA packs / gear motors]
[FCC lanes ×4] --voted cmd--> [EHA controllers]
[Bay PCB] --PWM/debug study--> same logical channels (J1–J4, HT, RUD)
```

Each primary-surface EHA pack: electric motor + pump + compact reservoir + ram. Position feedback (LVDT/resolver) + current/pressure health → FCC.

## Channel map

| Channel | Surface / utility | Category | Safe failure |
|---------|-------------------|----------|--------------|
| `eha_aileron_L/R` | Ailerons | Flight | Damp / bypass → trail |
| `eha_flaperon_L/R` | Flaperons | Flight | Damp hold or trail |
| `eha_ht` | All-moving HT | Flight | **Damp hold** (pitch-critical) |
| `eha_rudder` | Rudder | Flight | Damp / bypass → trail |
| `act_nlg_retract` | NLG | Gear | Free-fall unlock |
| `act_mlg_L/R_retract` | MLG | Gear | Free-fall unlock |
| `act_nws` | Nose-wheel steer | Utility | Damp center / caster (WOW-gated) |
| `act_wing_fold_L/R` | Fold @ WS-4 | Carrier util | Hold locks engaged |

Interface table (command / feedback / power / mechanical attach): **`actuators.yaml`**.

## Sizing assumptions (provisional)
Study-scale strokes ~25–40 mm surfaces, ~50–60 mm gear; rates align to `flight-controls.yaml`. Full-scale hinge moments TBD (#78); do not freeze vendor P/Ns now.

## Optional central-hydraulic stub
If later required (e.g. gun drive): dual circuits A/B, EDP per engine + EMDP, accumulators, priority valve (flight controls > utilities). Stainless/Ti lines in hot bay; flexible jumpers at FS-42 / FS-72 splices. **Not installed in baseline.**

## Study-scale mapping
OpenSCAD shell and KiCad PWM channels = same logical surfaces as full EHA. Do not invent a second control topology for the model.
