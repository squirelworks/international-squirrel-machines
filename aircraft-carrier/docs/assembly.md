# Aircraft carrier — assembly notes (#45)

**Product:** ISM-CV-1  
**Slice:** educational build sequence for the study Gerbers + deck STL package.

## Scope limits (hard)

Same as the design note / Gerbers slice: scale-model deck control + deck packaging only. Weapons / combat sensors / aviation ordnance remain **mass / footprint** placeholders — **no** fire control, seekers, guidance, warheads, or fuzing. Catapult / arresting are load/keep-out stubs only.

## Preconditions

| Artifact | Path |
|----------|------|
| Gerber zip / CPL / fab BOM | `../fab/` |
| Deck study STL | `../mechanical/deck_study.stl` |
| Board project | `../kicad/ism-carrier-deck.*` |
| Master BOM note | `bom.md` |

## Sequence

1. **Print / obtain deck study article** from `deck_study.stl` (or regenerate via OpenSCAD from `../shell/deck_study.scad`). Confirm island + ghost structure + inert mass boxes.
2. **Fabricate or order the deck-control board** from `ism-carrier-deck-gerbers.zip` + CPL + `BOM.csv`. Study pads — not a production RP2040 pitch claim.
3. **Mount board** on tray using H1–H4 / M3 hardware. Keep J1–J4 accessible for elevator / catapult / arresting / rudder stubs.
4. **Fit inert combat / ordnance mass boxes** per `mass-placeholders.yaml` / `aviation.yaml` — mass/footprint only; do not wire fire-control channels (none exist).
5. **Harness stubs** J1 elevator, J2 catapult keep-out, J3 arresting load, J4 rudder to scale actuators or bench loads. Power from a current-limited bench supply.
6. **Deck-area demo (optional)** run `../docs/deck_area_examples.py` teaching checks — not a flight-deck certification.
7. **Visual QA** against `structural.md`; photograph board orientation and mass-box stations for the lab notebook.

## Lab policy

- Physical: fit, clearance, and inert mass placement only.
- Simulated: any combat employment, fire control, or weapons performance — **out of scope**.
- Never attach live weapons, seekers, fuzing, or classified catapult plant hardware.

## Next

Polish checklist / inquire-for-release gate (open).
