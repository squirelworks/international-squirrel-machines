# Metallurgy & Composites — ISM-FJ-1 (#71)

**Trade baseline:** `trade-study.md` / `candidates.yaml` / `../interfaces/materials-zones.yaml` (#92)  
**Allowables (machine-readable):** `../interfaces/materials-allowables.yaml`  
**Process / AMS sourcing:** `manufacturing-sourcing.md` / `../interfaces/manufacturing.yaml` (#100)

Public alloy *families* are reference only. ISM designations (`ISM-Ti-6`, `ISM-Al-7xxx`, …) are internal product choices — not claimed OEM equivalents. Allowables below are **placeholder-class** design values for Flight Lab / sizing; coupon qualification is #78.

## Spec-style material callouts (BOM-ready)

| ISM ID | Public class (ref) | Product form / AMS class | Primary use |
|--------|-------------------|--------------------------|-------------|
| `ISM-Ti-6` | Ti-6Al-4V | Plate AMS 4911, bar AMS 4928, forging | Gear, fittings, hook/keel, hot-adjacent |
| `ISM-Al-7xxx` | 7075-T6 | Sheet/plate AMS 4045 | Bulkheads, spar caps (hybrid baseline) |
| `ISM-Al-2xxx` | 2024-T3 | Sheet AMS 4037 | Fatigue-critical fwd skins / panels |
| `ISM-Al-Li` | Al-Li class | Plate/sheet | Production weight option (spar caps / fuse) |
| `ISM-Steel-HS` | 300M AMS 6417 | Bar/forging | Cost alternate gear / hook |
| `ISM-CFRP-A` | Carbon/epoxy prepreg | Tape / fabric | Skins, ribs, surfaces, fin |
| `ISM-RF-Q` | Quartz/epoxy | Radome shell | RF-transparent nose |
| `ISM-Ni-HT` | Ni / high-temp stub | Sheet panel | Firewall / nozzle-adjacent |

Numeric Ftu/Fty/E and densities: `materials-allowables.yaml`.

## Composite stack-ups (study)

| Stack ID | Layup intent | Thickness (study mm) | Zones |
|----------|--------------|----------------------|-------|
| `wing_skin_qi` | `[0/45/90/-45]s` quasi-iso | ~2.0 | Wing skins |
| `spar_web_shear` | `[45/-45]ns` | ~3.0 | Spar webs / ribs |
| `surface_sandwich` | QI facesheets + core TBD | facesheet ~1.0 each | Empennage / control surfaces |

Fiber areal weight and resin system class TBD before first autoclave lot; cure on Eric’s oven (equipment reference only).

## Allowed joints matrix

| Join | Allowed | Forbidden / avoid | Rationale |
|------|---------|-------------------|-----------|
| Bonded | CFRP skins↔cores, fairings, radome ring | Primary gear fittings, arresting hook | Continuous load / seal |
| Bolted | Fittings, gear, hook, access panels, spar root, carry-through | — | Replaceable LRUs; peak loads |
| Riveted | Al skins↔longerons, secondary structure | Primary CFRP spar roots | Established Al practice |
| Hybrid bond+bolt | CFRP↔Al splices | — | Load share + fail-safe |

**Fasteners:** Ti or CRES primary; large-footprint washers / inserts in CFRP; captive fasteners on access panels.

## Galvanic / corrosion

| Pair | Required controls |
|------|-------------------|
| CFRP–Al | Glass isolation ply or primer + sealant; **no** bare Al washer on carbon; Ti/CRES fasteners |
| CFRP–Ti | Preferred dissimilar pair; sealant optional |
| Al–Steel | Primer + sealant + drain paths |
| Ti–Steel | Sealant at faying surfaces |

Carrier/salt: Ti baseline for gear/hook; Al needs primer/sealant/filiform mitigation; steel alternate requires heavy protection plan (`materials-zones.yaml` `carrier_salt`). Drain paths at WS/FS low points.

## Environment

| Region | Envelope (design intent) |
|--------|--------------------------|
| Avionics bay | −40 °C … +70 °C; ECS / cold-plate path |
| Aft hot / firewall | Continuous soak up to ~300 °C Ti; Ni stub near nozzle |
| Marine / carrier | Deck salt, wet bilge, arrestment spray — coatings per zone |

Moisture knockdown on CFRP: provisional **0.85** (hot/wet) in allowables YAML.

## Prototype vs production substitutions

| Zone | Prototype | Production option | Why |
|------|-----------|-------------------|-----|
| Wing spar caps | `ISM-Al-7xxx` | `ISM-Al-Li` | Cost first, then mass |
| Landing gear | `ISM-Ti-6` | `ISM-Steel-HS` (coated) | Ti preferred naval; steel cost lever |
| Fwd fuselage skins | `ISM-Al-2xxx` sheet | `ISM-CFRP-A` panels | Repairability vs mass |
| Study shell | Soft tooling / print / machine | Certified mill product per #100 | OpenSCAD ×36.9 → full scale |

## Still open (validation #78)
- Exact temper lots / fiber areal weight / resin Tg margin
- Lightning zoning drawing
- Fuel-tank sealant system selection
- Coupon allowables replacing placeholder Ftu/Fty
