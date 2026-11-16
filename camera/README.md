# ISM Camera

USB camera controller + enclosure. Original International Squirrel Machines design.

Generate: `python3 scripts/build_camera.py` — **ERC 0 / DRC 0**.

Image sensor is an off-board OV2640-class module on `J2`.

## Fab ordering

1. `python3 scripts/build_camera.py`
2. Upload `camera/fab/ism-camera-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd camera/shell && ./export.sh`

### Off-board BOM

- OV2640 (or compatible) camera module
- Lens / IR filter as required by module
- M2 screws (4×); USB-C cable

## Flash

```bash
cd camera/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_camera.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x0011**.

## Steve interface

| Signal | Module pad | GPIO |
|--------|------------|------|
| CAM SDA/SCL | 2–3 | GP0–1 |
| XCLK/PCLK/VSYNC/HREF | 4–7 | GP2–5 |
| RST/PWDN | 8–9 | GP6–7 |
| D0–D3 | 10–13 | GP8–11 |
| BTN_SHUT/MODE | 19–20 | GP15–16 |
| USB | 16–17 | DM/DP |

## Related

- [#7](https://github.com/squirelworks/international-squirrel-machines/issues/7)
