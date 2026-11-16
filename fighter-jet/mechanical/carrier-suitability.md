# Carrier Suitability — ISM-FJ-1

**Issue:** [#93](https://github.com/squirelworks/international-squirrel-machines/issues/93)  
**Load cases (Steve / Flight Lab):** `../interfaces/carrier-loads.yaml`  
**Materials (hook/gear salt):** #92 / `materials/` (zone map lands with materials PR if not yet on main)

ISM fictional / public engineering only — not a copy of any navy’s classified recovery manuals or ship procedures. Contemporaries (public carrier fighters) are reference for *problem classes* only.

## 1. Arresting hook

| Item | Baseline |
|------|----------|
| Location | Aft keel, engage point ≈ FS-88–94 (under nozzles / ahead of tip) |
| Structure | Forged/machined hook shank + point; damper in series; attach to **keel beam** |
| Materials | ISM-Ti-6 primary; ISM-Steel-HS cost alternate (#92) |
| Retraction | Electric or EHA into fairing; stowed flush for land ops |
| Hold-down | Deck hold-back fitting stub at FS-55–62 keel (catapult tension path separate) |
| Damper | Hydraulic/oleo-style energy absorber; stroke & orifice schedule in YAML |

### Keel / fuselage load path (arrestment)
Hook point → damper → keel longeron/beam → FS-72 and FS-62 bulkheads → carry-through / MLG keel → distributed skin/longeron shear. **No** primary arrestment path through avionics trays or wing skins alone. Cite stations: `ISM-FJ-DWG-050`; carry-through: `ISM-FJ-DWG-030`.

## 2. Catapult / launch-bar (NLG)

| Item | Baseline |
|------|----------|
| Launch bar | Articulating bar on NLG; engages conceptual shuttle/tow (ISM carrier sibling TBD) |
| Hold-back | Keel or MLG-area tension link until launch release |
| NLG loads | Longitudinal tow + vertical/side from deck motion; sized with catapult cases in YAML |
| Steering | Disengaged or limited during launch tension |

## 3. Landing gear — sink rate

| Item | Baseline (provisional) |
|------|------------------------|
| Design sink rate | See `carrier-loads.yaml` (`sink_rate_design_m_s`) — higher than land-based |
| NLG | FS-18; shimmy damper; launch-bar attach |
| MLG | FS-55; trunnions into Ti fittings → keel |
| WOW | Dual discretes to FCC (ground laws / wing-fold inhibit) |

Detail kinematics remain in `landing-gear.md`; carrier deltas override sink-rate / launch-bar only.

## 4. Wing fold

| Item | Baseline |
|------|----------|
| Hinge line | ≈ WS-4 (50% semi-span) — outboard of heavy inboard pylon STA-7/8 |
| Motion | Up-and-in fold; hinges in wing box with latch pair |
| Latches | Dual independent locks; proximity + load sensors to MC/FCC |
| Inhibit | Fold inhibited unless WOW + park brake/chocks logic + engines per MC policy |
| Hardpoints | STA-1…4 outboard of fold may be empty or light only when folded (SMS flag) |

Geometry freeze will need a dedicated drawing ID (future DWG); until then cite `%WS` + `hardpoints.yaml`.

## 5. Corrosion protection (carrier / salt)

Aligned with materials track:

- Ti preferred for gear, hook, keel fittings.
- Al structure: sealed joints, drain paths at low FS/WS, chromate-free primer path.
- CFRP–Al isolation (glass ply / sealant).
- Steel alternate parts: mandatory corrosion maintenance interval (flag in YAML).
- Deck wash / rinse access without opening avionics bay.

## Acceptance (#93)
- [x] Design note: hook, gear, wing fold, corrosion
- [x] `interfaces/carrier-loads.yaml` with load cases & parameters
- [x] Drawing/station cross-refs (DWG-030/050; hardpoints)
- [x] No classified carrier procedure detail
