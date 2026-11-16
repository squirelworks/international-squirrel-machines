# ISM Plotter

USB X/Y plotter controller + frame. Original International Squirrel Machines design.

Generate: `python3 scripts/build_plotter.py` — **ERC 0 / DRC 0**.

## Fab ordering

1. `python3 scripts/build_plotter.py`
2. Upload `plotter/fab/ism-plotter-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd plotter/shell && ./export.sh`

### Off-board BOM

- X/Y gantry motors + rails
- Pen holder / servo for lift
- Limit switches (X, Y) + pen home
- 9 V motor PSU; M2 screws; USB-C cable

## Flash

```bash
cd plotter/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_plotter.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x0010**.

## Steve interface

| Signal | Module pad | GPIO |
|--------|------------|------|
| AIN1/AIN2 / BIN1/BIN2 | 2–5 | GP0–3 |
| nSLEEP | 6 | GP4 |
| PEN_LIFT / LIM_X / LIM_Y | 7–9 | GP5–7 |
| PEN_HOME | 10 | GP8 |
| BTN_HOME/STOP/PWR | 11–13 | GP9–11 |
| USB | 16–17 | DM/DP |

## Related

- [#6](https://github.com/squirelworks/international-squirrel-machines/issues/6)
