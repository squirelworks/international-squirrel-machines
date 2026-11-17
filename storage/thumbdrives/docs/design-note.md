# Thumb Drive — design note

## Decision
**Wrap** commodity SPI NOR (Winbond W25Q32) on an original ISM USB stick board + shell. Not a vendor stick redesign.

## Form factor
- PCB **70 × 45 mm** (stick-ish; height clears `ISM_RP2040_Module`)
- USB-C receptacle nose, activity LED, reset

## Interface
- TinyUSB bring-up **VID 0x1209 / PID 0x001A**
- SPI: CLK/MOSI/MISO/CS on module pads 2–5; IO2/IO3 pulled to +3V3 for SPI mode

## Follow-ups
USB MSC class, JEDEC ID self-test, QSPI, USB-A plug variant — see gap issue.
