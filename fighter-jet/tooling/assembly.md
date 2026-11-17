# Tooling — assembly / use notes (ISM-FJ-1 / #106 / 4b)

Educational build and use sequence for the study tooling package. Complements airframe `../docs/assembly-notes.md` (#78).

## Scope

- Physical: print/fit study jigs, fixtures, layup mandrels, dies
- Soft #79/#80: **Steve’s lane** — do not build Soft here
- Decisions: remain **PROPOSED** in `../docs/decisions.md`
- Eric: CNC / printer / oven are **equipment references only**

## Preconditions

| Artifact | Path |
|----------|------|
| Master index | `tooling.yaml` |
| BOM | `bom.md`, `BOM.csv` |
| Exports | `./export.sh` → `.stl` / `.step` beside each `.scad` |

## Sequence

1. **Regenerate exports** with `./export.sh` if `.scad` changed.
2. **Print / machine study articles** from STL (or shop equivalent). Confirm scale is study-mm, not full-size.
3. **TOOL-010** — seat A01/A02/A03 splice demos at FS-42 / FS-72 rings; use ⌀6 pins in base.
4. **TOOL-020** — load RH wing-box spar/rib demo; spar cradles at 15% / 65% chord.
5. **TOOL-030** — set VT posts and HT cradles; all-moving HT is PROPOSED only.
6. **TOOL-040** — clamp skin/longeron stack; bushings at 20 mm study pitch.
7. **TOOL-050 / 070 / 080** — layup demos on male tools; cure only in Eric’s oven (reference). Canopy/intake mandrels are educational packaging forms — **no** transparency or LO recipes.
8. **TOOL-060** — male/female skin form pair dry-fit (no live press recipe).
9. **QA** — photograph tool ID labels; log against `drawings.md`.

## Lab policy

- No seekers, guidance, munition, warhead, or fuzing tooling.
- No designing Eric’s shop machines in this tree.
- Soft inquire gates stay unticked until Steve accepts or Sarah waives.

## Next

4c: Soft-parseable params (#88) + firmware CI (#130) after this PR merges. Product decisions stay PROPOSED until approved.
