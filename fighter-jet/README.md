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
├── diagrams/                 numbered drawings DWG-010…070, stations, ICDs
├── parameters/               Soft-loadable ism-fj-1.ismfj-params (#88)
├── interfaces/               YAML + bay-io.ismfj-iface for Flight Lab (Steve)
├── materials/                alloys, composites, fasteners, environments
├── mechanical/               airframe, gear, surfaces, access
├── hydraulics/               actuation architecture & failures
├── flight-controls/          FBW laws, redundancy, envelope
├── avionics/                 mission computer, buses, HUD/HMI, software
├── sensors-weapons/          radar/EO, stores, EW (fictional ISM)
├── docs/research/            comparative survey + citations (#95)
├── docs/viability.md         viability ladder (#103)
├── docs/bom/                 master BOM stub (#78)
├── docs/assembly-notes.md    prototype build sequence (#78)
├── docs/validation*.md/yaml  co-check matrix (#78)
├── docs/icd-freeze.md        Rev A ICD pin (#78)
├── geometry/                 OpenVSP/AVL/CalculiX + Eric scale-model targets
├── tooling/                  assembly jigs, fixtures, layup tools, dies (#106)
├── firmware/                 bay I/O bring-up (host BIT/UART profile) (#84)
├── kicad/                    bay controller PCB (electrical slice)
└── shell/                    parametric OpenSCAD study airframe
```

| Area | Directory | Status |
|------|-----------|--------|
| Diagrams & blueprints | `diagrams/` | Drawing index Rev A (#70) — cite ISM-FJ-DWG-* |
| Interfaces (Flight Lab) | `interfaces/` | Stub YAML contracts Rev A |
| Tooling | `tooling/` | Study OpenSCAD jigs + tooling.yaml (#106) |
| Materials | `materials/` | Design program |
| Mechanical | `mechanical/` | Design program |
| Hydraulics / actuation | `hydraulics/` | Design program |
| Fly-by-wire | `flight-controls/` | Design program |
| Avionics (beyond bay PCB) | `avionics/` | Design program |
| Sensors & weapons | `sensors-weapons/` | Design program (fictional) |
| Bay PCB | `kicad/` | Scaffold (KiCad project present) |
| Bay firmware | `firmware/` | Host BIT/UART bring-up (#84) |
| Study shell | `shell/` | Scaffold (parametric OpenSCAD) |

## Status
**Design program in progress.** Concept architecture, diagrams, and materials/mechanical/FBW/avionics narratives are in-tree. PCB routing, production STLs, and detailed FEA/CFD remain next-cycle work.

## Branding
Industrial Warp-era lines; warm grays / soft browns; single accent (TBD). ISM squirrel badge on the vertical stabilizer and avionics silkscreen. No external trademarks. See `docs/branding.md`.

## Next concrete steps
1. Materials trade study + zone map YAML (#71 continuous track).
2. Carrier suitability load cases YAML (hook / catapult / wing fold).
3. Stores integration inert models + SMS interface YAML (no seeker/warhead/fuze).
4. Comparative fighter programme survey under `docs/research/`.
5. Lock product decisions; expand KiCad; export study STLs; freeze bay connector pinout.

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
