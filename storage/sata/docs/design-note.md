# SATA — design note

## Approach

**Wrap** commodity SATA drives on an original ISM carrier: simplified SATA data header + drive power pass-through + USB-C MCU. A/B differential pairs stubbed; USB–SATA bridge ASIC is a follow-up.

## Connector

- `ISM_SATA7` (7-pin bring-up; not a vendor SATA receptacle artwork copy)
- Pins 1/4/7 GND; 2/3/5/6 A±/B± NC on this PCB

## Firmware

- TinyUSB **VID 0x1209 / PID 0x001E**
- DET sense (pad 2 / GP0) drives ACT LED; pairs remain stubbed

## Follow-ups

USB–SATA bridge, full SATA receptacle, +12V rail, activity from drive LED pin — see gap issue.
