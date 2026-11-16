# ISM Graphics Card

SPI GPU controller card for the ISM motherboard `J_EXP` slot. Original International Squirrel Machines design.

Generate: `python3 scripts/build_graphics_card.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| Host | `J1` 1×10 — mates `motherboard/` `J_EXP` |
| GPU MCU | RP2040 module (`U1`) + USB-C bring-up |
| Output | HDMI Type-A (`J3`) — DDC/HPD/CEC/+5V on board; **TMDS off-board** |
| EDID | AT24C02C (LCSC **C6203**) |
| Framebuffer | Lyontek LY68L6400SLIT (LCSC **C261881**) |
| Mech | Cooler shroud + slot bracket |

## Fab ordering

1. `python3 scripts/build_graphics_card.py`
2. Upload `graphics-card/fab/ism-graphics-card-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd graphics-card/shell && ./export.sh`

### Off-board BOM

- Motherboard with `J_EXP` populated
- HDMI TMDS PHY / scaler module (harness to `J3` TMDS pads)
- M2 screws (4×); HDMI cable

## Flash

```bash
cd graphics-card/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_graphics_card.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x0015**.

## Steve interface

| Signal | Module pad | GPIO | Notes |
|--------|------------|------|-------|
| EXP_SCK/MOSI/MISO/CS | 2–5 | GP0–3 | From MB `J_EXP` |
| FB_CLK/CS/DQ0/DQ1 | 6–9 | GP4–7 | Framebuffer SPI |
| SDA/SCL | 10–11 | GP8–9 | MB I2C |
| HPD/CEC | 12–13 | GP10–11 | HDMI |
| LED_ACT | 19 | GP17 | Activity / HPD mirror |
| HDMI_SDA/SCL | 20–21 | GP18–19 | EDID DDC |
| USB | 16–17 | — | Bring-up |

## Related

- [#14](https://github.com/squirelworks/international-squirrel-machines/issues/14)
- Motherboard [#12](https://github.com/squirelworks/international-squirrel-machines/issues/12) · Monitor [#10](https://github.com/squirelworks/international-squirrel-machines/issues/10)
