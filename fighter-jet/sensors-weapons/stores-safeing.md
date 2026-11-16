# Stores Safeing & SMC Interface — ISM-FJ-1 (#77)

**YAML:** `../interfaces/sms-interface.yaml` · **Stations:** `../interfaces/hardpoints.yaml`  
**Drawings:** `ISM-FJ-DWG-040` (stations) · `ISM-FJ-DWG-030` (spar pads) · `ISM-FJ-DWG-060` (WS)

## Hard stop
**Integration / ICD / lab only.** No guidance laws, seekers, propulsion/motors, warheads, fuzing, arming codes, or weapon-protocol message internals. `armed_consent` means dual-consent **release path ready** — not munition arming.

## Station map (max class)

| Station | Location | Hardware | Mass class max | Drawing |
|---------|----------|----------|----------------|---------|
| STA-1/2 | Wingtip | `rail_tip` | 150 kg | DWG-040 |
| STA-3/4 | WS~0.75 | `pylon_rail_light` | 300 kg | DWG-040/060 |
| STA-5/6 | WS~0.50 | `pylon_ejector_medium` | 700 kg | DWG-040/060 |
| STA-7/8 | WS~0.25 | `pylon_ejector_heavy` | 1200 kg | DWG-040/030 |
| STA-9 | Centerline | `pylon_ejector_heavy` | 1500 kg | DWG-040 |

Envelope / BL/WL study mm: `hardpoints.yaml`. Multi-origin adapters: #101.

## SMC / SMS interface (draft)
Block 1: SMS is an **MC logical partition** (alias SMC). Topics:

| Topic / discrete | Purpose |
|------------------|---------|
| `mc.stores_config` | Inventory / hung / selected |
| `mc.stores_mode` | `safe` · `armed_consent` · `captive_carry` · `training_sim` |
| `mc.stores_release_cmd` | Release or jettison event (no fuze fields) |
| `fcc.stores_inhibit` | Envelope / WOW / structural veto |
| `sms.safe_arm_discrete` | Independent SAFE / CONSENT |
| `sms.release_inhibit_discrete` | Hard inhibit |
| `sms.jettison_guard_discrete` | Guarded emergency clear |

## Force-SAFE table

| ID | Condition | Notes |
|----|-----------|-------|
| FS-01 | Any WOW | Unless maintenance override pin |
| FS-02 | Ground pin installed | Mechanical |
| FS-03 | FCC inhibit true | Envelope / gear / sensors |
| FS-04 | Safe/arm discrete = SAFE | Dual consent fail |
| FS-05 | Mode safe or training_sim | Lab / demo |
| FS-06 | Outside separation envelope | Per store class |
| FS-07 | FCS sensor disagree | Degraded |
| FS-08 | Hung store | Station inhibit + report |
| FS-09 | Essential bus abnormal | Power |
| FS-10 | Lab sim-only policy | Bench |

## Lab / demo policy
Authoritative narrative: `lab-policy.md`. Truth table: `../interfaces/safe-inhibit-table.yaml` (SAFE/INHIBIT only — no ARM/RELEASE rows).

| Venue | Simulated | Physically actuated |
|-------|-----------|---------------------|
| Flight Lab (#79) | Release cmd, inhibit, safe/arm state, gates, inventory | None |
| HIL (#80) | Munition internals, fuzing, seekers | Pylon discrete loopback, safe/arm switch, **resistive** ejector-squib simulator; inert fit only |
| Never in-repo demos | — | Live ordnance, real squibs, arming devices |

Documentation and bench interfaces only — no unlawful weaponization guidance.
