# ISM Printer

USB printer **control board** + chassis shell.

- RP2040 MCU (USB-C)
- **DRV8833PWPR** dual H-bridge (LCSC **C50506**) — paper feed + carriage
- Head mezzanine (SPI) for off-board thermal/inkjet module
- Paper sensor header + front panel buttons

Generator: `scripts/build_printer.py`. Original ISM design.
