# Avionics Architecture — ISM-FJ-1 (#75)

Beyond the bay PCB scaffold: aircraft-level nodes, buses, power, connectors, and packaging.  
**Contracts:** `../interfaces/avionics-architecture.yaml` · `../interfaces/avionics-bus.yaml`  
**Topology SVG:** `bus-topology.svg` · **Pinouts:** `connectors-pinouts.md` · **Placement:** `bay-pcb-placement.md`

## Multi-board / LRU split (justified)
| LRU | Bay slot | Why separate |
|-----|----------|--------------|
| **Bay I/O PCB** (`kicad/`) | F | Study/HIL concentrator: MCU, local IMU footprint, radio, PWM J1–J4, USB — **not** sole flight-critical path |
| **FCC ×4** | B | Flight-critical laws; physical separation from mission apps |
| **MC ×2** | A | Mission fusion / stores / display; may restart without losing control |
| **PDU** | C | 28 V cross-tie; keeps power faults off digital boards |
| **IMU tray** | D | Vibration isolation; short quiet harness to FCC/MC |
| **Radio / data-link** | E | RF / antenna feeds away from FCC |

Radar/EO boxes themselves are #76; Soft UI apps are Steve’s lane.

## Schematic coverage (bay I/O)
| Domain | Coverage | Notes |
|--------|----------|-------|
| IMU bus | I2C SDA/SCL + 3V3/GND | Local footprint; tray IMU via `J_SENS` |
| Radio | SPI MOSI/MISO/SCK + power | Module on bay PCB |
| Power tree | 28 V in → 5 V act / 3V3 logic | PDU upstream; LDO on board |
| Actuator drivers | J1–J4 PWM headers | Map to trunks A1–A4 / EHA cmd study path |
| USB debug | DP/DM | Development only (`ISM-Bay-Debug`) |

Orphan placeholders are not allowed without a note in `kicad/README.md` or this table.

## Bus topology (masters)
- **ISM-Bus A:** vehicle primary — FCC schedule owner (or TDMA peer); peers MC, bay I/O, radios, HUD symbol gen, PDU.
- **ISM-Bus B:** dissimilar physical route — FCC lane-2 side; isolation backup.
- **Sensor fabric S1:** radar/EO → MC (fiber stub preferred); **MC is master**.
- **FCC cross-channel:** deterministic short-period lane sync.
- **Maintenance USB:** WOW / maintenance-pin gated.

## BIT / health
`pdu.power_status`, `fcc.lane_health`, `mc.bit`, `bay_io.bit` @ ~10 Hz → HUD caution, Flight Lab, HIL. Enables #84 firmware bring-up from this baseline.
