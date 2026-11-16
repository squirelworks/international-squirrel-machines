# Actuation Failure Modes — ISM-FJ-1 (#73)

Per-channel safe-failure modes are authoritative in `../interfaces/actuators.yaml` (`safe_failure`).

## EHA baseline (flight controls)

| Failure | Detection | Response |
|---------|-----------|----------|
| Motor / pump seize | Current / speed / position lag | Declare surface failed; FCC reconfigures (e.g. flaperon assists roll) |
| Internal leak | Pressure / duty-cycle rise | Limit rate; land-ASAP caution |
| Command path loss (one lane) | Cross-lane vote | Surviving FCC lanes command actuator |
| Hardover command | Dual-lane disagree + model | Bypass / damp; trail or **hold** (HT) per ICD |
| Power bus loss to one EHA | PDU monitor | As seize; asymmetric thrust assist if needed |

## Gear / utilities

| Failure | Response |
|---------|----------|
| Gear actuator power loss | Free-fall unlock + gravity/spring; down-lock discrete required |
| NWS loss | Damp to center or caster; WOW-gated |
| Wing-fold power loss | Hold locks engaged; do not unlock under load |

## Central-hydro stub (if equipped)

| Failure | Response |
|---------|----------|
| Single circuit loss | Alternate circuit; reduced rate |
| Dual circuit loss | EMDP or EHA-only surfaces if hybrid |
| Reservoir low | Isolate leaking side; caution |

## Flight-controls interface rules
1. No single actuator or single bus loss may make the aircraft departing within the protected envelope.
2. WOW and air-data validity gate ground vs flight gains.
3. Maintenance BIT exercises each EHA on deck with surface clearances checked.

## Still stubbed
- Quantitative hinge-moment tables
- Exact bypass orifice sizing
- Gun-drive hydro demand (if gun option selected)
