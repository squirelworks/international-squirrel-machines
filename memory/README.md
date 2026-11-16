# ISM Memory (RAM modules)

Planned fab-ready DIMM / SODIMM-style RAM modules for the ISM bench.

## Scope
- JEDEC-inspired module outline (original ISM design; not a copy of vendor artwork)
- KiCad schematic + PCB (`memory/kicad/`) with edge connector, SPD EEPROM, decoupling
- `fab/` gerbers, CPL, BOM.csv (LCSC where possible)
- OpenSCAD carrier / handling shell with STL + STEP (`memory/shell/`)
- Optional bring-up firmware only if an onboard MCU/test header is used
- README: ordering, assembly, pinout, power ratings, and USB/test interfaces for Steve

## Status
Scaffolded. Tracked by issue #110. Implementation after peripherals.
