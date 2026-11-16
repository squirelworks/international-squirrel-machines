# ISM Computer Case

Smart front-panel PCB + OpenSCAD chassis. Original International Squirrel Machines design.

Generate: `python3 scripts/build_case.py` — **ERC 0 / DRC 0**.

## Fab ordering

1. `python3 scripts/build_case.py`
2. Upload `case/fab/ism-case-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd case/shell && ./export.sh`

### Off-board / chassis BOM

- Mini-ITX (or similar) motherboard + PSU
- ATX front-panel ribbon to `J2`
- Motherboard USB2 header cable to `J5`
- M3 screws for chassis / FP bosses; M2 for FP PCB
- USB-C cable for MCU flash / HID

## Flash

```bash
cd case/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_case.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x0012**.

## Steve interface

| Signal | Module pad | GPIO | Notes |
|--------|------------|------|-------|
| BTN_PWR | 2 | GP0 | Front power button |
| BTN_RST | 3 | GP1 | Front reset button |
| LED_PWR | 4 | GP2 | Panel power LED |
| LED_HDD | 5 | GP3 | Panel activity LED |
| ATX_PWR_SW | 6 | GP4 | To MB PWR_SW via J2 |
| ATX_RST_SW | 7 | GP5 | To MB RST_SW via J2 |
| ATX_PWR_LED | 8 | GP6 | From MB PWR_LED |
| ATX_HDD_LED | 9 | GP7 | From MB HDD_LED |
| USB DM/DP | 16–17 | — | USB-C programming / HID |
| Front USB-A | J3/J4 | — | Passthrough to J5 MB USB |

### Connectors

| Ref | Role |
|-----|------|
| J1 | USB-C (MCU) |
| J2 | ATX front-panel 1×10 |
| J3/J4 | Front USB-A |
| J5 | Motherboard USB2 1×4 |

## Related

- [#11](https://github.com/squirelworks/international-squirrel-machines/issues/11)
