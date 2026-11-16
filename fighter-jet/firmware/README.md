# Bay I/O Firmware Bring-up — ISM-FJ-1 (#84 / A1 #119)

Host-buildable bring-up for the **bay I/O concentrator** (`../kicad/`). Maps logical PWM J1–J4 and inceptor stubs for HIL / Flight Lab adapters. Not the quadruplex FCC laws binary.

## MCU (from schematic)
| Item | Value |
|------|-------|
| Part | **RP2040** (`ISM:MCU`) |
| Study package | ISM QFN-56-1EP (1.27 mm pitch — not production 0.4 mm) |
| Rails | 3V3, GND (5V on servo headers) |
| Debug | UART/stdio host profile; SWD/USB on article later |
| Datasheet | https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf |

## Toolchain
| Target | Toolchain |
|--------|-----------|
| **Host stub (default, CI)** | `gcc` C11, `-Wall -Wextra -Werror` — `make` / `make test` |
| Pico / RP2040 (optional later) | Pico SDK — same API in `include/ism_bay_fw.h` + `hal/` |

```bash
cd fighter-jet/firmware
make clean && make && make test   # 0 errors / 0 warnings
make run                          # interactive UART/stdio profile
./scripts/test_brownout.sh        # SS-BO-01
./scripts/test_uplink_loss.sh     # SS-UL-01
```

Builds **without** the board attached.

## Behaviour
- **BIT line** (stdio / `bay_io.bit`): board id, version, `fw_hash`, rails, IMU self-test, uptime, fault bits, actuator + inceptor vectors — see `../interfaces/bit-frame.yaml`.
- **Actuator path:** `act <ch> <cmd>` → J1–J4 normalized (−1…+1); rejected in safe-state.
- **Safe-state triggers:** brownout, watchdog, uplink loss, inceptor loss → neutral PWM + inactive discretes (`../interfaces/safe-state.yaml`).
- **HAL stubs:** `hal/ism_hal.h` (host no-ops in `ism_hal_host.c`).

## Partitioning (study)
| Loop | Rate (provisional) | Notes |
|------|--------------------|-------|
| Control proxy | 100 Hz | Not FCC laws — bay mapping only |
| Housekeeping / BIT | 10 Hz | `bay_io.bit` |
| Jitter budget | 500 µs provisional | Measure on analyzer before claiming |

## Steve / Soft hooks
| Artifact | Path |
|----------|------|
| BIT frame | `../interfaces/bit-frame.yaml` |
| Safe-state | `../interfaces/safe-state.yaml` |
| Bay I/O iface | `../interfaces/bay-io.ismfj-iface` |
| Params / cal | `../parameters/ism-fj-1.ismfj-params` |
| Bus topics | `../interfaces/avionics-bus.yaml` (`bay_io.*`, `mc.*`, `hud.*`, `analyzer.*`) |
| Bring-up checklist | `../avionics/bringup-log.md` |

## Reference patterns (not compliance)
- MIL-STD-1553B Notice 2 — scheduled BIT framing idea
- MIL-STD-704F — brownout / transient test category ideas
- NASA SP-2016-6105 Rev 2 — ICD / verification practice

## Out of scope
FCC production laws, Soft UI apps (#79–83 implementations), weapon release/arming/fuzing (inert placeholders only).
