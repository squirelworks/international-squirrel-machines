# Subsonic bomber — assembly notes (#38)

**Product:** ISM-SB-1  
**Slice:** educational build sequence for the study Gerbers + airframe STL package.

## Weapons boundary (hard)

Same as the design note / Gerbers slice: inert bay mass/CG/volume + SAFE/INHIBIT only. **No** seekers, guidance, munition propulsion, warheads, fuzing, arming, or employment content.

## Preconditions

| Artifact | Path |
|----------|------|
| Gerber zip / CPL / fab BOM | `../fab/` |
| Airframe study STL | `../mechanical/airframe_study.stl` |
| Board project | `../kicad/ism-sb-bay.*` |
| Master BOM note | `bom.md` |

## Sequence

1. **Print / obtain airframe study article** from `airframe_study.stl` (or regenerate via OpenSCAD from `../shell/airframe_study.scad`). Confirm bay keep-out volume is an inert cutout only.
2. **Fabricate or order the bay board** from `ism-sb-bay-gerbers.zip` + CPL + `BOM.csv`. Study pads — not a production RP2040 pitch claim.
3. **Mount board** on bay tray with H1–H4 / M3 hardware. Keep J1–J4 accessible for door / SAFE / INHIBIT stubs.
4. **Fit inert payload mass block** per `../interfaces/payload-placeholders.yaml` — mass/CG/volume only; do not install live stores.
5. **Harness stubs** J1 door actuator (bench load OK), J2 SAFE, J3 INHIBIT. Never wire arm/release channels (none exist). Power from a current-limited bench supply.
6. **Cruise / payload demo (optional)** run `../docs/cruise_examples.py` teaching checks — not a flight clearance.
7. **Visual QA** against `structural.md`; photograph board orientation and inert bay block for the lab notebook.

## Lab policy

- Physical: fit, clearance, and inert mass placement only.
- Simulated: any release, employment, or weapons performance — **out of scope**.
- SAFE/INHIBIT discretes are bench logic only — no executable arm/release sequences.

## Next (not this PR)

Polish checklist / inquire-for-release gate; remaining sibling BOM slices.
