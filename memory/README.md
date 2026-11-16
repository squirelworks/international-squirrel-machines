# ISM Memory (RAM modules)

Fab-ready DIMM/SODIMM-style RAM module for the ISM bench — edge connector, SPD EEPROM, simplified DRAM packages, carrier shell.
Original International Squirrel Machines design (not a vendor JEDEC artwork copy).

Generate: `python3 scripts/build_memory.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| Edge | `ISM_SO_DIMM_Edge20` — 20 fingers (power, DQ, CLK/CS/A, SPD I2C) |
| Memory ICs | **Default:** 2× Lyontek `LY68L6400SLIT` (LCSC **C261881**, stock SOIC-8). Optional land: `ISM:ISM_DRAM_SOIC` |
| SPD | Microchip-class `24LC02` SOIC-8 (LCSC) |
| Probe | `J2` 1×4 header (+3V3/GND/SDA/SCL) |
| PCB | 80 × 36 mm, 4-layer |

## Fab ordering

1. `python3 scripts/build_memory.py`
2. Upload `fab/ism-memory-gerbers.zip`
3. SMT: `fab/ism-memory-cpl.csv` + `fab/BOM.csv`
4. `cd shell && ./export.sh` — print carrier tray/lid

### Off-board BOM

- M2 screws (2×) for carrier
- Pico (or ISM RP2040) for SPD probe firmware on J2

## Assembly

1. SMT: DRAM packages, SPD, pull-ups, decoupling.
2. Fit module in carrier tray; edge fingers remain accessible.
3. Optional: attach SPD probe to J2.

## Flash (SPD probe)

```bash
cd memory/firmware
mkdir -p build && cd build
cmake .. && make -j
# copy ism_memory_spd.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x000B**. Wire Pico GP4/GP5 → J2 SDA/SCL.

## Steve interface

| Item | Value |
|------|-------|
| Edge power | `+3V3` (default PSRAM + SPD), `+1V2` (reserved edge rail), `GND` |
| SPD bus | I2C addr `0x50`, SDA/SCL on edge + J2 |
| Probe | J2: 1=+3V3, 2=GND, 3=SDA, 4=SCL |
| Firmware | USB-CDC printf of first 16 SPD bytes |

## Related

- [#110](https://github.com/squirelworks/international-squirrel-machines/issues/110)
