# Stores Integration (Inert) — ISM-FJ-1

**Issue:** [#94](https://github.com/squirelworks/international-squirrel-machines/issues/94) · Related [#77](https://github.com/squirelworks/international-squirrel-machines/issues/77)  
**Machine-readable:** `../interfaces/inert-stores.yaml`, `../interfaces/sms-interface.yaml`  
**Stations:** `../interfaces/hardpoints.yaml` · Drawing **ISM-FJ-DWG-040**

## Hard stop (out of scope)
**No** guidance laws, seeker design, rocket/motor propulsion, warheads, or fuzing. This track is **integration only**: attach geometry, inert mass/CG/drag for the flight model, separation envelopes, and SMS I/O for Steve / Flight Lab.

## Hardpoints, pylons, rails, ejector racks

| Hardware | Stations | Role |
|----------|----------|------|
| Wingtip rail | STA-1/2 | Rail launch; light AAM-class inert |
| Outboard pylon + rail/ejector | STA-3/4 | Light AAM / pod |
| Mid pylon + ejector rack | STA-5/6 | Medium AAM / fuel / strike-class inert |
| Inboard pylon + ejector rack | STA-7/8 | Heavy / fuel |
| Centerline pylon + ejector | STA-9 | Fuel / EW / large |

Pylon lug spacing study: 80 mm fore-aft (`hardpoints.yaml`). Ejector racks provide downward impulse at release; rails constrain pitch/yaw until clear. Loads stay in spar-reinforced hardpoints (DWG-030/040).

## Inert store class models (public figures)

ISM invents **inert** product IDs. Dimensions/mass below are **class-typical public figures** used only to seed Flight Lab mass/drag — not copies of any national weapon design.

### ISM-INERT-AAM-S (AIM-9 *class*)

| Property | Value | Public class reference |
|----------|-------|------------------------|
| Length | ≈ 2.9 m | AIM-9 family length ~2.85–3.0 m (public encyclopedic / fact-sheet range) |
| Diameter | ≈ 127 mm (5 in) | Widely published AIM-9 body diameter |
| Mass (inert training-class) | ≈ 85–91 kg | Public AIM-9 mass ~85–91 kg |
| CG (inert model) | 45% length from nose | ISM modeling assumption for integration |

Citations (open/public):
- Wikipedia, “AIM-9 Sidewinder” — length, diameter, weight summary (accessed as public reference; not SoT for ISM design).
- U.S. Navy / manufacturer public fact sheets historically list ~5 in diameter and ~190 lb class weight (same order of magnitude).

### ISM-INERT-AGM-M (AGM-114 *class*)

| Property | Value | Public class reference |
|----------|-------|------------------------|
| Length | ≈ 1.63 m | AGM-114 family length ~1.6 m (public) |
| Diameter | ≈ 178 mm (7 in) | Published Hellfire-class diameter |
| Mass (inert class) | ≈ 45–49 kg | Public AGM-114 mass ~45–50 kg |
| CG (inert model) | 48% length from nose | ISM modeling assumption |

Citations (open/public):
- Wikipedia, “AGM-114 Hellfire” — length, diameter, weight summary (public reference only).
- Public defense fact sheets / FAS-style open summaries for Hellfire-class dimensions (order-of-magnitude).

Exact part numbers and live munition internals are **not** used.

## Flight-model effects
For each loaded station, Flight Lab shall apply from YAML:
- added mass at station BL/FS/WL
- CG shift via `mass-properties.yaml` rules
- parasite drag increment (`cd_increment` / reference area)
- roll-inertia contribution stub (optional)

## Separation envelopes (engineering placeholders)
Provisional KEAS / AOA / Nz / sideslip gates in `sms-interface.yaml`. Marked `provisional: true` until Flight Lab co-check (#79) and validation (#78).

## SMS interface
MC owns inventory & consent; FCC vetoes on envelope/WOW; release/jettison commands are **discrete + serial topics** only — no fuze programming fields in-repo.

## Acceptance (#94)
- [x] Inert store YAML models
- [x] SMS interface machine-readable stub
- [x] Separation envelope placeholders with provisional flags
- [x] README / this note state no seeker/warhead/fuze/propulsion detail
