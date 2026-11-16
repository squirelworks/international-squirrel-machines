# ISM Motherboard

Bring-up **motherboard** for the ISM desktop stack.

- RP2040 BMC (USB-C) — southbridge / board management stand-in
- Memory header sharing the ISM 20-net map with `memory/`
- CPU module header (off-board; see #13)
- Expansion SPI/I2C slot for graphics / sound / network cards
- Case-compatible ATX front-panel + motherboard USB headers
- Simplified ATX power input (full 24-pin later)

Form factor: 140×110 mm PCB + printable tray / I/O shield / lid.

Generator: `scripts/build_motherboard.py`. Original ISM design.
