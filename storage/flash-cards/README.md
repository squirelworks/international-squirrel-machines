# ISM Flash Cards

USB microSD reader/adapter for commodity flash cards. Original International Squirrel Machines design.

Generate: `python3 scripts/build_flash_cards.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| Host | USB-C (`J1`) bring-up |
| MCU | RP2040 module (`U1`) — SPI master |
| Media | Hirose DM3AT microSD socket (`J2`, LCSC **C293610**) |
| Shell | Reader body + card silhouette |

## Fab ordering

1. `python3 scripts/build_flash_cards.py`
2. Upload `storage/flash-cards/fab/ism-flash-cards-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd storage/flash-cards/shell && ./export.sh`

### Off-board BOM

- Commodity microSD card
- M2 screws (4×)

## Flash

```bash
cd storage/flash-cards/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_flash_cards.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x0019**.

## Steve interface

See `interfaces/flash-cards.yaml`. DET (pad 6 / GP4) mirrors presence on LED.

## Related

- [#52](https://github.com/squirelworks/international-squirrel-machines/issues/52) · umbrella [#49](https://github.com/squirelworks/international-squirrel-machines/issues/49)
- Follow-ups: [#220](https://github.com/squirelworks/international-squirrel-machines/issues/220)
