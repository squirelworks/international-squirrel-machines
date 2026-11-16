# ISM Memory (RAM modules)

SODIMM-inspired **80×36 mm** module: 20-finger edge, SPD `24LC02`, J2 I2C header.

**Default population:** 2× Lyontek **LY68L6400SLIT** 64 Mbit SPI/QPI PSRAM (LCSC **C261881**, stock SOIC-8).
**Optional:** `ISM:ISM_DRAM_SOIC` land pattern for a custom ISM DRAM package (not default SMT).

Generator: `scripts/build_memory.py`. Original ISM design (not a vendor JEDEC artwork copy).
