# ISM Fighter Jet (ISM-FJ-1 “Nutcracker”)

Full design program for the International Squirrel Machines single-seat fighter — not a PCB-and-shell toy. The KiCad avionics bay board and OpenSCAD airframe are one electrical/mechanical slice of a broader air-vehicle program: structure, materials, actuation, fly-by-wire, mission avionics, sensors, and stores.

Pure Squirrel-OS/2 development. Contemporary fighters and open RC/avionics projects may be studied as reference only; resulting geometry, buses, materials callouts, and control architecture are original ISM work.

## Working assumptions (revise with product decisions)
| Topic | Current default | Notes |
|-------|-----------------|-------|
| Role | Multirole day/night fighter | Air superiority primary; secondary strike |
| Crew | Single seat | Dual optional later |
| Propulsion | Twin low-bypass turbofan | Single-engine alternate documented as option |
| Control | Full fly-by-wire, no mechanical backup | Quadruplex digital; see `flight-controls/` |
| Actuation | Electro-hydrostatic (EHA) primary | Central hydraulic optional stub |
| Scale intent | Full conceptual air vehicle | Parametric shell is a reduced-scale study model |

Open product decisions are listed at the bottom of this README and in `docs/devices/fighter-jet.md`.

## Program layout

```
fighter-jet/
├── README.md                 ← you are here
├── diagrams/                 orthographics, stations, bays, harness
├── materials/                alloys, composites, fasteners, environments
├── mechanical/               airframe, gear, surfaces, access
├── hydraulics/               actuation architecture & failures
├── flight-controls/          FBW laws, redundancy, envelope
├── avionics/                 mission computer, buses, HUD/HMI, software
├── sensors-weapons/          radar/EO, stores, EW (fictional ISM)
├── kicad/                    bay controller PCB (electrical slice)
└── shell/                    parametric OpenSCAD study airframe
```

| Area | Directory | Status |
|------|-----------|--------|
| Diagrams & blueprints | `diagrams/` | Design program — SVG + station notes |
| Materials | `materials/` | Design program |
| Mechanical | `mechanical/` | Design program |
| Hydraulics / actuation | `hydraulics/` | Design program |
| Fly-by-wire | `flight-controls/` | Design program |
| Avionics (beyond bay PCB) | `avionics/` | Design program |
| Sensors & weapons | `sensors-weapons/` | Design program (fictional) |
| Bay PCB | `kicad/` | Scaffold (KiCad project present) |
| Study shell | `shell/` | Scaffold (parametric OpenSCAD) |

## Status
**Design program in progress.** Concept architecture, diagrams, and materials/mechanical/FBW/avionics narratives are in-tree. PCB routing, production STLs, and detailed FEA/CFD remain next-cycle work.

## Branding
Industrial Warp-era lines; warm grays / soft browns; single accent (TBD). ISM squirrel badge on the vertical stabilizer and avionics silkscreen. No external trademarks. See `docs/branding.md`.

## Next concrete steps
1. Lock product decisions: engine count, empty-weight class, accent color, composite vs aluminum wing box.
2. Expand `kicad/` schematic (power tree, IMU/radio footprints) and freeze bay connector pinout against `diagrams/wiring-harness.md`.
3. Export study STLs from `shell/airframe.scad`; add spar/rib station markers matching `diagrams/stations.md`.
4. Draft interface control documents (ICD) for stick/throttle → FCC → EHA.
5. Polish package (BOM, assembly, renders) and inquire before any release tag.

## Open product decisions
1. Twin vs single engine (baseline docs assume twin).
2. Empty-weight / length class for full-scale FS tables.
3. All-composite wing box vs hybrid Al-Li + CFRP skins (baseline: hybrid).
4. All-moving horizontal tail vs conventional elevator.
5. Landing-gear retract: electric vs EHA.
6. FCC quadruplex vs triplex.
7. Internal gun vs fuel/EW pallet in that bay.
8. Livery accent color (branding single-accent rule).
9. Wet vs dry wing hardpoints; max store weight.

## Related docs
- Device note: `docs/devices/fighter-jet.md`
- Principles: `docs/design-principles.md`
- Branding: `docs/branding.md`
- Roadmap: `docs/roadmap.md` (Phase 6)
