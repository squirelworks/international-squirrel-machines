# Viability Ladder — ISM-FJ-1

**Issue:** [#103](https://github.com/squirelworks/international-squirrel-machines/issues/103)  
**Criteria (Steve):** `../interfaces/viability-criteria.yaml`  
**Survey class context:** `research/comparative-fighter-survey.md` (#99)

## Pass / fail ladder

| Stage | Owner | In this PR? | Exit criterion |
|-------|-------|-------------|----------------|
| 1. Sanity gates | ISM | **Yes** | All gates in `viability-criteria.yaml` `pass` or documented `waiver` |
| 2. Independent analysis | ISM plan + Steve run | **Plan + geometry yes** | OpenVSP/VSPAERO + AVL + CalculiX bands met |
| 3. Scale model | Eric (data from ISM) | **Geometry/CG data yes** | Static + RC models match published targets |
| 4. Coupons | Validation (#78) | No | Allowables locked |
| 5. Full scale | Validation (#78) | No | Structural/flight campaign |

Repo scope for #103 = stages **1–2** fully specified; stage **3 data** published for Eric.

## Sanity (stage 1)
Compare provisional mass/geometry/propulsion assumptions against public fighter-class bands (Raymer / Roskam sizing heuristics + #99 programme class spread). Every rule cites a source in YAML.

## Independent analysis (stage 2)
| Tool | Artifact | Path |
|------|----------|------|
| OpenVSP / VSPAERO | Parametric OML + case defs | `../geometry/openvsp/` |
| AVL | Vortex-lattice deck | `../geometry/avl/` |
| CalculiX | Tailhook mount load cases + expected bands | `../geometry/calculix/tailhook-plan.yaml` |

Steve converts / runs; ISM owns expected-result bands and tolerances.

## Scale-model data for Eric (stage 3 input)
`../geometry/scale-model/targets.yaml` — OML source, scale factors, CG/inertia targets for static display and RC flight models. Eric builds models; ISM does not design his shop machines.

## Acceptance (#103)
- [x] Issue filed
- [x] `viability-criteria.yaml`
- [x] This ladder note
- [x] OpenVSP/AVL convertibles
- [x] CalculiX tailhook plan + bands
- [x] Eric scale-model targets
- [x] Citations on every sanity rule
