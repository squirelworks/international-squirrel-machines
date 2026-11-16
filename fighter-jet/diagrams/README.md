# Diagrams & Blueprints — Drawing Index

**Product:** ISM-FJ-1 “Nutcracker”  
**Convention:** `drawing-convention.md`  
**Issue:** [#70](https://github.com/squirelworks/international-squirrel-machines/issues/70)

Downstream mechanical / systems / Flight Lab work cites **drawing IDs** below (not free-text filenames alone).

## Drawing index

| Drawing ID | Rev | Sheet / artifact | Scale & units | Purpose |
|------------|-----|------------------|---------------|---------|
| ISM-FJ-DWG-010 | A | `orthographic.svg` | Study mm; 1 du = 1 mm; L=420 mm stated on sheet | Three-view orthographic (plan / side / front) |
| ISM-FJ-DWG-020 | A | `section-avionics-bay.svg` | Study mm; 1 du = 1 mm | Section cut through avionics bay at FS-48 |
| ISM-FJ-DWG-030 | A | `section-wing-root.svg` | Study mm; 1 du = 1 mm | Section cut wing root / main spar at FS-62 |
| ISM-FJ-DWG-040 | A | `hardpoints-icd.svg` + `hardpoints.md` | Study mm + % FS / % WS | Hardpoint / pylon locations vs aircraft datum |
| ISM-FJ-DWG-050 | A | `fuselage-stations.svg` + `stations.md` | % FS / study mm | Fuselage & wing station tables |
| ISM-FJ-DWG-060 | A | `wing-plan.svg` | Study proportions; spars % chord | Wing box spars / ribs |
| ISM-FJ-DWG-070 | A | `systems-overview.svg` | Schematic (N/A) | Sensors → MC/FCC → EHA overview |
| ISM-FJ-DWG-080 | A | `sensor-aperture-keepouts.md` | Study mm + % FS | Sensor aperture envelopes vs OML / gear keep-outs (A4 #122) |
| ISM-FJ-DWG-081 | A | `pylon-rail-icd.md` | Study mm + lug class | Pylon / rail interface ICD + clearance (A4 #122) |

## Supporting notes (not drawings)

| Artifact | File | Notes |
|----------|------|-------|
| Drawing convention / datum | `drawing-convention.md` | Axes, FS/WS/BL/WL, numbering |
| Assembly breakdown | `assembly-breakdown.md` | Major assemblies A01–A10 |
| Bay layouts | `bay-layouts.md` | Nose / cockpit / avionics / weapons / propulsion |
| Wiring / harness | `wiring-harness.md` | Trunks; pinouts TBD |

## Machine-readable twins
Geometry and hardpoints for Steve / Flight Lab: `../interfaces/` (`aircraft-geometry.yaml`, `hardpoints.yaml`, …).

## Acceptance (#70)
- [x] Three-view with scale and units stated (DWG-010)
- [x] Section through avionics bay (DWG-020) and main spar / wing root (DWG-030)
- [x] Hardpoints dimensioned vs defined datum (DWG-040)
- [x] Drawing index lists every sheet and revision (this README)
- [x] Downstream issues can cite drawing IDs unambiguously
