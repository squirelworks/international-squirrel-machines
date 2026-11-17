# ISM IDE

PATA/IDE carrier for commodity drives. Original International Squirrel Machines design.

Generate: `python3 scripts/build_ide.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| Host | USB-C (`J1`) bring-up |
| MCU | RP2040 module (`U1`) — DASP / RESET |
| PATA | `ISM_IDE_PATA16` (`J2`) — control/sense; DD bus stubbed |
| Power | `J3` 1×4 drive +5V/GND (+12V external) |
| Shell | Carrier + lid |

## Fab ordering

1. `python3 scripts/build_ide.py`
2. Upload `storage/ide/fab/ism-ide-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd storage/ide/shell && ./export.sh`

### Off-board BOM

- Commodity 2.5"/3.5" PATA drive
- M2 screws (4×)
- Optional external +12V for 3.5" spindles

## Flash

```bash
cd storage/ide/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_ide.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x001C**.

## Steve interface

See `interfaces/ide.yaml`.

## Related

- [#55](https://github.com/squirelworks/international-squirrel-machines/issues/55) · umbrella [#49](https://github.com/squirelworks/international-squirrel-machines/issues/49)
- Follow-ups: [#233](https://github.com/squirelworks/international-squirrel-machines/issues/233)
