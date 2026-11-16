# ISM Aircraft Carrier — B2 sibling slice (#45 / with #43)

**Program ID:** ISM-CV-1 (study name TBD)

## B2 slice (this PR)
Light design note aligned with warship B2 (#43): flight-deck / aviation gear as **mass and area placeholders**. Combat systems follow the same rule — mass/footprint only.

Full carrier roadmap (#45) beyond this slice remains open (KiCad, structure, BOM, …).

## Scope limits (hard)
- No weapons interfaces, fire control, or combat-system internals
- No export-controlled data
- Aviation weapons stay inert mass boxes if listed

## Deliverables (B2)
| Path | Role |
|------|------|
| `docs/design-note.md` | Flight deck, aviation, propulsion stubs + placeholders |
| `shell/deck_study.scad` | Flight-deck proportion sketch |

See also `../warship/` for hydrostatics teaching and the shared weapons/sensor placeholder policy.
