# Rocket — assembly notes (#41)

**Product:** ISM-RK-1  
**Slice:** educational build sequence for the study Gerbers + airframe STL package.

## Scope limits (hard)

Same as the design note / Gerbers slice: hobby airframe + passive logger/recovery only. **No** guidance, steering, active flight control, ballistic-missile, or RV content. Motors are certified commercial hobby classes only.

## Preconditions

| Artifact | Path |
|----------|------|
| Gerber zip / CPL / fab BOM | `../fab/` |
| Airframe study STL | `../mechanical/airframe_study.stl` |
| Board project | `../kicad/ism-rocket-logger.*` |
| Master BOM note | `bom.md` |

## Sequence

1. **Print / obtain airframe study article** from `airframe_study.stl` (or regenerate via OpenSCAD from `../shell/airframe_study.scad`). Confirm fins / bulkheads / motor-mount ghosts.
2. **Fabricate or order the logger board** from `ism-rocket-logger-gerbers.zip` + CPL + `BOM.csv`. Study pads — not a production RP2040 pitch claim.
3. **Mount board** in bay/tray with H1–H4 / M3 hardware. Keep J1–J4 accessible for recovery / locator / SAFE stubs.
4. **Fit recovery packaging stubs** (drogue/main) as mechanical mock-ups only for the study article; follow public hobby recovery practice when flying a real airframe.
5. **Harness** J1 drogue, J2 main, J3 buzzer, J4 SAFE LED. Never wire guidance or steering channels (none exist).
6. **Motor:** install only a **certified commercial hobby motor** from public NAR/TRA catalogs when flying — out of this fab kit.
7. **Stability demo (optional)** run `../docs/stability_examples.py` teaching checks — not a flight clearance.
8. **Visual QA** against `structural.md`; photograph board orientation for the lab notebook.

## Lab policy

- Physical: fit, clearance, passive logger, and recovery packaging only.
- Simulated: any guidance, steering, or weapons performance — **out of scope**.
- Never fabricate propellant or guidance hardware in-repo.

## Next

Polish checklist / inquire-for-release gate (open).
