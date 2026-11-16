# Bay I/O Firmware Bring-up — ISM-FJ-1 (#84)

Host-buildable bring-up for the **bay I/O concentrator** (`../kicad/`). Maps logical PWM J1–J4 and inceptor stubs for HIL / Flight Lab adapters. Not the quadruplex FCC laws binary.

## Toolchain
| Target | Toolchain |
|--------|-----------|
| **Host stub (default)** | `gcc` C11 — `make` / `make test` |
| Pico / RP2040 (optional later) | Pico SDK — same API in `include/ism_bay_fw.h` |

```bash
cd fighter-jet/firmware
make test          # safe-state + BIT unit test
make && make run   # interactive UART/stdio profile
```

## Behaviour
- **BIT line** (stdio): board id, version, rail/IMU/radio/uplink/brownout/safe, actuator + inceptor vectors.
- **Actuator path:** `act <ch> <cmd>` → J1–J4 normalized (−1…+1); rejected in safe-state.
- **Inceptor path:** `inc <idx> <val>` → stick pitch/roll, throttle, pedal stubs.
- **Safe-state:** brownout **or** loss of uplink → neutral actuators (testable via `brownout` / `uplink`).

## Steve / Soft hooks
Machine-readable: `../interfaces/firmware-bringup.yaml`  
BIT topic alias: `bay_io.bit` on ISM-Bus-A (`avionics-bus.yaml`). Host profile substitutes UART/stdio until bus stack lands.

## Out of scope
FCC production laws, Soft UI apps (#79–83), weapon internals.
