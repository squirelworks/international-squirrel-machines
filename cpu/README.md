# ISM CPU

Compute daughtercard for the ISM motherboard `J_CPU` 2×10. Original International Squirrel Machines design.

Generate: `python3 scripts/build_cpu.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| Core | RP2040 module (`U1`) |
| Flash | Winbond **W25Q32JVSS** SOIC-8 (LCSC **C82307**) on CLK/CS/DQ0–3 |
| Host | `J1` 2×10 — mates `motherboard/` `J_CPU` net map |
| Debug | USB-C for standalone flash / HID |
| Mech | Printable heatsink shroud + base plate |

## Fab ordering

1. `python3 scripts/build_cpu.py`
2. Upload `cpu/fab/ism-cpu-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd cpu/shell && ./export.sh`

### Off-board BOM

- Motherboard with `J_CPU` populated (`motherboard/`)
- M2 screws (4×); thermal pad optional under shroud fins
- USB-C cable for bring-up

## Flash

```bash
cd cpu/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_cpu.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x0014**.

## Steve interface

| Signal | Module pad | GPIO | MB `J_CPU` |
|--------|------------|------|------------|
| CLK/CS | 2–3 | GP0–1 | 5–6 |
| DQ0–DQ3 | 4–7 | GP2–5 | 7–10 |
| A0/A1 | 8–9 | GP6–7 | 11–12 |
| SDA/SCL | 10–11 | GP8–9 | 13–14 |
| CPU_TX/RX | 12–13 | GP10–11 | 15–16 |
| CPU_RST | 19 | GP17 | 17 |
| LED_ACT | 20 | GP18 | — |
| USB | 16–17 | — | — |
| +12V | — | — | 18 (parked; future Vcore) |

## Related

- [#13](https://github.com/squirelworks/international-squirrel-machines/issues/13)
- Motherboard [#12](https://github.com/squirelworks/international-squirrel-machines/issues/12)
