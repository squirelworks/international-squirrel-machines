# Tooling — educational BOM (ISM-FJ-1 / #106 / 4b)

**Product:** ISM-FJ-1 study tooling  
**Slice:** fab-ready study package — STL + STEP markers for every OpenSCAD tool.

## Scope / weapons boundary (hard)

- Assembly / layup / forming **study tools** only (reduced-scale mm)
- Eric shop machines = **required equipment reference only** (not designed here)
- Soft #79/#80 remain **Steve’s lane**
- Product decisions are **FROZEN 2026-11-17** (`../docs/decisions.md`)
- Stores / weapons tooling out of scope beyond inert-structure fixtures
- **Not** a procurement order

## Printed / machined study articles

| Tool ID | Qty | Article | STL | STEP |
|---------|-----|---------|-----|------|
| ISM-FJ-TOOL-010 | 1 | Fuselage splice jig | `jigs/fuselage_splice_jig.stl` | `.step` |
| ISM-FJ-TOOL-020 | 1 | Wing box jig (RH study) | `jigs/wing_box_jig.stl` | `.step` |
| ISM-FJ-TOOL-030 | 1 | Empennage jig | `jigs/empennage_jig.stl` | `.step` |
| ISM-FJ-TOOL-040 | 1 | Drill/rivet edge fixture | `fixtures/drill_rivet_fixture.stl` | `.step` |
| ISM-FJ-TOOL-050 | 1 | Wing lower-skin layup tool | `layup/wing_skin_layup_tool.stl` | `.step` |
| ISM-FJ-TOOL-060 | 1 | Forward skin form die pair | `dies/skin_form_die.stl` | `.step` |
| ISM-FJ-TOOL-070 | 1 | Canopy layup mandrel | `layup/canopy_layup_mandrel.stl` | `.step` |
| ISM-FJ-TOOL-080 | 1 | Intake layup mandrel | `layup/intake_layup_mandrel.stl` | `.step` |

## Consumables / hardware (study)

| ID | Qty | Item | Notes |
|----|-----|------|-------|
| HW-PIN-6 | lot | ⌀6 mm alignment pins | TOOL-010 base |
| HW-BUSH-3.2 | 8 | Drill bushings ID 3.2 | TOOL-040 |
| HW-CLAMP | lot | Hand clamps | lab |
| VAC-BAG | lot | Vacuum bag film | layup tools — Eric oven for cure |
| REL-FILM | lot | Release film / tape | layup / dies |

## Out of BOM (explicit)

CNC mill / printer / oven designs (Eric lane); seekers, guidance, munition tooling; Soft apps (#79/#80).

## Machine-readable index

See `tooling.yaml` and CSV stub `BOM.csv`.
