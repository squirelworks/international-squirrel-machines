# Actuation Failure Modes — ISM-FJ-1

## EHA baseline

| Failure | Detection | Response |
|---------|-----------|----------|
| Motor / pump seize | Current / speed / position lag | Declare surface failed; FCC reconfigures (e.g., flaperon assists roll) |
| Internal leak | Pressure / duty-cycle rise | Limit rate; land ASAP caution |
| Command path loss (one lane) | Cross-lane vote | Remaining FCC lanes command actuator |
| Hardover command | Dual-lane disagree + model | Bypass / damp; surface to trail or locked per surface ICD |
| Power bus loss to one EHA | PDU monitor | As seize; possibly use asymmetric thrust assist |

## Central-hydro stub (if equipped)

| Failure | Response |
|---------|----------|
| Single circuit loss | Survive on alternate circuit; reduced rate |
| Dual circuit loss | Electric backup pump or EHA-only surfaces if hybrid |
| Reservoir low | Isolate leaking side; caution |

## Flight-controls interface rules
1. No single actuator or single bus loss may make the aircraft departing within the protected envelope.
2. WOW and air-data validity gate ground vs flight gains.
3. Maintenance BIT exercises each EHA on deck with surface clearances checked.

## Still stubbed
- Quantitative hinge-moment tables
- Exact bypass orifice sizing
- Gun-drive hydro demand (if gun option selected)
