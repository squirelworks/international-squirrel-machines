# Avionics Program — ISM-FJ-1

Beyond the bay controller PCB (#75): architecture, buses, power, connectors, MC/FCC roles, HUD/HMI, partitioning. KiCad under `../kicad/` is the **bay I/O concentrator** slice.

| Doc | Content |
|-----|---------|
| `architecture.md` | Aircraft-level architecture + schematic coverage |
| `bus-topology.svg` | Masters / peers diagram |
| `connectors-pinouts.md` | HOTAS / actuation / sense / power drafts |
| `bay-pcb-placement.md` | Placement zones + multi-board split |
| `mission-computer.md` | MC roles, lanes |
| `buses-power.md` | ISM-Bus, power architecture |
| `sensors-nav.md` | IMU, GNSS, air-data |
| `hmi-hud.md` | HUD, LAD, HOTAS |
| `software-partitioning.md` | Safety partitions |
| `computing-platform.md` | Flight-critical RTOS vs OS/2 ground/lab; SquirrelBIOS trial |

**Steve / Flight Lab:** `../interfaces/avionics-architecture.yaml` · `../interfaces/avionics-bus.yaml` · `../interfaces/bit-frame.yaml` · `../interfaces/bay-io.ismfj-iface`  
**Bring-up checklist (A1):** `bringup-log.md` · firmware `../firmware/`  
**Ground/lab OS:** [squirrel-os2#225](https://github.com/squirelworks/squirrel-os2/issues/225) — see `computing-platform.md`.
