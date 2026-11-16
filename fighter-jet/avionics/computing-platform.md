# Computing Platform Split — ISM-FJ-1 (planning)

Planning note for where flight software and ground/lab tools run. Complements `software-partitioning.md`. Not a Soft-app implementation ticket (Steve owns Flight Lab / HIL UI).

## 1) Flight-critical (FBW & avionics partitions)
- **Runtime:** small RTOS with **DO-178C** and **ARINC 653**-style time/space partitioning as **reference** practice (ISM-original partitions — not a certified stack claim).
- **Boot:** **SquirrelBIOS** reused for board bring-up, BIST, and boot integrity on FCC / bay I/O / related LRUs.
- **Drivers:** may be borrowed across boards where interfaces match (`firmware/` bay bring-up, future FCC ports).
- **Owns:** FCC laws, monitors/vote, essential HUD symbols, safeing discretes path with MC — see partitions table in `software-partitioning.md`.
- **Does not own:** Soft desktop apps or unclassified “mission laptop” UX.

## 2) Ground / lab (Squirrel OS/2)
Host platform for non-flight-critical tools:

| Use | Notes |
|-----|-------|
| Flight Lab | Aero + FCS co-check (#79 / Soft) |
| Mission planning | Ground only |
| Flight-data download | Post-flight / iron-bird |
| Maintenance laptop | BIT, data load interlocks |
| HIL bench | Host side of #80 |

**Tracker:** [squirrel-os2#225](https://github.com/squirelworks/squirrel-os2/issues/225)

ISM still publishes machine-readable ICDs under `../interfaces/` — Soft imports; does not fork.

## 3) First SquirrelBIOS trial
**Eric’s RC flight controller** is the first place to trial SquirrelBIOS bring-up (consumer/RC lane). Lessons (boot, BIST, driver patterns) feed ISM fighter bay I/O / FCC bring-up (`../firmware/`, #84) without pulling RC product code into `fighter-jet/`.

## Weapons boundary
Stores/SMS remain **integration-level** only: no guidance, seekers, propulsion, warheads, fuzing, or arming-code internals in this tree.
