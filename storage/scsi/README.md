# ISM SCSI

SCSI carrier for commodity drives. Original International Squirrel Machines design.

Generate: `python3 scripts/build_scsi.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| Host | USB-C (`J1`) bring-up |
| MCU | RP2040 module (`U1`) — BSY / RST |
| SCSI | `ISM_SCSI16` (`J2`) — control/sense; DB bus stubbed |
| Power | `J3` 1×4 drive +5V/GND (+12V external) |
| Shell | Carrier + lid |

## Fab ordering

1. `python3 scripts/build_scsi.py`
2. Upload `storage/scsi/fab/ism-scsi-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd storage/scsi/shell && ./export.sh`

### Off-board BOM

- Commodity SCSI drive
- M2 screws (4×)
- Optional external +12V

## Flash

```bash
cd storage/scsi/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_scsi.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x001D**.

## Steve interface

See `interfaces/scsi.yaml`.

## Related

- [#56](https://github.com/squirelworks/international-squirrel-machines/issues/56) · umbrella [#49](https://github.com/squirelworks/international-squirrel-machines/issues/49)
- Follow-ups: [#235](https://github.com/squirelworks/international-squirrel-machines/issues/235)
