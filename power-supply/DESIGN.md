# ISM Power Supply

**Track A** DC rail board for the ISM desktop stack.

- 12 V DC in from a certified AC-DC brick (no mains on PCB)
- LM2596 bucks for +5 V and +3.3 V; +12 V pass-through
- Output mates motherboard `J_PWR` 1×8
- RP2040 monitor / PS_ON / PWR_OK
- Printable enclosure + lid with vents

Generator: `scripts/build_power_supply.py`. Original ISM design. See `docs/design-note.md` and `docs/safety.md`.
