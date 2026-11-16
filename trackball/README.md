# ISM Trackball

USB trackball — RP2040, USB-C, optical sensor under a ~34 mm ball cup, 3 buttons + EC11 scroll.
Original International Squirrel Machines design (not QMK / not a third-party PCB clone).

Generate KiCad + fab: `python3 scripts/build_trackball.py`  
Target: **ERC 0 errors**, **DRC 0 errors** (`kicad-cli … --severity-error --exit-code-violations`).

## Layout

| Block | Notes |
|-------|--------|
| MCU | RP2040 QFN-56 (`ISM:RP2040_KB`) |
| USB | GCT USB4105-class USB-C + USBLC6-2SC6 ESD |
| Power | AMS1117-3.3 from VBUS, 12 MHz crystal, W25Q128 QSPI flash |
| Input | 3× PTS645 (L/R/M), Alps EC11 encoder + switch |
| Sensor | `ISM_OpticalSensor` / `ISM_OpticalSensor_8pad` looking up at the ball |
| PCB | 90 × 110 mm, 4-layer |

Project-local lib tables in `kicad/` point at `${KIPRJMOD}/../../common/kicad` for ISM libs and `${KICAD8_SYMBOL_DIR}` / `${KICAD8_FOOTPRINT_DIR}` for stock KiCad 8 libs.

## Fab ordering

1. `python3 scripts/build_trackball.py`
2. Upload `fab/ism-trackball-gerbers.zip` (4-layer gerbers + Excellon drill).
3. SMT: `fab/ism-trackball-cpl.csv` + `fab/BOM.csv` (LCSC where available).
4. `cd shell && ./export.sh` — print `case_bottom.stl` / `case_top.stl` (STEP boxes also in `shell/`).

### Off-board BOM

- ~34 mm trackball (delrin / phenolic)
- PTFE / rubber feet
- M2×6 screws (4×)
- USB-C cable
- Optional: scroll-wheel cap for EC11

## Assembly

1. SMT: MCU, flash, crystal, LDO, ESD, passives, sensor, buttons.
2. THT: USB-C, EC11 encoder.
3. Seat PCB on shell posts; screw M2.
4. Drop ball into cup; confirm sensor window faces the ball underside before closing the top shell.

## Flash

```bash
cd trackball/firmware
# requires PICO_SDK_PATH
mkdir -p build && cd build
cmake ..
make -j
# Hold BOOT, plug USB-C, copy ism_trackball.uf2 to RPI-RP2
```

VID/PID: **0x1209 / 0x0009** (pid.codes ISM allocation).

## Testing

1. Host sees “ISM Trackball” HID boot mouse.
2. Left / right / middle buttons click.
3. Encoder scrolls wheel; encoder switch = middle.
4. Ball motion (after sensor bring-up) moves cursor.

## Steve interface (firmware / host contract)

### USB

| Item | Value |
|------|-------|
| Connector | USB-C receptacle (UFP), CC1/CC2 = 5.1 kΩ to GND |
| Speed | Full-speed USB 2.0 |
| Class | HID boot mouse (`HID_ITF_PROTOCOL_MOUSE`) |
| Report | TinyUSB standard mouse report (buttons, X, Y, wheel) |
| VID/PID | `0x1209` / `0x0009` |
| Strings | Manufacturer `International Squirrel Machines`, Product `ISM Trackball` |

ESD: USBLC6-2SC6 on D+/D−. MCU pins: USB_DM = RP2040 pin 46, USB_DP = pin 47.

### GPIO pinout (RP2040)

| Signal | GPIO | Direction |
|--------|------|-----------|
| BTN_L | GP0 | in, pull-up |
| BTN_R | GP1 | in, pull-up |
| BTN_M | GP2 | in, pull-up |
| ENC_A | GP3 | in, pull-up |
| ENC_B | GP4 | in, pull-up |
| ENC_SW | GP5 | in, pull-up |
| SENS_SCLK | GP6 | SPI0 SCK |
| SENS_MOSI | GP7 | SPI0 TX |
| SENS_MISO | GP8 | SPI0 RX |
| SENS_NCS | GP9 | out |
| SENS_MOTION | GP10 | in, pull-up (active low) |
| SENS_RESET | GP11 | out |

### Protocol

- HID boot-protocol mouse over TinyUSB (`tud_hid_mouse_report`).
- Buttons active-low to GND; firmware ORs ENC_SW into middle button.
- Encoder: gray-code quadrature on ENC_A/ENC_B → wheel delta.
- Sensor: SPI0 @ 1 MHz; MOTION active-low; ball surface replaces mouse pad as the tracked plane.

### Power

- VBUS 5 V from USB-C → AMS1117-3.3 → +3V3 for RP2040, flash, sensor, LED.
- Bulk 10 µF on +5V and +3V3; 100 nF cluster at MCU; crystal load 15 pF.
- Board size: 90 × 110 mm, 4 copper layers (GND stitch on In1, +3V3 on In2; no headless zone pour).

## Related

- [#8](https://github.com/squirelworks/international-squirrel-machines/issues/8) Trackball
- Sibling mouse: `mouse/` (merged in #128)
