# Manufacturing & Supply Chain Research — ISM-FJ-1

**Issue:** [#100](https://github.com/squirelworks/international-squirrel-machines/issues/100) · Related [#92](https://github.com/squirelworks/international-squirrel-machines/issues/92)  
**Machine-readable:** `../interfaces/manufacturing.yaml`  
**Zones:** `../interfaces/materials-zones.yaml` · Drawings: `ISM-FJ-DWG-010`…`070`

## Hard stop (this track)
**Research only** for processes/specs/supply. Assembly jig / layup / die **designs** live under `../tooling/` ([#106](https://github.com/squirelworks/international-squirrel-machines/issues/106)). Eric owns general shop machines (CNC mill, large-format printer, heat-treat oven); listed below only as **required equipment**, not designed in-repo.

## Process vocabulary
| Code | Meaning |
|------|---------|
| `forge_machine` | Closed-die forge + CNC machining |
| `hot_spf_db` | Hot forming / superplastic forming + diffusion bond (Ti structures) |
| `am_ded_pbf` | Metal additive (DED or powder-bed fusion) + finish machine |
| `sheet_rivet` | Sheet form + rivet/fasten |
| `composite_auto` | Composite layup + autoclave (or OoA equivalent later) |

## Zone manufacturing map

Keyed to `materials-zones.yaml`. Specs are **public AMS-class callouts** (examples for procurement research — not a claim of current certification).

| Zone | Primary process | Spec / alloy (public class) | Heat treat (typical) | NDT | Drawing cross-ref |
|------|-----------------|----------------------------|----------------------|-----|-------------------|
| radome | `composite_auto` | Quartz/epoxy RF class (ISM-RF-Q) | Cure per resin SDS | Visual + tap / UT bond | DWG-050 FS-0–5 |
| forward_fuselage_skins | `sheet_rivet` (+ CFRP panels) | AMS 4037 2024-T3 sheet class | As-received T3; no re-age unless forming | Visual, eddy current holes | DWG-010/050 |
| pressure_bulkheads | `forge_machine` or plate machine | AMS 4045 7075-T6/T651 class | T6 / T651 | UT plate; penetrant machined | FS-22/42 |
| avionics_bay_structure | `composite_auto` + Al frames | CFRP + 7075 tray frames | Cure + Al T6 | UT laminate; visual | DWG-020 FS-48 |
| wing_skins | `composite_auto` | ISM-CFRP-A epoxy | Autoclave cure | UT / thermography | DWG-060 |
| wing_spar_caps | `forge_machine` or extrusion+machine | 7075 / Al-Li class bar-plate | T6 / T7351 class | UT; penetrant | DWG-030/060 |
| wing_spar_webs_ribs | `composite_auto` | CFRP | Cure | UT | DWG-060 |
| carry_through_box | Al box `sheet_rivet`/`forge_machine`; fittings `forge_machine` | 7075 + **AMS 4928/4911 Ti-6Al-4V** fittings | Al T6; Ti annealed or STA | UT; MPI/LPI fittings | DWG-030 FS-62 |
| landing_gear | `forge_machine` (Ti) or steel alternate | AMS 4928 Ti bar/forging **or** AMS 6417 300M | Ti anneal/STA; 300M quench+temper | UT + MPI | FS-18/55 |
| arresting_hook_keel | `forge_machine` | Ti AMS 4928 **or** 300M AMS 6417 | As gear | UT + MPI | FS-88–94 / keel |
| empennage_skins | `composite_auto` | CFRP | Cure | UT | DWG-010 |
| actuator_fittings | `forge_machine` (± `am_ded_pbf` proto) | Ti AMS 4928 | Annealed / STA | LPI + UT | surface hinges |
| aft_hot_structure | Ti `forge_machine` / `hot_spf_db`; Ni panels | Ti-6Al-4V + Ni HT sheet class | Ti + Ni per alloy | UT; visual | FS-82–100 |
| fasteners_primary | Buy finished | Ti / CRES aerospace fasteners | — | Lot certs | airframe |

**Metal AM:** reserved for prototype fittings / low-rate brackets (`am_ded_pbf`); flight fittings still plan forge+machine unless qualification campaign (#78) says otherwise.

**SPF+DB:** optional for Ti hollow structures / ducts — research path only for Block 2.

## Titanium path (Kroll → mill → small builder)

```
Ore / TiCl4 → Kroll sponge → electrode → (EB/PAM optional first melt) → VAR (final) → billet
  → mill products: AMS 4911 sheet/plate · AMS 4928 bar/forging stock
  → distributor cut-to-size → ISM forge/machine house → finished fitting
```

| Stage | Notes for ISM |
|-------|----------------|
| Kroll sponge | Commodity upstream; ISM does **not** operate Kroll plants |
| VAR | Aerospace cleanliness; public AMS 4911/4928 require multiple melt with VAR final |
| Mill products | Sheet/plate/bar from mills or AS9100 distributors |
| Lead times | Public distributor stock: days–weeks for common gauges; mill orders: **months**; forging dies: tooling track |
| Risks | Sponge/VAR capacity cycles; DFARS/domestic melt if required later; hydrogen/alpha-case process control |
| Small-builder buy | Purchase **certified** AMS 4911/4928 from aerospace distributors (examples below) with MTRs; no minimums often advertised for stock; cut-to-size then send to job-shop forge/CNC |

### Public supplier examples (citations — not endorsements)
| Example | Offers | Cite |
|---------|--------|------|
| Dynamic Metals | Ti-6Al-4V bar AMS 4928, sheet/plate AMS 4911; notes VAR final melt | [dynamic-ti64] |
| Service Steel Aerospace | Ti-6Al-4V mill products AMS 4911/4928; 300M AMS 6417 datasheet | [ssa-ti64], [ssa-300m] |
| United Performance Metals | Ti-6Al-4V sheet/plate/bar AMS 4911/4928/6931 | [upm-ti64] |
| TW Metals | AMS catalog including AMS 4037 (2024), AMS 4045 (7075) | [tw-ams] |
| Flight Metals | 300M AMS 6417 bar/forgings | [flight-300m] |

## Aluminum & steel (high level)
- **2024-T3 sheet (AMS 4037 class):** fatigue skins; form + rivet; keep cold-work benefits.
- **7075-T6/T651 (AMS 4045 class):** bulkheads, spar caps; watch SCC — prefer T73xx where damage tolerance demands.
- **300M (AMS 6417 class):** gear/hook **cost alternate**; corrosion plan mandatory vs Ti primary (#92/#93).

## Composites
Prepreg layup + autoclave (Eric oven as required equipment). Lightning mesh on wing skins. Galvanic isolation at CFRP–Al joints (`metallurgy-composites.md`).

## Required equipment (Eric’s lane — do not design here)
CNC mill · large-format polymer printer (study models) · heat-treat / cure oven · rivet guns / drills · UT/LPI inspection kits.

## Acceptance (#100)
- [x] Issue filed
- [x] This markdown note
- [x] `manufacturing.yaml`
- [x] Zones covered
- [x] Ti Kroll→VAR→mill path
- [x] Public citations
- [x] No tooling designs in this PR
