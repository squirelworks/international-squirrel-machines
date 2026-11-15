# ISM Fighter Jet — KiCad (Avionics)

Project files:
- `ism-fighter-jet.kicad_pro`
- `ism-fighter-jet.kicad_sch` (avionics schematic scaffold)
- `ism-fighter-jet.kicad_pcb` (board outline scaffold)

## Next implementation steps
1. Expand schematic: IMU (I2C/SPI), radio module, crystal, decoupling, USB-C or UART debug, servo/ESC drivers, power tree (battery → 5 V / 3V3).
2. Associate footprints (QFN MCU, IMU QFN, connectors).
3. Place components in the avionics-bay outline; route power and buses.
4. Export Gerbers.

Pure Squirrel-OS/2 development. Scaffold complete; ready for expansion.
