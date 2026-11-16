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

## Phase 6 — Aerospace / Fighter Jet program

Scaffold (PR #68) and the design-program documentation baseline (PR #86: diagrams, materials, mechanical, hydraulics, FBW, avionics, sensors/weapons) are in-tree. That is still **not** a finished product — remaining work is freeze decisions, Gerbers/STLs, ICD pinouts, software/Flight Lab, and validation, tracked by the issue set below.

**Directory:** `fighter-jet/`  
**Device note:** `docs/devices/fighter-jet.md`  
**Program epic:** [#85](https://github.com/squirelworks/international-squirrel-machines/issues/85)  
**Original thin roadmap:** [#36](https://github.com/squirelworks/international-squirrel-machines/issues/36) — superseded by #85 (close #36 as duplicate when able).

### 6.0 — Scaffold & design-program docs (complete)
- [x] Device directory + README
- [x] Avionics KiCad project stub (`fighter-jet/kicad/`)
- [x] Parametric OpenSCAD airframe stub (`fighter-jet/shell/`)
- [x] Device design note stub
- [x] Fighter jet design program — diagrams, materials, mechanical, hydraulics, FBW, avionics, sensors/weapons (PR #86)

### 6.1 — Structure (diagrams → materials → airframe)
Design-doc baselines live under `fighter-jet/diagrams/`, `materials/`, `mechanical/`. Issues track remaining productization against those docs.
- [x] [#70](https://github.com/squirelworks/international-squirrel-machines/issues/70) Diagrams & blueprints (3-views, sections, ICDs) — drawing index + DWG-010…070, interfaces stubs
- [x] [#71](https://github.com/squirelworks/international-squirrel-machines/issues/71) Materials: metallurgy + composites stack-up and allowables (trade baseline in #92)
- [x] [#72](https://github.com/squirelworks/international-squirrel-machines/issues/72) Mechanical airframe, landing gear & control surfaces

### 6.1b — Continuous research tracks (military program)
Ship YAML/JSON under `fighter-jet/` for Flight Lab; one PR per coherent chunk.
- [x] [#92](https://github.com/squirelworks/international-squirrel-machines/issues/92) Materials trade study (Ti / Al / steel / composites → zone map table)
- [x] [#93](https://github.com/squirelworks/international-squirrel-machines/issues/93) Carrier suitability (hook, catapult/arrestment loads, wing fold, corrosion) + load-case YAML
- [x] [#94](https://github.com/squirelworks/international-squirrel-machines/issues/94) Stores integration level (hardpoints, inert store models, SMS I/F) — no seeker/warhead/fuze detail
- [x] [#95](https://github.com/squirelworks/international-squirrel-machines/issues/95) Comparative fighter programme survey → `fighter-jet/docs/research/`
- [x] [#100](https://github.com/squirelworks/international-squirrel-machines/issues/100) Manufacturing & supply-chain research (no tooling designs)
- [x] [#101](https://github.com/squirelworks/international-squirrel-machines/issues/101) Multi-origin stores compatibility (NATO/RU/CN/JP adapters — integration only)
- [x] [#103](https://github.com/squirelworks/international-squirrel-machines/issues/103) Viability criteria & independent analysis (after #101; before tooling)
- [x] [#106](https://github.com/squirelworks/international-squirrel-machines/issues/106) Tooling (jigs/fixtures/dies under `fighter-jet/tooling/`)

### 6.2 — Systems (hydraulics / actuation / flight controls)
Baselines under `fighter-jet/hydraulics/`, `flight-controls/`.
- [x] [#73](https://github.com/squirelworks/international-squirrel-machines/issues/73) Hydraulics / actuation architecture
- [x] [#74](https://github.com/squirelworks/international-squirrel-machines/issues/74) Fly-by-wire & flight controls (inceptors → computer → surfaces)

### 6.3 — Avionics (beyond the bay PCB scaffold)
Baselines under `fighter-jet/avionics/` (+ KiCad bay PCB).
- [ ] [#75](https://github.com/squirelworks/international-squirrel-machines/issues/75) Avionics architecture (schematic, bus, bay, harness)
- [ ] [#84](https://github.com/squirelworks/international-squirrel-machines/issues/84) Avionics firmware bring-up (ISM)

### 6.4 — Weapons & sensors
Baselines under `fighter-jet/sensors-weapons/`.
- [ ] [#76](https://github.com/squirelworks/international-squirrel-machines/issues/76) Radar / EO / IR sensor suite
- [ ] [#77](https://github.com/squirelworks/international-squirrel-machines/issues/77) Missiles / stores / pylons / safeing

### 6.5 — Software & SquirrelSoft applications
Build our own software. Third-party sims are **not** source of truth.

| App | Issue | Repo boundary |
| --- | --- | --- |
| **Fighter Jet Flight Lab** | ISM [#79](https://github.com/squirelworks/international-squirrel-machines/issues/79) · SquirrelSoft [#168](https://github.com/squirelworks/squirrelsoft/issues/168) | **SquirrelSoft** (`squirelworks/squirrelsoft`); ISM owns airframe parameters / ICD |
| HIL bench UI | [#80](https://github.com/squirelworks/international-squirrel-machines/issues/80) | SquirrelSoft UI + ISM fixtures/harness |
| Mission-computer stubs | [#81](https://github.com/squirelworks/international-squirrel-machines/issues/81) | SquirrelSoft; interface contracts in ISM |
| HUD / HMI tooling | [#82](https://github.com/squirelworks/international-squirrel-machines/issues/82) | SquirrelSoft; display requirements in ISM |
| Data-bus analyzer | [#83](https://github.com/squirelworks/international-squirrel-machines/issues/83) | SquirrelSoft app + ISM bus docs/fixtures |
| Firmware / board bring-up | [#84](https://github.com/squirelworks/international-squirrel-machines/issues/84) | **ISM** (`fighter-jet/`) |

- [ ] [#79](https://github.com/squirelworks/international-squirrel-machines/issues/79) Flight Lab MVP (aero + FCS co-check)
- [ ] [#80](https://github.com/squirelworks/international-squirrel-machines/issues/80) HIL bench UI + ISM fixtures
- [ ] [#81](https://github.com/squirelworks/international-squirrel-machines/issues/81) Mission-computer stubs
- [ ] [#82](https://github.com/squirelworks/international-squirrel-machines/issues/82) HUD / HMI tooling
- [ ] [#83](https://github.com/squirelworks/international-squirrel-machines/issues/83) Data-bus analyzer
- [ ] [#84](https://github.com/squirelworks/international-squirrel-machines/issues/84) Avionics firmware bring-up (ISM)

### 6.6 — Integration, BOM, validation
- [ ] Freeze product decisions; Gerbers/STLs; ICD pinouts
- [ ] [#78](https://github.com/squirelworks/international-squirrel-machines/issues/78) Full airframe BOM, assembly notes, ICD freeze, validation campaign, polish

### Sibling aerospace stubs (still Planned)
- [ ] Bombers / rocket / satellite / carrier siblings (directory stubs only)

### Issues
Program index: **[#85](https://github.com/squirelworks/international-squirrel-machines/issues/85)**. Children #70–#84 carry acceptance criteria. #36 is the legacy thin checklist.

Each device follows the same cycle. Issues track the current open work.
