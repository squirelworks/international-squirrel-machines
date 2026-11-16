# Sonar — mechanical enclosure / array mount (#40)

**Product:** ISM-SNR-1  
**Slice:** educational handheld / hull-mount enclosure structure (ribs, transducer face mount, board tray, display bezel).  
**Not** a flight/sea-qualified sonar housing or array ICD.

## Scope limits (hard) — same spirit as submarine B3

- Educational / public echo-sounder and fish-finder class only
- Transducers = **mass / footprint / frequency-class stubs**
- **No** quieting or acoustic signature design
- **No** classified beamforming, ASW tactics, or combat employment
- **No** weapons interfaces, fire control, seekers, guidance, warheads, or fuzing
- **No** ITAR/EAR sonar or acoustic-warfare content

## Load path sketch (study)

| Member | Role | Study note |
|--------|------|------------|
| Enclosure ribs | Handheld box stiffening | Primary shell |
| Transducer face mount | Circular face keep-out | Mass/footprint stub |
| Echo-board tray | KiCad board mount | AFE/DSP/power packaging |
| Display bezel | Window frame stub | UI packaging |
| Hull-mount pads | Optional mount feet | Hull packaging only |

Stations: `../interfaces/transducer-placeholders.yaml` + `../interfaces/structural.yaml`.  
Shell: `../shell/enclosure_study.scad` (ghost ribs / tray / bezel / pads).

## Next (not this PR)

Gerbers / STLs, master BOM, polish / inquire-for-release.
