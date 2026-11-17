# NVMe — design note

## Decision
**Wrap** commodity M.2 2280 NVMe SSDs on an original ISM carrier: Key-M socket + USB-C power/presence MCU. PCIe lanes are stubbed; a USB–NVMe bridge ASIC is a follow-up (not on this PCB).

## Form factor
- PCB **100 × 45 mm** with 2280 bay + `H_M2` retention screw
- Simplified `ISM_M2_KeyM_Socket` (16-pin bring-up; not a JEDEC artwork copy)

## Interface
- TinyUSB **VID 0x1209 / PID 0x001B**
- PEDET → LED; PERST release on boot; CLKREQ sense; DEVSLP held low

## Follow-ups
USB–NVMe bridge, full Key-M pinout / Molex socket, 3 A +3V3 rail, 2242/2260 bays — see gap issue.
