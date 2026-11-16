# Sensor Integration (Physical) — ISM-FJ-1 (#76 / A4 #122)

**YAML:** `../interfaces/sensors.yaml` (`apertures[]`) · **FOV sketch:** `sensor-fov-keepouts.svg`  
**Datums:** `ISM-FJ-DWG-050` (fuselage stations) · `ISM-FJ-DWG-010` (OML) · `ISM-FJ-DWG-080` (aperture keep-outs)

## Hard stop (out of scope)
**Physical integration only.** Sensor internals remain fictional black boxes. **No** RF/EO performance prediction, waveforms, frequencies, or tactics. **No** missile seekers, guidance, warheads, fuzing, or arming. RWR/ESM stays non-specific cueing (`ew.md`).

## Aperture table (study mm; nose origin; L=420)

| ID | Station / mount | FS% | BL mm | WL mm | Envelope (L×W×H mm) | Mass kg | Power W | Cooling | Data topic | FOR cone |
|----|-----------------|-----|-------|-------|---------------------|---------|---------|---------|------------|----------|
| ISM-R1 | Nose radome | 5 | 0 | 28 | Ø40 × 30 deep | 85 | 2500 | ECS/liquid 2–5 kW class | `mc.radar_tracks` / `mc.radar_bit` | Az ±60°, El ±30° |
| ISM-EO1 | Ventral chin | 8 | 0 | 8 | 28×28×35 | 18 | 200 | ECS air 150 W | `mc.eo_tracks` / `mc.eo_bit` | Az ±90°, El −20…+40° |
| ISM-ADC probes | Nose boom / side | 10–15 | ±22 | 30 | each Ø6 × 40 | 2.5 kit | 15 | passive | `air_data.state` | n/a (probe) |
| ISM-GNSS | Spine / fin | 70–85 | 0 | 58 | 40×40×15 | 0.8 | 8 | passive | `gnss.state` | upper hemisphere |
| ISM-IMU | Bay slot D | 48 | 0 | 48 | 80×60×40 | 4.5 | 25 | passive tray | `imu.state` | n/a |
| ISM-EW-RWR | Tip/fin + aft L/R | — | ±140 / ±20 | — | each 20×20×30 | 1.2 ea | 80 total | passive | `mc.rwr_emitters` | sphere stub |

Rows authoritative in `sensors.yaml` → `apertures[]`. Mounts cite `ISM-FJ-DWG-050` / study xyz.

## Field-of-regard keep-outs (geometry only)

| Sensor | Blocked by | Geometry note |
|--------|------------|---------------|
| ISM-R1 | Open NLG doors (lower hemi clutter); extreme pitch with tip stores | Lower FOR clipped when NLG deployed |
| ISM-EO1 | NLG door / leg when down; ground plane on taxi | Chin window must not slew into gear envelope |
| Air-data | Extreme sideslip / icing (validity, not FOR) | Disagree → degraded FCS (#74) |
| GNSS | Fuselage shadow below antenna plane | Upper-hemisphere install |
| RWR | Own pylons / stores occultation stubs | Non-specific; no tactics |

## Nose OML containment (volume check)
Study question: can the nose OML (`shell/airframe.scad`) contain the R1 aperture envelope?

- R1 envelope is a Ø40 × 30 mm cylinder at FS~5% / WL mid — forward of the NLG well (x≥55). Packaging OML is the radome capsule in `shell/lib/sensor_aperture_keepouts.scad` (`ISM-FJ-DWG-080`); `airframe.scad` uses a simplified hull tip.
- OpenSCAD: `shell/check_sensor_apertures.sh` asserts (1) aperture ∩ structural keep-outs (crew PV / gear wells) is empty, and (2) R1 outside the radome packaging OML is empty (contained).

## MC stub messages (#81 consumers)
Status / BIT / track-placeholder only — no performance content. See `flight_lab_stubs` in `sensors.yaml`:

| Topic | Fields (stub) |
|-------|---------------|
| `imu.state` | rates, accels, valid |
| `air_data.state` | keas, alt, mach, aoa/aos, valid |
| `gnss.state` | lat/lon/alt, sog, valid |
| `mc.radar_tracks` | track_id, az/el, range stub, quality |
| `mc.radar_bit` / `mc.eo_bit` | lru_ok, cooling/window_ok, power_ok |
| `mc.eo_tracks` | track_id, az/el, ir_or_tv, quality |
| `mc.rwr_emitters` | emitter_id, az, band_class, priority |

## Citations (open / public)
- Drawing datums: `ISM-FJ-DWG-050`, `ISM-FJ-DWG-010`
- Packaging method parallels A2 keep-out geometry (`shell/lib/`)
