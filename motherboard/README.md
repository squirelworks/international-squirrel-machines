# ISM Motherboard

BMC bring-up board with memory / CPU / expansion headers and case-compatible ATX FP + USB. Original International Squirrel Machines design.

Generate: `python3 scripts/build_motherboard.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| BMC | RP2040 module (`U1`) + USB-C |
| Memory | `J_MEM` 1×20 — same net map as `memory/` edge |
| CPU | `J_CPU` 2×10 — off-board module (#13) |
| Expansion | `J_EXP` 1×10 SPI/I2C for graphics/sound/network |
| Case | `J_FP` / `J_USB` match `case/` front panel |
| Power | `J_PWR` 1×8 bring-up ATX rails |
| ID | 24LC02 board EEPROM (LCSC **C7500**) |

## Fab ordering

1. `python3 scripts/build_motherboard.py`
2. Upload `motherboard/fab/ism-motherboard-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd motherboard/shell && ./export.sh`

### Off-board BOM

- ISM memory module (`memory/`) via adapter to `J_MEM`
- ISM CPU module (#13) on `J_CPU`
- Case FP ribbon to `J_FP`; front USB cable to `J_USB`
- Bench/ATX PSU leads to `J_PWR`; external **+1V2** for memory option
- M2 screws (4×)

## Flash

```bash
cd motherboard/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_motherboard.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x0013**.

## Steve interface

| Signal | Module pad | GPIO |
|--------|------------|------|
| CLK/CS | 2–3 | GP0–1 |
| DQ0–DQ3 | 4–7 | GP2–5 |
| A0/A1 | 8–9 | GP6–7 |
| SDA/SCL | 10–11 | GP8–9 |
| CPU_TX/RX | 12–13 | GP10–11 |
| CPU_RST | 19 | GP17 |
| LED_ACT | 20 | GP18 |
| WP | 21 | GP19 |
| EXP SPI | 22–25 | GP20–23 |
| USB | 16–17 | DM/DP |

## Related

- [#12](https://github.com/squirelworks/international-squirrel-machines/issues/12)
- Case [#11](https://github.com/squirelworks/international-squirrel-machines/issues/11) · Memory [#110](https://github.com/squirelworks/international-squirrel-machines/issues/110) · CPU [#13](https://github.com/squirelworks/international-squirrel-machines/issues/13)
