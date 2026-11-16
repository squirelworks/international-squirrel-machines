# Radar & EO Sensor Suite — ISM-FJ-1 (#76)

**YAML:** `../interfaces/sensors.yaml` · **FOV sketch:** `sensor-fov-keepouts.svg`  
**Bus:** Sensor fabric S1 + ISM-Bus-A (`avionics-bus.yaml`)  
**Soft processing apps:** Steve / SquirrelSoft — not this tree.

## Hard stop
No missile **seekers**, guidance, warheads, or fuzing. RWR/ESM is non-specific self-protect cueing only (`ew.md`).

## Aperture suite

| ID | Role | Mount (datum) | FOR (design) | Owner |
|----|------|---------------|--------------|-------|
| **ISM-R1** | Fictional AESA fire-control | Nose radome **FS ~5%** (`ISM-RF-Q`) | Az ±60°, El ±30° | MC |
| **ISM-EO1** | IRST / TV | Ventral chin **FS ~8%** | Az ±90°, El −20…+40° | MC |
| **ISM-IMU** | Rates / accels | Bay slot D **FS-48** | n/a | FCC+MC |
| **ISM-ADC** | Air data + AOA/AoS | Probes FS ~10–15% | n/a | FCC |
| **ISM-GNSS** | Multi-constellation | Spine/fin antenna FS ~70–85% | sky | MC (FCC soft) |
| **ISM-EW-RWR** | Emitter detect → LAD | Wingtip/fin + aft (L/R) | sphere stub | MC |

FCC may use radar/EO for **cueing only** — not flight-critical. Attitude/envelope: IMU + air data.

## Mounts vs blueprint datums
Study mm (nose origin, `fuselage_length=420`): R1 ≈ (21, 0, 28); EO1 ≈ (34, 0, 8). Full-scale ×36.9. Align to `ISM-FJ-DWG-050` / `aircraft-geometry.yaml`.

## Power + data ICD (summary)

| Node | Power | Data |
|------|-------|------|
| ISM-R1 | Primary 28 V · ~2.5 kW class · ECS/liquid cool | Cmd on Bus A; tracks on **S1** @ 20 Hz |
| ISM-EO1 | Primary 28 V · ~200 W · ECS air | Cmd Bus A; tracks/video S1 @ 30 Hz |
| IMU | Essential 28 V · ~25 W | `imu.state` @ 200 Hz Bus A |
| ADC | Essential 28 V · ~15 W | `air_data.state` @ 100 Hz |
| GNSS | Essential · ~8 W | `gnss.state` @ 10 Hz |
| RWR | Primary · ~80 W | `mc.rwr_emitters` @ 10 Hz |

Rows authoritative in `sensors.yaml`.

## Keep-outs / FOV
- **Radar:** keep liquid/waveguide off crew pressure vessel; lower-hemisphere clutter when gear doors open.
- **EO:** NLG door / leg when down; taxi debris; do not slew into gear envelope.
- **Air data:** icing / extreme sideslip disagree → degraded FCS mode (#74).

## Flight Lab stubs
Topics listed under `flight_lab_stubs` in YAML (tracks, BIT, IMU/air-data). No third-party sim as source of truth (#79 co-check).

## Still open
- Exact aperture diameter vs nose trade
- Cooling power refinement
- Antenna RF survey; LPI/ECCM claims stay non-specific
