# ISM Power Supply

DC-side ATX-style rail board for the ISM stack (**Track A** — certified 12 V brick off-board; **no mains** on this PCB). Original International Squirrel Machines design.

Generate: `python3 scripts/build_power_supply.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| Input | `J_IN` barrel — 12 V from certified AC-DC brick |
| Bucks | LM2596S-5.0 (`U3`) + LM2596S-3.3 (`U4`) |
| Output | `J_OUT` 1×8 — mates `motherboard/` `J_PWR` |
| Control | `J_CTL` — PS_ON / PWR_OK / 5VSB stub |
| Monitor | RP2040 (`U1`) + USB-C |
| Docs | `docs/design-note.md`, `docs/safety.md`, `interfaces/psu.yaml` |

## Fab ordering

1. `python3 scripts/build_power_supply.py`
2. Upload `power-supply/fab/ism-power-supply-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd power-supply/shell && ./export.sh`

### Off-board BOM

- **Certified** 12 V AC-DC brick / wall adapter (SELV)
- Harness `J_OUT` → motherboard `J_PWR`
- Optional fan for enclosure grille; M2 screws (4×)

## Flash

```bash
cd power-supply/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_power_supply.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x0018**.

## Steve interface

See `interfaces/psu.yaml`. Summary:

| Signal | Module pad | GPIO | Notes |
|--------|------------|------|-------|
| PS_ON | 2 | GP0 | Active-low ATX |
| PWR_OK | 3 | GP1 | Assert when rails OK |
| SNS_12/5/3V3 | 4–6 | GP2–4 | Divider sense |
| LED_ACT | 19 | GP17 | Status |

## Related

- [#23](https://github.com/squirelworks/international-squirrel-machines/issues/23) · follow-up [#216](https://github.com/squirelworks/international-squirrel-machines/issues/216)
- Motherboard [#12](https://github.com/squirelworks/international-squirrel-machines/issues/12) · UPS [#29](https://github.com/squirelworks/international-squirrel-machines/issues/29)
