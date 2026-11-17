# IDE — design note

## Decision
**Wrap** commodity PATA/IDE drives on an original ISM carrier: simplified PATA header + drive power pass-through + USB-C MCU. ATA data bus stubbed; USB–PATA bridge ASIC is a follow-up.

## Form factor
- PCB **90 × 45 mm** with 2.5"-bay style shell
- `ISM_IDE_PATA16` (16-pin bring-up; not a full 40-pin IDC artwork copy)
- `J3` 1×4 for +5V/GND (+12V external)

## Interface
- TinyUSB **VID 0x1209 / PID 0x001C**
- DASP → LED; RESET pulse on boot; INTRQ / IORDY sense

## Follow-ups
USB–PATA bridge, full 40-pin IDC, proper Molex drive power / +12V rail — see gap issue.
