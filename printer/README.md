# ISM Printer

USB printer controller + chassis. Original International Squirrel Machines design.

Generate: `python3 scripts/build_printer.py` — **ERC 0 / DRC 0**.

Motors (feed + carriage) use on-board **DRV8833PWPR**. Print head and paper
path mechanics are off-board modules linked via `J4` / `J5`.

## Fab ordering

1. `python3 scripts/build_printer.py`
2. Upload `printer/fab/ism-printer-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd printer/shell && ./export.sh`

### Off-board BOM

- DC motors (feed + carriage) or geared equivalents
- Thermal/inkjet head module
- Paper photointerrupter
- 9 V motor PSU
- M2 screws (4×); USB-C cable

## Flash

```bash
cd printer/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_printer.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x000F**.

## Steve interface

| Signal | Module pad | GPIO |
|--------|------------|------|
| AIN1/AIN2 / BIN1/BIN2 | 2–5 | GP0–3 |
| nSLEEP | 6 | GP4 |
| HEAD SPI CS/SCK/MOSI | 7–9 | GP5–7 |
| PAPER_SENS | 10 | GP8 |
| BTN_FEED/CANCEL/PWR | 11–13 | GP9–11 |
| USB | 16–17 | DM/DP |

## Related

- [#5](https://github.com/squirelworks/international-squirrel-machines/issues/5)
