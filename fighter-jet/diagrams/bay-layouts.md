# Bay Layouts — ISM-FJ-1

## Nose sensor bay (FS-0 → FS-12)
| Zone | Content | Access |
|------|---------|--------|
| Radome volume | AESA antenna face (fictional ISM-R1) | Hinged radome |
| Lower EO | IRST / TV turret window | Ventral panel |
| Pitot / AOA | Nose boom or side probes | External |

Keep liquid cooling and waveguide stubs off the crew pressure vessel.

## Cockpit (FS-22 → FS-42)
- HUD combiner at FS-28; large-area display (LAD) below.
- Side-stick (right) and throttle quadrant (left) — HOTAS.
- Ejection seat rails (concept only; no pyrotechnic detail in-repo).
- Environmental control ducts along side walls.

## Avionics bay (FS-48 ±) — KiCad slice lives here
| Slot | LRU | Notes |
|------|-----|-------|
| A | Mission computer (MC) | Dual-lane; see `avionics/` |
| B | Flight control computer (FCC) | Quadruplex boxes preferred |
| C | Power distribution unit (PDU) | 28 V DC primary |
| D | IMU / GPS | Vibration-isolated tray |
| E | Data-link / radio | Antenna feed to fin / belly |
| F | Bay controller PCB | `kicad/ism-fighter-jet.*` — local I/O, PWM/EHA cmds, USB debug |

Mounting: four M3 bosses matching PCB outline (~120×60 mm study). Cooling: forced air from ECS branch; cold-plate stub for MC.

## Weapons / gun bay (optional, FS-68–75)
- Internal gun option: ammunition drum + blast tube exit on lower fuselage.
- Or replace with fuel / EW pallet — product decision.

## Propulsion bays (FS-82–95)
- Twin engine modules side-by-side or slightly staggered.
- Accessory gearbox, generators, EHA pumps (if central hydro retained).
- Firewalls and extinguisher bottles forward of nozzles.

## Landing gear wells
- NLG: FS-18, forward retract into fuselage.
- MLG: FS-55, outboard retract into wing/fuselage blend (TBD with planform).
