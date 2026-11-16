# International Squirrel Machines — Roadmap

Pure Squirrel-OS/2 Warp-style hardware. Scaffold → implement → polish → inquire for release.

## Phase 0 — Repository Scaffold (complete)
- [x] Repository created
- [x] Core documentation (principles, branding, devices)
- [x] Device directory stubs (including drawing pads range)
- [x] Roadmap
- [ ] Issues created for every device (in progress)

## Phase 1 — Keyboard (first production device)
**Directory:** `keyboard/` (per-size trees under `keyboard/<size>/`)
- [x] 60% fab-ready (KiCad ERC/DRC 0, fab/, shell STL/STEP, TinyUSB) — PR #128 · [#61](https://github.com/squirelworks/international-squirrel-machines/issues/61)
- [x] 65% fab-ready — PR #133 · [#62](https://github.com/squirelworks/international-squirrel-machines/issues/62)
- [x] 75% fab-ready — PR #136 · [#63](https://github.com/squirelworks/international-squirrel-machines/issues/63)  
- [x] TKL fab-ready — PR #138 · [#64](https://github.com/squirelworks/international-squirrel-machines/issues/64)
- [x] Full-size fab-ready — PR #141 · [#65](https://github.com/squirelworks/international-squirrel-machines/issues/65)
- [x] 40% fab-ready — PR #144 · [#60](https://github.com/squirelworks/international-squirrel-machines/issues/60)
- [x] Large fab-ready — PR #146 · [#66](https://github.com/squirelworks/international-squirrel-machines/issues/66)
- [x] Extra-large fab-ready — [#67](https://github.com/squirelworks/international-squirrel-machines/issues/67) (PR #150)
- [ ] Polish and inquire for release

## Phase 2 — Input Devices
- [x] Mouse (`mouse/`) — fab-ready with 60% in PR #128 · [#3](https://github.com/squirelworks/international-squirrel-machines/issues/3)
- [x] Trackball (`trackball/`) — [#8](https://github.com/squirelworks/international-squirrel-machines/issues/8) (PR #152)
- [x] Macro pad (`macro-pad/`) — [#9](https://github.com/squirelworks/international-squirrel-machines/issues/9) (PR #154)
- [x] Typewriter (`typewriter/`) — [#4](https://github.com/squirelworks/international-squirrel-machines/issues/4) (PR #159)
- [x] Drawing pads range — small / medium / large (`drawing-pads/`) — [#2](https://github.com/squirelworks/international-squirrel-machines/issues/2) (PR #162)

## Phase 3 — Output Devices
- [x] Monitor (`monitor/`) — [#10](https://github.com/squirelworks/international-squirrel-machines/issues/10) (this PR)
- [ ] Printer (`printer/`)
- [ ] Plotter (`plotter/`)
- [ ] Camera (`camera/`)

## Phase 4 — Core System
- [x] Memory / RAM modules (`memory/`) — fab-ready · [#110](https://github.com/squirelworks/international-squirrel-machines/issues/110) (PR #156)
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
- [x] [#75](https://github.com/squirelworks/international-squirrel-machines/issues/75) Avionics architecture (schematic, bus, bay, harness)
- [x] [#84](https://github.com/squirelworks/international-squirrel-machines/issues/84) Avionics firmware bring-up (ISM)

### 6.4 — Weapons & sensors
Baselines under `fighter-jet/sensors-weapons/`.
- [x] [#76](https://github.com/squirelworks/international-squirrel-machines/issues/76) Radar / EO / IR sensor suite
- [x] [#77](https://github.com/squirelworks/international-squirrel-machines/issues/77) Missiles / stores / pylons / safeing

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
- [x] [#84](https://github.com/squirelworks/international-squirrel-machines/issues/84) Avionics firmware bring-up (ISM)

### 6.6 — Integration, BOM, validation
- [ ] Freeze product decisions; Gerbers/STLs; ICD pinouts
- [x] [#78](https://github.com/squirelworks/international-squirrel-machines/issues/78) Full airframe BOM, assembly notes, ICD freeze, validation campaign, polish
- [x] [#88](https://github.com/squirelworks/international-squirrel-machines/issues/88) Soft-parseable `ism-fj-1.ismfj-params` + `bay-io.ismfj-iface` for Flight Lab (stores inert only)

### Sibling aerospace (bombers B1 / surface B2)
- [x] Bombers B1 design-note slice — [#37](https://github.com/squirelworks/international-squirrel-machines/issues/37) hypersonic educational aerothermal/TPS; [#38](https://github.com/squirelworks/international-squirrel-machines/issues/38) subsonic; [#39](https://github.com/squirelworks/international-squirrel-machines/issues/39) supersonic (weapons boundary). KiCad / structure / BOM still open.
- [x] Warship B2 design note — [#43](https://github.com/squirelworks/international-squirrel-machines/issues/43) hull/hydrostatics/stability/powering; weapons & combat sensors as mass/footprint placeholders only. Carrier light slice with [#45](https://github.com/squirelworks/international-squirrel-machines/issues/45).
- [x] Submarine B3 design note — [#44](https://github.com/squirelworks/international-squirrel-machines/issues/44) hull/trim/pressure-hull concept; sonar = mass/footprint only; no quieting/acoustics/life-support.
- [x] Rocket B4 design note — [#41](https://github.com/squirelworks/international-squirrel-machines/issues/41) hobby-class; certified motors; passive logger/recovery; no guidance or active control.
- [x] Satellite B5 design note — [#31](https://github.com/squirelworks/international-squirrel-machines/issues/31) bus + payload; weapons boundary (payload mass/power/data only).
- [x] Space station design note — [#42](https://github.com/squirelworks/international-squirrel-machines/issues/42) modules / power / ECLSS / docking / avionics; weapons boundary.
- [x] Sonar design note — [#40](https://github.com/squirelworks/international-squirrel-machines/issues/40) educational echo-sounder; transducers = mass/footprint; no quieting/classified acoustics (B3 spirit).
- [x] Gundam design note — [#46](https://github.com/squirelworks/international-squirrel-machines/issues/46) actuators / sensors / power / cockpit; weapons = stores/SAFE-INHIBIT placeholders only.
- [x] Aircraft carrier design-note deepen — [#45](https://github.com/squirelworks/international-squirrel-machines/issues/45) flight deck / aviation / propulsion; weapons & combat sensors = mass/footprint only.
- [x] Subsonic bomber design-note deepen — [#38](https://github.com/squirelworks/international-squirrel-machines/issues/38) airframe interfaces + inert bay/SAFE-INHIBIT stubs.
- [x] Supersonic bomber design-note deepen — [#39](https://github.com/squirelworks/international-squirrel-machines/issues/39) airframe / cruise thermal + inert bay/SAFE-INHIBIT stubs.
- [x] Fighter EW textbook stubs — epic [#85](https://github.com/squirelworks/international-squirrel-machines/issues/85): mass/footprint + SAFE/INHIBIT only (no waveforms / live dispense).
- [x] Hypersonic bomber aerothermal deepen — [#37](https://github.com/squirelworks/international-squirrel-machines/issues/37) interfaces + teaching heat-flux; educational only (no weapons / TPS recipes).
- [x] Warship KiCad scale-model control — [#43](https://github.com/squirelworks/international-squirrel-machines/issues/43) thruster/rudder/ballast stubs; no weapons/fire-control.
- [x] Rocket KiCad passive logger / recovery — [#41](https://github.com/squirelworks/international-squirrel-machines/issues/41); no guidance/steering/seekers.
- [x] Submarine KiCad scale-model control — [#44](https://github.com/squirelworks/international-squirrel-machines/issues/44) prop/planes/ballast stubs; no acoustics/weapons/seekers.
- [x] Satellite KiCad bus OBC/EPS/radio — [#31](https://github.com/squirelworks/international-squirrel-machines/issues/31); payload mass/power/data only.
- [x] Aircraft carrier KiCad scale-model deck control — [#45](https://github.com/squirelworks/international-squirrel-machines/issues/45) elevator/catapult/arresting/rudder stubs; no weapons/fire-control.
- [x] Space station KiCad habitat EPS/ECLSS/CDH — [#42](https://github.com/squirelworks/international-squirrel-machines/issues/42); no weapons/combat docking.
- [x] Sonar KiCad educational echo AFE/DSP — [#40](https://github.com/squirelworks/international-squirrel-machines/issues/40); no quieting/classified acoustics/weapons.
- [ ] Gundam KiCad (#46 / #169) when merged; remaining siblings / FJ gaps

### Issues
Program index: **[#85](https://github.com/squirelworks/international-squirrel-machines/issues/85)**. Children #70–#84 carry acceptance criteria. #36 is the legacy thin checklist.

Each device follows the same cycle. Issues track the current open work.
