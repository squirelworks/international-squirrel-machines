# Agent handoff — Sarah fab-ready lane

Updated after **SATA** PR [#242](https://github.com/squirelworks/international-squirrel-machines/pull/242) (`#57`). Stopped here on usage limit — do not invent new work beyond this queue unless Sarah/Fred redirect.

## Just finished
- Peripherals + keyboard sizes: no remaining fab-readiness gaps found.
- Storage carriers through **SATA** fab-ready (flash → thumb → NVMe → IDE → SCSI → SATA).
- SCSI [#236](https://github.com/squirelworks/international-squirrel-machines/pull/236) merged as `f1896fe`.
- SATA: ERC/DRC 0, TinyUSB **0x1209 / 0x001E**, gaps [#241](https://github.com/squirelworks/international-squirrel-machines/issues/241). Issue ticks need a human (bot gets 403).

## Next (in order — one-device PRs off `main`)
1. **Squirrel-ROM** (`storage/squirrel-rom/`) · [#58](https://github.com/squirelworks/international-squirrel-machines/issues/58) — build-vs-wrap still TBD (`storage/docs/build-vs-wrap.md`); confirm with Sarah/Eric if needed, then fab-ready package (same pattern as other storage: builder ERC/DRC 0, fab/, shell, TinyUSB next PID **0x001F**, discover/roadmap, gap issue, PR).
2. **Squirrel-floppy** (`storage/squirrel-floppy/`) · [#59](https://github.com/squirelworks/international-squirrel-machines/issues/59) — same; build-vs-wrap TBD.
3. After storage range closes: **UPS** · [#29](https://github.com/squirelworks/international-squirrel-machines/issues/29) (PSU Track A already fab-ready).
4. Deferred: research briefs **C1–C6**; microwave = control/UI/enclosure only.

## Conventions that worked
- Branch: `cursor/ism-<device>-09ac` off latest `main`.
- One device per PR; tick roadmap boxes in-repo; note issue-edit 403 in PR body.
- File follow-up gap issues (non-blocking) before opening the PR.
- Watch CI via branch subscription; fix/push if red.

## Do not start until told
Next agent: pick up **#58 Squirrel-ROM** only when Sarah says continue.
