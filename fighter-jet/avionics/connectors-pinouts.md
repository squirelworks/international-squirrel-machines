# Connector Pinout Drafts — ISM-FJ-1 (#75)

Provisional drafts for harness ICD freeze. Series TBD (circular mil-class intent on article; pin-header study on bay PCB).

## J1–J4 — Actuation study headers (bay PCB → A1–A4)

| Pin | Name | Dir | Notes |
|-----|------|-----|-------|
| 1 | SIG / PWM | Out | Maps to EHA cmd study / servo |
| 2 | 5V | Pwr | Actuator rail (study); article may be discrete only |
| 3 | GND | Ret | Dedicated actuation return — not digital 0 V at FCC |

| Conn | Trunk | Logical surface (#73/#74) |
|------|-------|---------------------------|
| J1 | A1 | Aileron (L study; R via harness split or J1B later) |
| J2 | A2 | HT |
| J3 | A3 | Rudder |
| J4 | A4 | Flaperon / throttle study |

## J_HOTAS — Stick / throttle / pedals feed

| Pin | Signal | Range / type |
|-----|--------|--------------|
| 1–2 | Stick pitch / roll | Normalized ±1 · 100 Hz (`flight-controls.yaml`) |
| 3 | AP disconnect discrete | Active low |
| 4–5 | Throttle L / R | 0…1 |
| 6 | Pedal yaw | ±1 |
| 7–8 | Toe brake L / R | 0…1 |
| 9 | 5V ref | Sensed |
| 10 | GND | Signal |

## J_SENS — Air data / WOW / IMU tray

| Pin | Signal |
|-----|--------|
| 1–2 | Air-data KEAS / static (or digital air-data link) |
| 3–4 | AOA / AoS |
| 5–7 | WOW_NLG, WOW_MLG_L, WOW_MLG_R |
| 8–9 | IMU tray I2C/SPI + sync |
| 10 | GND_sense |

## J_PWR — PDU → bay PCB (P2 family)

| Pin | Rail |
|-----|------|
| 1 | 28 V primary |
| 2 | 28 V essential (battery-backed) |
| 3 | GND_pwr |
| 4 | Power_good discrete |
| 5 | Chassis |

## J_BUS — ISM-Bus A/B stubs on bay I/O

| Pin | Bus |
|-----|-----|
| 1–2 | Bus A H/L (or ISM digital pair) |
| 3–4 | Bus B H/L |
| 5 | Shield |
| 6 | GND |

Article FCC/MC use their own bus connectors; bay I/O is a peer node for HIL/study.
