# International Squirrel Machines (ISM)

Pure Squirrel-OS/2 Warp-style hardware development.

**International Squirrel Machines** is the hardware companion line to Squirrel-OS/2. All devices are designed and developed independently (contemporary sources studied only as reference). Designs live here as KiCad projects and parametric 3D-printable shells.

## Device Line

| Device | Status | Directory |
|--------|--------|-----------|
| Keyboard | Scaffolded | `keyboard/` |
| Mouse | Planned | `mouse/` |
| Monitor | Planned | `monitor/` |
| Computer Case | Planned | `case/` |
| Motherboard | Planned | `motherboard/` |
| CPU | Planned | `cpu/` |
| Graphics Card | Planned | `graphics-card/` |
| Typewriter | Planned | `typewriter/` |
| Printer | Planned | `printer/` |
| Plotter | Planned | `plotter/` |
| Camera | Planned | `camera/` |
| Trackball | Planned | `trackball/` |
| Sound Card | Planned | `sound-card/` |
| Network Card | Planned | `network-card/` |
| Terminal | Planned | `terminal/` |
| Macro Pad | Planned | `macro-pad/` |

## Repository Layout

```
international-squirrel-machines/
├── README.md
├── docs/
│   ├── roadmap.md
│   ├── design-principles.md
│   ├── branding.md
│   └── devices/
├── common/
│   ├── footprints/
│   ├── libraries/
│   └── branding/
├── keyboard/
│   ├── README.md
│   ├── kicad/
│   └── shell/
└── [device]/
```

## Getting Started

1. Clone this repository.
2. Open device directories for KiCad projects or OpenSCAD shells.
3. See `docs/roadmap.md` for the current development sequence.
4. Issues track every device scaffold and implementation milestone.

## Philosophy

- Pure Squirrel-OS/2 development.
- When in doubt, scaffold.
- If scaffolded, implement.
- If implemented, polish.
- If polished, inquire for the next release.

Part of the Squirrelworks family alongside [squirrelbios](https://github.com/squirelworks/squirrelbios).
