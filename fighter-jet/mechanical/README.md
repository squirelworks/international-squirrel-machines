# Mechanical Design — ISM-FJ-1

Airframe structure, landing gear, control surfaces, actuators/hinges, load paths, access panels, and maintainability.

| Doc | Focus |
|-----|-------|
| `airframe.md` | Primary structure, carry-through, load paths (#72) |
| `landing-gear.md` | NLG/MLG envelopes, attach XYZ, retract (#72) |
| `carrier-suitability.md` | Hook, catapult, sink-rate, wing fold, salt (#93) |
| `control-surfaces.md` | Hinge schedule, actuator attach (#72) |
| `maintainability.md` | Access panels, LRU paths, break points |
| `propulsion.md` | Twin turbofan packaging, inlet/mounts/offtakes (A2 #120) |

**Flight Lab contracts:** `../interfaces/mechanical-airframe.yaml` (#72), `carrier-loads.yaml`, `propulsion.yaml` (#120)  
Materials: `../materials/`. Stations: `../diagrams/stations.md`. Shell: `../shell/airframe.scad` + `shell/lib/propulsion_keepouts.scad`.
