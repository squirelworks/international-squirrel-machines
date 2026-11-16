# Hardpoint / Pylon ICD Geometry — ISM-FJ-1

**Drawing:** `ISM-FJ-DWG-040` Rev A · Sheet: `hardpoints-icd.svg`  
**Datum:** see `drawing-convention.md`  
**Machine-readable twin:** `../interfaces/hardpoints.yaml`

All positions are relative to aircraft datum (FS-0 nose tip, centerline BL-0, WL at fuselage mid-height). Study millimetres assume `fuselage_length = 420`, `wing_span = 280` (`shell/airframe.scad`).

## Station table (symmetric L/R unless noted)

| Sta | Side | FS % | FS study mm | WS % | BL study mm (semi-span 140) | WL study mm (rel. WL0) | Role | Max store mass class (stub) |
|-----|------|------|-------------|------|-----------------------------|------------------------|------|------------------------------|
| STA-1 | L tip | 58 | 244 | 100 | −140 | −6 | Wingtip rail | Light AAM |
| STA-2 | R tip | 58 | 244 | 100 | +140 | −6 | Wingtip rail | Light AAM |
| STA-3 | L | 60 | 252 | 75 | −105 | −8 | Outboard pylon | Light AAM / pod |
| STA-4 | R | 60 | 252 | 75 | +105 | −8 | Outboard pylon | Light AAM / pod |
| STA-5 | L | 61 | 256 | 50 | −70 | −10 | Mid pylon | Medium AAM / fuel |
| STA-6 | R | 61 | 256 | 50 | +70 | −10 | Mid pylon | Medium AAM / fuel |
| STA-7 | L | 62 | 260 | 25 | −35 | −12 | Inboard pylon | Heavy / fuel |
| STA-8 | R | 62 | 260 | 25 | +35 | −12 | Inboard pylon | Heavy / fuel |
| STA-9 | CL | 55 | 231 | 0 | 0 | −28 | Centerline | Fuel / EW / large |

Wing LE at root ≈ FS-48 (study mm 202); hardpoint FS values sit on the wing box carry-through band (FS-55–62). Exact lug bolt patterns freeze in Block 2 mechanical ICD; this sheet freezes **station locations**.

## Pylon interface (geometry envelope)
- Pylon attach face: parallel to local wing lower skin; lug pair spaced **80 mm** fore-aft (study) along local chord.
- Swing clearance cone: 15° outboard, 10° inboard (jettison / eject path stub).
- Wet hardpoints: product decision — baseline **dry** until fuel ICD lands.

## Citation
Mechanical (#72), stores (#77), and Flight Lab (#79) shall cite `ISM-FJ-DWG-040` + station IDs above — not free-text wing percentages alone.
