# Station Diagram — ISM-FJ-1

Stations are expressed as **% of fuselage length (FS)** from nose tip aft, and **% semi-span (WS)** from centerline outboard. Absolute millimeters apply to the OpenSCAD study model (`shell/airframe.scad` defaults); full-scale lengths are TBD pending product weight class.

## Fuselage stations (FS)

| Station | % FS | Study mm (L=420) | Contents |
|---------|------|------------------|----------|
| FS-0 | 0% | 0 | Nose tip / pitot |
| FS-5 | 5% | 21 | Radome hinge / EO window fairing |
| FS-12 | 12% | 50 | Radar / EO bay aft bulkhead |
| FS-18 | 18% | 76 | Nose landing gear pivot |
| FS-22 | 22% | 92 | Forward pressure bulkhead |
| FS-28 | 28% | 118 | Instrument panel / HUD combiner plane |
| FS-35 | 35% | 147 | Stick / ejection seat rails (concept) |
| FS-42 | 42% | 176 | Aft cockpit bulkhead / ECS |
| FS-48 | 48% | 202 | **Avionics bay** (dorsal hatch) — KiCad board mounts here |
| FS-55 | 55% | 231 | Main landing gear trunnion |
| FS-62 | 62% | 260 | Wing carry-through / center box |
| FS-72 | 72% | 302 | Internal gun / ammo (optional) / fuel cell |
| FS-82 | 82% | 344 | Engine inlet ducts / accessory gearbox |
| FS-90 | 90% | 378 | Engine mounts / nozzle interface |
| FS-100 | 100% | 420 | Nozzle exit / drag chute (optional stub) |

## Wing stations (WS)

| Station | % semi-span | Role |
|---------|-------------|------|
| WS-0 | 0% | Root rib / side-of-body fitting |
| WS-2 | 25% | Inboard stores pylon hardpoint |
| WS-4 | 50% | Mid-span pylon / fuel |
| WS-6 | 75% | Outboard pylon (light stores / rail) |
| WS-8 | 92% | Aileron actuator bay |
| WS-10 | 100% | Tip / missile rail optional |

## Empennage
- Horizontal stabilizer hinge line ≈ FS-92, incidence trimmed by EHA.
- Vertical stabilizer spar roots ≈ FS-88–96; ISM badge boss on fin (~60% fin height).

## Drawing cross-ref
- Plan/side/front: `orthographic.svg`
- Wing box: `wing-plan.svg`
- Bay contents: `bay-layouts.md`
