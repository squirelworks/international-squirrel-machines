# ISM shared KiCad libraries

Original International Squirrel Machines symbols and footprints used by more than
one device.

## Contents

- `ISM.kicad_sym` — project symbols (simplified RP2040 for keyboards/mice, MX
  switch, ISM optical mouse sensor, …)
- `ISM.pretty/` — footprints (`SW_MX_*`, diode helpers, `ISM_OpticalSensor_8pad`, …)

## Stock KiCad libraries

Device projects also embed or reference **stock KiCad 8** symbol and footprint
libraries shipped with KiCad (for example `Device`, `power`, `Connector`,
`Connector_USB`, `Package_DFN_QFN`, `Package_SO`, `Package_TO_SOT_SMD`,
`Memory_Flash`, `Power_Protection`, `Regulator_Linear`, `Switch`, `Crystal`,
`Rotary_Encoder`, `Button_Switch_SMD`, `Resistor_SMD`, `Capacitor_SMD`,
`LED_SMD`, `MountingHole`).

Those stock libraries are © their respective KiCad library contributors and are
used here under the KiCad library license terms. ISM-authored symbols and
footprints in this directory are original ISM work and are **not** copies of
third-party keyboard or mouse PCB libraries.
