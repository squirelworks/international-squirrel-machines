# ISM Keyboard — 60%

ANSI 60% (5×14 matrix), RP2040 module carrier, USB-C, MX hotswap pads, printable shell.
Original International Squirrel Machines design (not QMK / not a third-party PCB clone).

Generate KiCad + fab: `python3 scripts/build_keyboard_final.py`  
Target: **ERC 0 errors**, **DRC 0 errors** (`kicad-cli … --severity-error --exit-code-violations`).

## Layout

| Block | Notes |
|-------|--------|
| MCU | `ISM_RP2040_Module` carrier (`ISM:RP2040_MOD`) — 2.54 mm breakout |
| USB | GCT USB4105-class USB-C + USBLC6-2SC6 ESD |
| Matrix | 61× MX hotswap + SOD-123 1N4148W (cathode → COL) |
| Routing | ROW on In1.Cu, COL on In2.Cu, blind vias F↔inner |

Project-local lib tables in `kicad/` point at `${KIPRJMOD}/../../common/kicad` for ISM libs and `${KICAD8_SYMBOL_DIR}` / `${KICAD8_FOOTPRINT_DIR}` for stock KiCad 8 libs.

## Fab ordering

1. `python3 scripts/build_keyboard_final.py`
2. Upload `fab/ism-keyboard-60-gerbers.zip` (4-layer gerbers + Excellon drill).
3. SMT: `fab/ism-keyboard-60-cpl.csv` + `fab/BOM.csv` (LCSC where available).
4. Print `shell/case_*.stl` (STEP boxes also in `shell/` via `./export.sh`).

### Off-board BOM

- 61× MX-compatible switches
- 61× keycaps (ANSI 60% set)
- Stabilizers for 2u+ keys
- Plate (optional; `shell/case_plate.stl`)
- Case bottom + top frame (`shell/export.sh`)
- M2 screws, USB-C cable
- RP2040 module matching `ISM_RP2040_Module` pinout

## Shell

```bash
cd keyboard/60-percent/shell
./export.sh   # STL + approximate STEP boxes
```

## Flash

```bash
cd keyboard/60-percent/firmware
mkdir -p build && cd build
cmake ..   # needs PICO_SDK_PATH
make -j
# BOOT + UF2 → RPI-RP2
```

VID/PID: **0x1209 / 0x0001**.

## Testing

1. Host enumerates “ISM Keyboard 60%”.
2. Matrix keys type; modifiers work.
3. USB suspend/resume still enumerates.

## Steve interfaces

### USB HID

- Boot keyboard HID (`HID_ITF_PROTOCOL_KEYBOARD`)
- Standard 8-byte keyboard report (modifier + 6 keys)
- Manufacturer `International Squirrel Machines`, Product `ISM Keyboard 60%`

### GPIO / matrix (module pin ↔ RP2040 GPIO)

| Net | Module pad | Typical GP | Role |
|-----|------------|------------|------|
| ROW0–ROW4 | 2–6 | GP0–GP4 | Row drive (active low) |
| COL0–COL13 | 7–13, 19–25 | GP5–GP18 | Column sense (pull-up, active low) |
| USB_DM / USB_DP | 16 / 17 | USB PHY | USB 2.0 |
| +5V / +3V3 / GND | 15 / 14 / 1,26 | — | Power |
| RUN | 18 | RUN | 10 kΩ pull-up + reset button |

Diodes: cathode toward COL, anode toward switch toward ROW.

### Power

- USB-C VBUS → USBLC6 ESD → module 5 V / onboard 3V3
- CC1/CC2 5.1 kΩ to GND
- Local 100 nF cluster at module +3V3
