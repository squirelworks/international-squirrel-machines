# ISM Typewriter

Mechanical + electronics hybrid typewriter — RP2040 module controller, USB-C, 4×12 MX hot-swap matrix, carriage-bay shell.
Original International Squirrel Machines design (not QMK).

Generate: `python3 scripts/build_typewriter.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| MCU | `ISM_RP2040_Module` ROW0–3 / COL0–11 |
| USB | GCT USB-C + USBLC6-2SC6 |
| Matrix | 48× MX hot-swap + 1N4148W |
| Shell | Deep case + plate + carriage hood channel |
| PCB | ~304 × 250 mm class, 4-layer |

## Fab ordering

1. `python3 scripts/build_typewriter.py`
2. Upload `fab/ism-typewriter-gerbers.zip`
3. SMT: `fab/ism-typewriter-cpl.csv` + `fab/BOM.csv`
4. `cd shell && ./export.sh`

### Off-board BOM

- 48× MX switches + typewriter-style keycaps
- M2×6 screws (4×)
- USB-C cable
- Optional: carriage / platen mechanicals (future)

## Assembly

1. SMT diodes/passives/ESD; fit RP2040 module + USB-C.
2. Hot-swap sockets + switches.
3. Seat PCB in shell; fit plate; carriage hood over rear bay.

## Flash

```bash
cd typewriter/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_typewriter.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x000C**. HID boot keyboard.

## Steve interface

Same GPIO map as 40% keyboard (ROW GP0–3, COL GP5–16). USB HID keyboard.

## Related

- [#4](https://github.com/squirelworks/international-squirrel-machines/issues/4)
