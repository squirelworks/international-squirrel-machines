# Stores Stations & Safeing — ISM-FJ-1

## Stations (fictional ISM pylons)

| Station | Location | Typical use (fictional) |
|---------|----------|-------------------------|
| STA-1/2 | Wingtip rail | Short-range IR missile (ISM-AAM-S) |
| STA-3/4 | WS-6 | Light AAM / pod |
| STA-5/6 | WS-4 | Medium AAM / fuel / strike (ISM-AAM-M / ISM-GBU-stub) |
| STA-7/8 | WS-2 | Heavy strike / fuel |
| STA-9 | Centerline | Fuel / EW pod / large store |
| Internal | Gun bay opt. | ISM gun concept or fuel/EW pallet |

Hardpoints reinforce spars per `diagrams/wing-plan.svg` and `mechanical/airframe.md`.

## Release / safeing philosophy
1. **Mechanical safe** on ground with pins; WOW inhibits release unless maintenance override.
2. **Dual consent:** MC stores logic **and** independent safe/arm discrete path.
3. **FCC veto:** envelope / AOA / gear unsafe → inhibit.
4. **Jettison:** separate guarded path for emergency store clear; still respects some structural limits.
5. **No live fuzing detail in-repo** — only interface philosophy.

## Harness
Stores serial + discretes on trunk W1 (`diagrams/wiring-harness.md`).

## Product decisions
- Internal gun vs clean bay
- Max store weight class
- Wet vs dry wing hardpoints
