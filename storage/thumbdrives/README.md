# ISM Thumb Drives

USB-MSC stick board wrapping commodity SPI NOR flash. Original International Squirrel Machines design.

Generate: `python3 scripts/build_thumbdrives.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| Host | USB-C (`J1`) bring-up |
| MCU | RP2040 module (`U1`) — SPI master / MSC controller |
| Media | Winbond **W25Q32JVSS** SOIC-8 (`U3`, LCSC **C82307**) |
| Shell | Stick body + end cap |

## Fab ordering

1. `python3 scripts/build_thumbdrives.py`
2. Upload `storage/thumbdrives/fab/ism-thumbdrives-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd storage/thumbdrives/shell && ./export.sh`

### Off-board BOM

- M2 screws (4×)

## Flash

```bash
cd storage/thumbdrives/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_thumbdrives.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x001A**.

## Steve interface

See `interfaces/thumbdrives.yaml`. Activity LED heartbeat until MSC lands.

## Related

- [#53](https://github.com/squirelworks/international-squirrel-machines/issues/53) · umbrella [#49](https://github.com/squirelworks/international-squirrel-machines/issues/49)
- Follow-ups: [#225](https://github.com/squirelworks/international-squirrel-machines/issues/225)
