# Landing Gear Concept — ISM-FJ-1

## Arrangement
Tricycle gear. Nose gear (NLG) forward retract; main gear (MLG) retract inboard/aft into blend (exact door kinematics TBD).

| Unit | Station | Design intent |
|------|---------|---------------|
| NLG | FS-18 | Steering + shimmy damper; single wheel |
| MLG L/R | FS-55 | Trailing-arm or levered suspension; brakes; dual or single wheel (TBD) |

## Loads (qualitative)
- Spin-up / spring-back at touchdown sized for design sink rate (TBD with weight class).
- Side loads into NLG for steering and crosswind.
- MLG fittings into titanium/steel trunnions tied to keel beam — not to wing skins alone.

## Materials
- Legs / links: ISM-Ti-6 baseline (see `materials/`).
- Axles / pins: high-strength steel option if cost drives; corrosion plan required.
- Doors: CFRP sandwich with Ti hinges.

## Systems interfaces
- Retract: EHA or electric actuators (prefer electric for gear to keep hydro localized) — **product decision**.
- Weight-on-wheels (WOW) discretes to FCC for ground mode / envelope.
- Nose-wheel steering commanded from FCC/rudder pedals on ground.

## Failure / dispatch
- Free-fall emergency extension (mechanical unlock + gravity/spring assist).
- Door-open indications on HUD/LAD caution suite.
