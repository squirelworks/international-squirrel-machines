# Lab / Demo Policy — Sensors & Stores (A4 #122 / #76 / #77)

**Machine-readable twin:** `../interfaces/safe-inhibit-table.yaml` · `../interfaces/sms-interface.yaml` (`lab_demo_policy`)

## Hard stop
**Integration and ICD only.** No guidance, seekers, munition propulsion, warheads, fuzing, or arming codes. No executable arm/release sequences timed for live release. Nothing actuated physically on benches beyond **inert fit and clearance** checks.

## What is simulated vs physically fitted

| Venue | Simulated | Physically moved / fitted |
|-------|-----------|---------------------------|
| Flight Lab (#79 / SS#173) | Sensor stub messages; SMS inventory/mode/inhibit; carriage drag / CG; loadout legality | None (software only) |
| HIL (#80) | Munition internals, fuzing, seekers, release timing | Pylon discrete loopback; safe/arm switch; **resistive** ejector-squib simulator; inert shape fit on fixture |
| Shop / CAD benches | — | Inert 3D-printed / foam store shapes for clearance and lug spacing fit only |
| Never in-repo | — | Live ordnance, real squibs, arming devices, seeker hardware |

## Proposal (accepted for Rev A)
Only **fit and clearance** checks with inert shapes are physical. All SAFE/INHIBIT logic, BIT, and track stubs stay simulated.

## Force-SAFE / inhibit
Every lab session starts in SAFE. Force-SAFE conditions FS-01…FS-10 and the truth table in `safe-inhibit-table.yaml` apply. Outputs are **SAFE** or **INHIBIT** only — never ARM or RELEASE commands from the table.
