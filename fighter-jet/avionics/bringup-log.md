# Bay I/O Bring-up Log — ISM-FJ-1 (A1 / #84 / #119)

Checklist for study-scale bay board (`../kicad/`) + host firmware (`../firmware/`).
Not the quadruplex FCC article bring-up.

**MCU:** RP2040 (schematic `ISM:MCU`). Datasheet: Raspberry Pi RP2040.  
**Rails on board:** 3V3, 5V, GND (28 V essential is upstream).  
**Debug:** UART/stdio host profile now; SWD/USB on article later.

## Rails
- [ ] 3V3 present at U1 / U2 / U3 (no brownout BIT)
- [ ] 5V present at J1–J4 pin 2
- [ ] GND continuity EP / headers / MH
- [ ] Brownout inject (SS-BO-01) → safe, actuators neutral

## Clock / debug
- [ ] Host `make && make test` clean (0 errors / 0 warnings at `-Wall -Wextra -Werror`)
- [ ] `make run` emits BIT line with `board=ISM-FJ-BAY-IO`
- [ ] (Article) SWD attach / USB CDC — deferred until fab

## IMU (U2)
- [ ] I2C SDA/SCL wired; ACK on bus (or host stub `imu=1`)
- [ ] Self-test bit in BIT frame (`imu`)
- [ ] Calibration keys load from `parameters/ism-fj-1.ismfj-params`

## Radio (U3)
- [ ] SPI SCK/MOSI/MISO wired; `radio` BIT healthy in stub
- [ ] `DISC_RADIO_ENABLE` inactive in safe-state

## Actuator channels (J1–J4 → A1–A4)
- [ ] J1 PWM_AIL — cmd accepted when not safe; rejected in safe
- [ ] J2 PWM_ELE — same
- [ ] J3 PWM_RUD — same
- [ ] J4 PWM_THR — same
- [ ] SS-UL-01 uplink loss → all neutral
- [ ] SS-WD-01 watchdog → hold safe
- [ ] SS-IN-01 inceptor loss → actuators neutral

## Inceptors
- [ ] Stick pitch/roll, throttle, pedal stubs via `inc` host cmds
- [ ] Loss timeout per params (`inceptor.loss_timeout_ms`)

## Bus / Soft hooks
- [ ] `bay_io.bit` topic present in `interfaces/avionics-bus.yaml`
- [ ] Topics for #81/#82/#83 present (see bus YAML A1 block)
- [ ] `bit-frame.yaml` / `safe-state.yaml` / `bay-io.ismfj-iface` load without unknown keys

## References (pattern only — not “compliant”)
- MIL-STD-704F — brownout/transient test category ideas
- MIL-STD-1553B Notice 2 — scheduled BIT framing idea
- NASA SP-2016-6105 Rev 2 — ICD / verification matrix practice
