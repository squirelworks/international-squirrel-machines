# ISM SATA

SATA carrier for commodity drives. Original International Squirrel Machines design.

Generate: `python3 scripts/build_sata.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| Host | USB-C (`J1`) bring-up |
| MCU | RP2040 module (`U1`) — DET / ACT |
| SATA | `ISM_SATA7` (`J2`) — GNDs wired; A/B pairs stubbed |
| Power | `J3` 1×4 drive +5V/GND (+12V external) |
| Shell | Carrier + lid |

## Fab ordering

1. `python3 scripts/build_sata.py`
2. Upload `storage/sata/fab/ism-sata-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd storage/sata/shell && ./export.sh`

### Off-board BOM

- Commodity 2.5"/3.5" SATA drive
- M2 screws (4×)
- Optional external +12V for 3.5" spindles

## Flash

```bash
cd storage/sata/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_sata.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x001E**.

## Steve interface

See `interfaces/sata.yaml`.
