# Sensor Aperture Keep-outs — ISM-FJ-1

**Drawing:** `ISM-FJ-DWG-080` Rev A  
**Issue:** A4 #122 / #76  
**Machine-readable:** `../interfaces/sensors.yaml` (`apertures[]`)  
**Geometry check:** `../shell/check_sensor_apertures.sh`

## Purpose
Freeze aperture envelope stations (FS/BL/WL study) and structural keep-outs for packaging. No RF/EO performance content.

## Sheets
| Item | Ref |
|------|-----|
| R1 nose aperture | `sensors.yaml` ISM-R1 · study xyz (21, 0, 28) |
| EO1 chin aperture | ISM-EO1 · (34, 0, 8) |
| Keep-outs | Crew pressure vessel FS~20–40%; NLG/MLG wells |
| OpenSCAD | `shell/lib/sensor_aperture_keepouts.scad` |

## Citation
Downstream sensors / Flight Lab cite **ISM-FJ-DWG-080** + aperture IDs.
