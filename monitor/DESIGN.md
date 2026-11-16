# ISM Monitor

Desk monitor **control/UI board** + bezel shell.

- RP2040 OSD MCU (USB-C HID/config)
- HDMI Type-A input (DDC / HPD / +5V on-board; TMDS to off-board scaler)
- AT24C02C EDID/config EEPROM (LCSC **C6203**)
- Backlight MOSFET (2N7002) + 12 V LED header
- Panel mezzanine to commercial LCD controller

Generator: `scripts/build_monitor.py`. Original ISM design.
