# ISM CPU

Pluggable **CPU module** for the ISM desktop stack.

- RP2040 compute core (USB-C bring-up)
- W25Q32 SPI/QSPI flash on the motherboard memory-bus stub nets
- 2×10 header matching `motherboard/` `J_CPU` (UART + I2C + reset + power)
- Printable finned heatsink shroud

Architecture: soft CPU / BMC co-processor stand-in until a discrete ISM ISA lands.

Generator: `scripts/build_cpu.py`. Original ISM design.
