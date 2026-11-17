# SCSI — design note

## Decision
**Wrap** commodity SCSI drives on an original ISM carrier: simplified SCSI header + drive power pass-through + USB-C MCU. Data bus stubbed; USB–SCSI bridge ASIC is a follow-up.

## Form factor
- PCB **90 × 45 mm** with drive-bay style shell
- `ISM_SCSI16` (16-pin bring-up; not a full Centronics/IDC artwork copy)
- `J3` 1×4 for +5V/GND (+12V external)

## Interface
- TinyUSB **VID 0x1209 / PID 0x001D**
- BSY → LED; RST pulse on boot; ACK / REQ / SEL sense

## Follow-ups
USB–SCSI bridge, full 50/68-pin IDC, TERMPWR rail, ID switch UI — see gap issue.
