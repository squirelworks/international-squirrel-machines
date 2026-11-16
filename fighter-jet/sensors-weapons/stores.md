# Stores Stations & Safeing — ISM-FJ-1 (#77)

**Safeing / SMC detail:** `stores-safeing.md` · **YAML:** `../interfaces/sms-interface.yaml` · `hardpoints.yaml`

## Hard stop
No guidance, seekers, propulsion, warheads, fuzing, or arming codes in-repo. Integration + ICD + lab policy only.

## Stations (fictional ISM pylons)

| Station | Location | Typical inert / store class | Mass max |
|---------|----------|----------------------------|----------|
| STA-1/2 | Wingtip rail | Short-range AAM-class inert | 150 kg |
| STA-3/4 | WS~0.75 | Light AAM / pod | 300 kg |
| STA-5/6 | WS~0.50 | Medium AAM / fuel / strike-class inert | 700 kg |
| STA-7/8 | WS~0.25 | Heavy / fuel | 1200 kg |
| STA-9 | Centerline | Fuel / EW / large | 1500 kg |
| Internal | Gun bay opt. | Product decision vs fuel/EW | — |

Hardpoints → spars: `ISM-FJ-DWG-040` / `030` / `060`. Geometry & BL/WL: `hardpoints.yaml`.

## Prior tracks
- **#94** inert models + SMS stub — `stores-integration.md`, `inert-stores.yaml`
- **#101** multi-origin adapters — integration only
- **#77** (this) safeing table, SMC discretes, lab/demo policy

## Release / safeing philosophy
1. **Mechanical safe** on ground with pins; WOW inhibits release unless maintenance override.
2. **Dual consent:** MC stores logic **and** independent safe/arm discrete (`CONSENT` ≠ munition arm).
3. **FCC veto:** envelope / AOA / gear unsafe → inhibit.
4. **Jettison:** separate guarded path; structural limits still apply.
5. **Force-SAFE** whenever FS-01…FS-10 conditions hold (`stores-safeing.md`).

## Harness
Stores serial + discretes on trunk W1 (`diagrams/wiring-harness.md`).

## A4 integration (#122)
Per-station `max_store_class` / `lug_class` / `clearance_envelope` in `hardpoints.yaml` (MIL-STD-8591 / MIL-HDBK-1763 cites). Carriage ΔCD0: `carriage-drag.yaml`. SAFE/INHIBIT truth table: `safe-inhibit-table.yaml`. Lab policy: `lab-policy.md`. Adjacent-store OpenSCAD: `shell/check_stores_clearance.sh`.

## Product decisions (open)
- Internal gun vs clean bay
- Wet vs dry wing hardpoints (baseline **dry**)
