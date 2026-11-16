# ISM Network Card

SPI Ethernet NIC for the ISM motherboard `J_EXP` slot. Original International Squirrel Machines design.

Generate: `python3 scripts/build_network_card.py` — **ERC 0 / DRC 0**.

## Layout

| Block | Notes |
|-------|--------|
| Host | `J1` 1×10 — mates `motherboard/` `J_EXP` |
| NIC MCU | RP2040 module (`U1`) + USB-C bring-up |
| PHY/MAC | W5500 (`U3`) — SPI Ethernet (LCSC **C113367**) |
| Port | RJ45 HR911105A (`J3`) with magnetics (LCSC **C2839419**) |
| Clock | 25 MHz crystal (`Y1`) |
| Mech | Cooler shroud + slot bracket |

## Fab ordering

1. `python3 scripts/build_network_card.py`
2. Upload `network-card/fab/ism-network-card-gerbers.zip`
3. SMT: CPL + `BOM.csv`
4. `cd network-card/shell && ./export.sh`

### Off-board BOM

- Motherboard with `J_EXP` populated
- Cat5e/Cat6 patch cable
- M2 screws (4×)

## Flash

```bash
cd network-card/firmware
mkdir -p build && cd build && cmake .. && make -j
# copy ism_network_card.uf2 to RPI-RP2
```

VID/PID **0x1209 / 0x0017**.

## Steve interface

| Signal | Module pad | GPIO | Notes |
|--------|------------|------|-------|
| EXP_SCK/MOSI/MISO/CS | 2–5 | GP0–3 | From MB `J_EXP` |
| ETH_SCLK/MOSI/MISO/CS | 6–9 | GP4–7 | To W5500 SPI |
| SDA/SCL | 10–11 | GP8–9 | MB I2C |
| ETH_INT / ETH_RST | 12–13 | GP10–11 | W5500 |
| LED_ACT | 19 | GP17 | Heartbeat / INT mirror |
| USB | 16–17 | — | Bring-up |

## Related

- [#16](https://github.com/squirelworks/international-squirrel-machines/issues/16) · follow-up [#212](https://github.com/squirelworks/international-squirrel-machines/issues/212)
- Motherboard [#12](https://github.com/squirelworks/international-squirrel-machines/issues/12) · Sound [#15](https://github.com/squirelworks/international-squirrel-machines/issues/15)
