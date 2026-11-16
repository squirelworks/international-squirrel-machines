# ISM Sound Card

I2S stereo DAC card for the ISM motherboard `J_EXP` slot. Original International Squirrel Machines design.

Generate: `python3 scripts/build_sound_card.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| Host | `J1` 1×10 — mates `motherboard/` `J_EXP` |
| Audio MCU | RP2040 module (`U1`) + USB-C bring-up |
| DAC | PCM5102A (`U3`) — I2S, PLL mode (LCSC **C96588**) |
| Output | 3.5 mm TRS (`J3`) — tip L / ring R / sleeve GND |
| Mech | Cooler shroud + slot bracket |

## Fab ordering

1. `python3 scripts/build_sound_card.py`
2. Upload `sound-card/fab/ism-sound-card-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd sound-card/shell && ./export.sh`

### Off-board BOM

- Motherboard with `J_EXP` populated
- Headphones or line cable (3.5 mm TRS)
- M2 screws (4×)

## Flash

```bash
cd sound-card/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_sound_card.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x0016**.

## Steve interface

| Signal | Module pad | GPIO | Notes |
|--------|------------|------|-------|
| EXP_SCK/MOSI/MISO/CS | 2–5 | GP0–3 | From MB `J_EXP` |
| I2S_BCLK/DOUT/LRCLK | 6–8 | GP4–6 | To PCM5102A |
| SDA/SCL | 10–11 | GP8–9 | MB I2C |
| LED_ACT | 19 | GP17 | Heartbeat |
| USB | 16–17 | — | Bring-up |

## Related

- [#15](https://github.com/squirelworks/international-squirrel-machines/issues/15) · follow-up [#207](https://github.com/squirelworks/international-squirrel-machines/issues/207)
- Motherboard [#12](https://github.com/squirelworks/international-squirrel-machines/issues/12) · Graphics [#14](https://github.com/squirelworks/international-squirrel-machines/issues/14)
