# Landing Gear Concept — ISM-FJ-1 (#72)

**Envelopes & attach XYZ (study mm):** `../interfaces/mechanical-airframe.yaml` → `landing_gear`  
**Carrier deltas:** `carrier-suitability.md` + `../interfaces/carrier-loads.yaml` (#93)

## Arrangement
Tricycle. NLG forward retract; MLG retract inboard/aft into fuselage blend. Doors: CFRP sandwich, Ti hinges.

| Unit | Station | Design intent |
|------|---------|---------------|
| NLG | **FS-18** | Steering + shimmy damper; single wheel; **launch bar** for catapult |
| MLG L/R | **FS-55** | Levered / trailing-arm; brakes; single wheel baseline |

## Attach points (airframe)
| Unit | Structure | Study attach (mm, nose-origin) |
|------|-----------|--------------------------------|
| NLG | Keel + FS-18 bulkhead | ≈ (75.6, 0, 8) |
| MLG L | Keel + FS-55 trunnion + longerons | ≈ (231, −18, 10) |
| MLG R | Mirror | ≈ (231, +18, 10) |

Trunnions are **ISM-Ti-6** (steel HS alternate with heavy corrosion plan). Load path ends in keel/bulkheads — not wing skins alone.

## Stowed / deployed envelopes (study mm)

| Unit | Deployed wheel center | Stowed bay box (approx) |
|------|----------------------|-------------------------|
| NLG | (75.6, 0, −28), tire OD 18 | x 55–95, y ±12, z 5–30 |
| MLG L | (231, −42, −32), tire OD 28 | x 200–260, y −30…−5, z 5–35 |
| MLG R | (231, +42, −32), tire OD 28 | x 200–260, y +5…+30, z 5–35 |

Full-scale ≈ ×36.9. Shell cutouts in `../shell/airframe.scad` match these bays.

## Loads
- Spin-up / spring-back at design sink rate — carrier case **LC-LDG-01/02** (7.2 m/s class) in `carrier-loads.yaml`.
- Side loads into NLG (steering / crosswind).
- Catapult: launch-bar path **LC-CAT-01/02**.

## Systems interfaces
- Retract: electric or EHA — **product decision** (prefer electric to keep hydro localized).
- WOW discretes → FCC ground mode (`WOW_NLG`, `WOW_MLG_L/R`).
- NWS from FCC / rudder pedals on ground.
- Free-fall emergency extension (mechanical unlock + gravity/spring).

## Shell / STL
Module `landing_gear_deployed()` in `airframe.scad`; export target `gear.stl`.
