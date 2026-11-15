# Fighter Jet (ISM-FJ-1 “Nutcracker”)

Official ISM air-vehicle design program. The bay KiCad board and OpenSCAD shell are **one electrical/mechanical slice**, not the whole device.

## Form factor
Single-seat, twin-engine (baseline), single-fin multirole fighter. Industrial Warp-era lines; ISM squirrel badge on the vertical stabilizer. Original geometry — not a replica of any specific aircraft.

## Program areas (in-repo)
| Area | Path |
|------|------|
| Diagrams / blueprints | `fighter-jet/diagrams/` |
| Materials | `fighter-jet/materials/` |
| Mechanical | `fighter-jet/mechanical/` |
| Hydraulics / EHA | `fighter-jet/hydraulics/` |
| Fly-by-wire | `fighter-jet/flight-controls/` |
| Avionics | `fighter-jet/avionics/` |
| Sensors & weapons (fictional) | `fighter-jet/sensors-weapons/` |
| Bay PCB | `fighter-jet/kicad/` |
| Study shell | `fighter-jet/shell/` |

## Branding
Warm grays / soft browns; single accent TBD. See `docs/branding.md`.

## Open product decisions
1. Twin vs single engine
2. Empty-weight / scale class (conceptual full-size vs study-only)
3. All-composite wing box vs hybrid Al-Li + CFRP
4. All-moving HT vs separate elevator
5. Gear retract: electric vs EHA
6. FCC quadruplex vs triplex
7. Internal gun vs clean bay / EW pallet
8. Accent color for livery and HUD chrome
