# Propulsion Integration — ISM-FJ-1 (A2 #120)

**Scope:** packaging / interfaces only. The engine is a **public-class black box** (envelope + offtakes). No turbomachinery, combustor, or FADEC laws. **No weapon/missile propulsion.**

**Contracts:** `../interfaces/propulsion.yaml` · bounds `../docs/research/engine-class-bounds.md` · twin/single `../docs/research/twin-vs-single.md`  
**Study keep-outs:** `../shell/propulsion_keepouts.scad` (mm, scale 36.9)

## Baseline
Twin low-bypass turbofan modules, side-by-side, **FS-82–95**. Twin chosen for asymmetric-thrust backup and multirole payload. **Single-engine alternate** remains an open product decision (see twin-vs-single trade).

## Envelope table (full-scale class)

| Item | Band / nominal | Notes |
|------|----------------|-------|
| Count | 2 (baseline) | single open |
| Dry thrust / eng | ~50–60 kN class; **60 kN** nom. | EJ200/M88/F414 bounds |
| Wet thrust / eng | ~75–98 kN class; **90 kN** nom. | twin total **180 kN** → G-TW-MTOW ≈ 0.99 @ 18500 kg |
| Length / eng | 3.5–4.2 m; **3.9 m** nom. | |
| Max diameter | 0.70–0.90 m; **0.80 m** nom. | |
| Dry mass / eng | 900–1200 kg; **1050 kg** nom. | |
| SFC cruise | ~0.85 /h class | provisional → G-BREGUET |

Sources: `ef-tecguide-2013`, encyclopedia class pages, Raymer/Mattingly/Seddon textbook methods (DOI only).

## Inlet / duct packaging
| Parameter | Value (provisional) | Method |
|-----------|---------------------|--------|
| Design Mach | 0–1.6 | conceptual |
| Capture area (total) | 0.72 m² | textbook capture sizing class |
| Duct length | ~2.4 m (FS-60→FS-82) | station table |
| Offset ratio | ~0.35 | mild S-duct |
| Diffuser AR | ~1.6 | Seddon/Mattingly class |

**Routing sketch:** side/under lip → outboard ducts along lower-mid longerons → engine face at FS-82. Ducts **clear** dorsal avionics bay (FS-48) and **clear** MLG wells (FS-55). Open risks: distortion / compatibility (need CFD/tunnel later).

## Mount layout (FS-90 frames)
| Mount | FS | Loads |
|-------|----|-------|
| Thrust links L/R | FS-90 | forward thrust, 1g + manoeuvre inertia, gyroscopic stub |
| Side links fwd | FS-85 | lateral / vertical |
| Side links aft | FS-94 | lateral / nozzle interface |

Feeds `mechanical-airframe.yaml` attach notes. Firewall / hot zone: `materials-zones.yaml` aft_hot_structure.

## Offtakes
| Offtake | Twin baseline |
|---------|---------------|
| Generators | **40 kVA**/eng → **80 kVA** total toward PDU 28 V / EHA converters |
| Bleed | customer bleed stub |
| Cross-tie | essential bus survives single gen loss (`avionics/buses-power.md`) |

## Nozzle / aft body
Variable-geometry **stub** only. IR plume textbook notes belong in **A3** — no sensor-specific suppression design here.

## Fire protection
Engine-bay fire zones FS-82–95 L/R; bottles + detection → caution suite. No fuel-system detail beyond firewall.

## Removal
Aft on rails FS-82–98 **without cockpit separation** (`maintainability.md`). Clearance checked conceptually against HT/fin roots (FS-88–96).

## Controls
Throttles → FCC / FADEC-class controllers (vendor ICD TBD). Differential thrust as FBW secondary assist. Bay PWM J4 is **study throttle channel only** — not article FADEC.

## Viability wiring
`propulsion.yaml` `viability_inputs` supply `thrust_sl_*` and cruise SFC so **G-TW-MTOW**, **G-FUEL-FRAC**, and **G-BREGUET** have no missing propulsion input.

## Hard limits
- No engine internals or performance decks beyond public class figures.
- No munition/missile propulsion.
- Public sources only (no ITAR/EAR tech data).
