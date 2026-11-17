# ISM Power Supply — design note (Track A)

## Track decision

**Track A:** certified enclosed AC-DC brick supplies **12 V DC** into this board. ISM designs only the **DC rail board** (bucks, connectors, sequencing/monitor, enclosure). No mains copper on ISM Gerbers.

Track B (offline SMPS study) remains documentation-only — see `safety.md`.

## Power budget (bring-up class)

| Rail | Voltage | Tol. | Budget | Source |
|------|---------|------|--------|--------|
| +12V | 12.0 V | ±5% | 3 A pass-through | Brick → barrel `J_IN` |
| +5V | 5.0 V | ±5% | 2 A | LM2596S-5.0 |
| +3.3V | 3.3 V | ±5% | 2 A | LM2596S-3.3 |
| +5VSB | = +5V stub | — | 0.5 A class | Tied to +5V on `J_CTL` pin 4 |

Loads: motherboard BMC + modules (C3), memory (C1), storage later (C2). Totals are bring-up class; production wattage TBD against ATX design-guide clause tables.

## Connectors

| Ref | Role |
|-----|------|
| `J_IN` | 12 V DC barrel (certified brick) |
| `J_OUT` | 1×8 mates `motherboard/` `J_PWR` (12/12/5/5/3V3/3V3/GND/GND) |
| `J_CTL` | PS_ON, PWR_OK, GND, +5VSB |
| `J_USB` | RP2040 bring-up |

## Sequencing

- Bucks always-on when 12 V present (ON/OFF tied GND).
- MCU asserts `PWR_OK` when sense dividers read rails in band after `PS_ON` asserted (active-low ATX convention; see `interfaces/psu.yaml`).

## Thermal (estimate)

LM2596 at ≤2 A / 12→5 and 12→3.3 with TO-263 copper: junction estimate stays below datasheet max with ≥20 °C margin at 40 °C ambient for bring-up loads; validate on first article with thermocouple.
