# ISM Keyboard — 65%

ANSI 65% (5×14 matrix, 70 keys: 61-key 60% block + 9-key nav cluster), RP2040 module carrier, USB-C, MX hotswap pads, printable shell.
Original International Squirrel Machines design (not QMK / not a third-party PCB clone).

Generate KiCad + fab: `python3 scripts/build_keyboard_65.py`  
Target: **ERC 0 errors**, **DRC 0 errors** (`kicad-cli … --severity-error --exit-code-violations`).

## Layout

| Block | Notes |
|-------|--------|
| MCU | `ISM_RP2040_Module` carrier (`ISM:RP2040_MOD`) — 2.54 mm breakout |
| USB | GCT USB4105-class USB-C + USBLC6-2SC6 ESD |
| Matrix | 70× MX hotswap + SOD-123 1N4148W (cathode → COL); nav keys on spare intersections |
| Nav | DEL, PGUP, PGDN, HOME, END, arrows |
| Routing | ROW on In1.Cu, COL on In2.Cu, blind vias F↔inner |

Project-local lib tables in `kicad/` point at `${KIPRJMOD}/../../common/kicad` for ISM libs and `${KICAD8_SYMBOL_DIR}` / `${KICAD8_FOOTPRINT_DIR}` for stock KiCad 8 libs.

## Fab ordering

1. `python3 scripts/build_keyboard_65.py`
2. Upload `fab/ism-keyboard-65-gerbers.zip` (4-layer gerbers + Excellon drill).
3. SMT: `fab/ism-keyboard-65-cpl.csv` + `fab/BOM.csv` (LCSC where available).
4. Print `shell/case_*.stl` (STEP boxes also in `shell/` via `./export.sh`).

### Off-board BOM

- 70× MX-compatible switches
- 70× keycaps (ANSI 65% set)
- Stabilizers for 2u+ keys
- Plate (optional; `shell/case_plate.stl`)
- Case bottom + top frame (`shell/export.sh`)
- M2 screws, USB-C cable
- RP2040 module matching `ISM_RP2040_Module` pinout

## Shell

```bash
cd keyboard/65-percent/shell
./export.sh   # STL + approximate STEP boxes
```

## Flash

```bash
cd keyboard/65-percent/firmware
mkdir -p build && cd build
cmake ..   # needs PICO_SDK_PATH
make -j
# BOOT + UF2 → RPI-RP2
```

VID/PID: **0x1209 / 0x0002**.

## Testing

1. Host enumerates “ISM Keyboard 65%”.
2. Matrix keys type; nav cluster and modifiers work.
3. USB suspend/resume still enumerates.

## Steve interfaces

### USB HID

- Boot keyboard HID (`HID_ITF_PROTOCOL_KEYBOARD`)
- Standard 8-byte keyboard report (modifier + 6 keys)
- Manufacturer `International Squirrel Machines`, Product `ISM Keyboard 65%`

### GPIO / matrix (module pin ↔ RP2040 GPIO)

| Net | Module pad | Typical GP | Role |
|-----|------------|------------|------|
| ROW0–ROW4 | 2–6 | GP0–GP4 | Row drive (active low) |
| COL0–COL13 | 7–13, 19–25 | GP5–GP18 | Column sense (pull-up, active low) |
| USB_DM / USB_DP | 16 / 17 | USB PHY | USB 2.0 |
| +5V / +3V3 / GND | 15 / 14 / 1,26 | — | Power |
| RUN | 18 | RUN | 10 kΩ pull-up + reset button |

Diodes: cathode toward COL, anode toward switch toward ROW.

Nav electrical map (physical right column / arrow cluster):

| Key | Electrical |
|-----|------------|
| DEL | R2 C13 |
| PGUP | R3 C12 |
| PGDN | R3 C13 |
| HOME | R4 C8 |
| END | R4 C9 |
| UP | R4 C10 |
| LEFT | R4 C11 |
| DOWN | R4 C12 |
| RIGHT | R4 C13 |

## Related

- Roadmap issue: [#62](https://github.com/squirelworks/international-squirrel-machines/issues/62)
- Sibling: `keyboard/60-percent/` (PR #128)
