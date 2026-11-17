# Polish & Inquire-for-Release — ISM-FJ-1 (#78)

## Soft lane (Steve) — do not build Soft in ISM
Soft Flight Lab (#79) and Soft HIL UI (#80) are **Steve’s lane**. Soft inquire gates stay **unticked** here until Soft accepts or Sarah waives. Do not implement Soft apps in this repo.

## Checklist
- [x] Program docs + interfaces Rev A tree in-repo (#70–#84 tracks)
- [x] ICD freeze note + `icd-freeze.yaml` pin
- [x] Master BOM stub + assembly sequence
- [x] Validation matrix with Soft blockers listed
- [ ] Soft Flight Lab MVP (#79) — **blocked on Soft (Steve)**
- [ ] Soft HIL UI (#80) — **blocked on Soft (Steve)**
- [ ] Coupon / allowables campaign replace provisional Ftu/Fty
- [x] Gerbers for bay PCB + study STL for airframe shell
- [x] Bay/study educational BOM + assembly (`docs/bom.md`, `docs/assembly.md`)
- [x] Product decisions file (`docs/decisions.md`) — **PROPOSED only**, pending user approval
- [x] Tooling fab-ready study package (`tooling/` STL/STEP/BOM/drawings/assembly) — #106 / 4b
- [ ] Renders / livery accent decision
- [ ] Inquire-for-release sign-off (Sarah / program)

## Inquire-for-release gate
Do **not** claim flight-cleared article. Release inquire is for **design package Rev A** once Soft co-check blockers are accepted or waived. Product decisions in `decisions.md` must be approved (or explicitly deferred) before freeze language is used.

## Weapons boundary
Inert stores / SAFE-INHIBIT only. No seekers, guidance, munition propulsion, warheads, fuzing, or arming.
