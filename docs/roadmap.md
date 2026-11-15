# International Squirrel Machines — Roadmap

Pure Squirrel-OS/2 Warp-style hardware. Scaffold → implement → polish → inquire for release.

## Phase 0 — Repository Scaffold (complete)
- [x] Repository created
- [x] Core documentation (principles, branding, devices)
- [x] Device directory stubs (including drawing pads range)
- [x] Roadmap
- [ ] Issues created for every device (in progress)

## Phase 1 — Keyboard (first production device)
**Directory:** `keyboard/`
- [ ] Design note: layout, MCU, matrix, hot-swap, mounting
- [ ] KiCad schematic + PCB (`keyboard/kicad/`)
- [ ] Parametric OpenSCAD shell (`keyboard/shell/`) — top/bottom, USB, ISM badge
- [ ] First Gerbers + STLs
- [ ] BOM, assembly notes, renders
- [ ] Polish and inquire for release

## Phase 2 — Input Devices
- [ ] Mouse (`mouse/`)
- [ ] Trackball (`trackball/`)
- [ ] Macro pad (`macro-pad/`)
- [ ] Typewriter (`typewriter/`)
- [ ] Drawing pads range — small / medium / large (`drawing-pads/`)

## Phase 3 — Output Devices
- [ ] Monitor (`monitor/`)
- [ ] Printer (`printer/`)
- [ ] Plotter (`plotter/`)
- [ ] Camera (`camera/`)

## Phase 4 — Core System
- [ ] Computer case (`case/`)
- [ ] Motherboard (`motherboard/`)
- [ ] CPU (`cpu/`)
- [ ] Graphics card (`graphics-card/`)
- [ ] Sound card (`sound-card/`)
- [ ] Network card (`network-card/`)
- [ ] Power supply (to be added)

## Phase 5 — Complements
- [ ] Terminal (`terminal/`)
- [ ] Laptop / portable chassis
- [ ] Docking station

Each device follows the same cycle. Issues track the current open work.
