# Fighter Jet (ISM-FJ-1 “Nutcracker”)

Official ISM air-vehicle design program. The bay KiCad board and OpenSCAD shell are **one electrical/mechanical slice**, not the whole device.

## Form factor
Single-seat, twin-engine (baseline), single-fin multirole fighter. Industrial Warp-era lines; ISM squirrel badge on the vertical stabilizer. Original geometry — not a replica of any specific aircraft.

## Program areas (in-repo)
| Area | Path |
|------|------|
| Diagrams / blueprints | `fighter-jet/diagrams/` (cite `ISM-FJ-DWG-*`) |
| Flight Lab parameters | `fighter-jet/parameters/ism-fj-1.ismfj-params` (#88) |
| Flight Lab interfaces | `fighter-jet/interfaces/` (YAML + `bay-io.ismfj-iface`) |
| Materials | `fighter-jet/materials/` |
| Mechanical | `fighter-jet/mechanical/` |
| Hydraulics / EHA | `fighter-jet/hydraulics/` |
| Fly-by-wire | `fighter-jet/flight-controls/` |
| Avionics | `fighter-jet/avionics/` |
| Sensors & weapons (fictional) | `fighter-jet/sensors-weapons/` |
| Research notes | `fighter-jet/docs/research/` (comparative survey #95) |
| Viability / geometry | `fighter-jet/docs/viability.md`, `fighter-jet/geometry/` |
| Tooling | `fighter-jet/tooling/` (#106) — fab-ready study STL/STEP/BOM |
| Firmware (bay I/O) | `fighter-jet/firmware/` (#84) |
| BOM / assembly / validation | `fighter-jet/docs/bom/`, `assembly-notes.md`, `validation.md` (#78) |
| Bay/study educational BOM | `fighter-jet/docs/bom.md`, `assembly.md` (#85 Gerbers follow-on) |
| Product decisions (PROPOSED) | `fighter-jet/docs/decisions.md` |
| Bay PCB | `fighter-jet/kicad/` |
| Bay fab (study Gerbers) | `fighter-jet/fab/` |
| Study shell + STL | `fighter-jet/shell/` |

## ICD freeze (Rev A)
Pinned interface list: [`fighter-jet/interfaces/icd-freeze.yaml`](../../fighter-jet/interfaces/icd-freeze.md) · manifest [`schema-manifest.yaml`](../../fighter-jet/interfaces/schema-manifest.yaml). Key renames require Rev B.

## Branding
Warm grays / soft browns; single accent TBD. See `docs/branding.md`.

## Open product decisions

**PROPOSED baselines (not frozen):** [`fighter-jet/docs/decisions.md`](../../fighter-jet/docs/decisions.md). Soft #79/#80 = Steve’s lane (inquire gates stay unticked).

1. Twin vs single engine
2. Empty-weight / scale class (conceptual full-size vs study-only)
3. All-composite wing box vs hybrid Al-Li + CFRP
4. All-moving HT vs separate elevator
5. Gear retract: electric vs EHA
6. FCC quadruplex vs triplex
7. Internal gun vs clean bay / EW pallet
8. Accent color for livery and HUD chrome

## Weapons boundary
Stores / weapons in-program = **mass / footprint / SAFE / INHIBIT** placeholders only. Bay board has no stores fire channels. **No** seekers, guidance, munition propulsion, warheads, fuzing, or arming.
