# ISM Monitor

USB OSD / HDMI-DDC control board + desk-monitor shell.
Original International Squirrel Machines design.

Generate: `python3 scripts/build_monitor.py` — **ERC 0 / DRC 0**.

Video path: commercial LCD scaler sits off-board; this PCB handles OSD buttons,
EDID/DDC, backlight PWM, and panel enable. HDMI TMDS lands are left for the
scaler harness; DDC/HPD/+5V are on this board.

## Fab ordering

1. `python3 scripts/build_monitor.py`
2. Upload `monitor/fab/ism-monitor-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd monitor/shell && ./export.sh`

### Off-board BOM

- LCD panel + commercial HDMI/LVDS scaler board
- 12 V backlight PSU (or panel-native LED driver)
- M2 screws (4×)
- USB-C cable; HDMI cable

## Flash

```bash
cd monitor/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_monitor.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x000E**.

## Steve interface

| Signal | Module pad | GPIO |
|--------|------------|------|
| BTN_PWR/MENU/UP/DN | 2–5 | GP0–3 |
| BL_PWM / PNL_EN / HPD | 6–8 | GP4–6 |
| I2C SDA/SCL | 9–10 | GP7–8 |
| UART_TX (scaler OSD) | 11 | GP9 |
| USB | 16–17 | DM/DP |

## Related

- [#10](https://github.com/squirelworks/international-squirrel-machines/issues/10)
