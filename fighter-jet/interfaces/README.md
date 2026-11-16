# ISM-FJ-1 Machine-Readable Interfaces

Source of truth for **SquirrelSoft Flight Lab** (Steve) and other consumers. Human narratives remain under sibling dirs; these files are the loadable contracts.

| File | Contents | Status |
|------|----------|--------|
| `schema-manifest.yaml` | Index of interface files, versions, drawing cross-refs | Rev A |
| `aircraft-geometry.yaml` | Datum, study scale, major dimensions, stations | Stub with numbers |
| `mass-properties.yaml` | Mass, CG, inertia tensor placeholders | Stub schema + provisional numbers |
| `flight-controls.yaml` | Inceptors ICD, modes, surface cmds ↔ EHA, envelope | Stub (#74) |
| `sensors.yaml` | Suite mounts, apertures[], power/data ICD, FOV stubs | Stub (#76 / A4 #122) |
| `hardpoints.yaml` | Stations, max_store_class, lug_class, clearance | Stub (#77 / A4 #122) |
| `actuators.yaml` | EHA/gear channels, I/F table, safe failure | Stub (#73) |
| `hydraulics.yaml` | Routing keep-outs / EHA pack envelopes | Stub (#73) |
| `avionics-bus.yaml` | Bus topology, topics, power | Stub (#75) |
| `avionics-architecture.yaml` | LRU split, connectors, schematic coverage | Stub (#75) |
| `firmware-bringup.yaml` | Bay I/O FW hooks, BIT UART profile, safe-state | Stub (#84) |
| `bit-frame.yaml` | BIT fields, rates, UART/bus encoding | Stub (A1 #119) |
| `safe-state.yaml` | Trigger → channel → output → test ID | Stub (A1 #119) |
| `bay-io.ismfj-iface` | Soft-parseable bay I/O channel map (`ISM-FJ interface 1`) (#88) | Stub Rev A |
| `icd-freeze.yaml` | Rev A pinned ICD list for co-check | Stub (#78) |
| `materials-zones.yaml` | Airframe zone → material map + joints | Stub (#92) |
| `carrier-loads.yaml` | Arrestment / catapult / sink-rate / wing-fold cases | Stub (#93) |
| `inert-stores.yaml` | Inert store mass/dims/drag/CG (public class figures) | Stub (#94) |
| `sms-interface.yaml` | SMC/SMS topics, force-SAFE, lab policy, envelopes | Stub (#77) |
| `manufacturing.yaml` | Zone process/spec/NDT/supply (research) | Stub (#100) |
| `multi-origin-stores.yaml` | Family×station×adapter + inert catalogue | Stub (#101) |
| `viability-criteria.yaml` | Sanity gates + class bands (canonical) | Stub (#103) |
| `materials-allowables.yaml` | Spec callouts, allowables, stack-ups, joints | Stub (#71) |
| `mechanical-airframe.yaml` | Load paths, gear envelopes, hinge/actuator geom | Stub (#72) |
| `propulsion.yaml` | Engine envelope, inlet/duct, mounts, offtakes | Stub (A2 #120) |
| `carriage-drag.yaml` | ΔCD0 per store/loadout + illegal fixture | Stub (A4 #122) |
| `safe-inhibit-table.yaml` | Condition → SAFE/INHIBIT truth table | Stub (A4 #122) |
| `loadout_validate.py` | SS#173 loadout legality check | Stub (A4 #122) |

## Rules
1. Units are SI unless a field ends in `_mm` / `_deg` / `_pct` (study-model companions).
2. `status: stub` means Flight Lab may load it; numbers marked `provisional: true` will change when product decisions freeze.
3. Drawing IDs (`ISM-FJ-DWG-…`) in `source_drawings` must match `diagrams/` index.
4. Do not fork these into SquirrelSoft — import from this tree.

## Consumer map
| Consumer | Primary files |
|----------|---------------|
| Flight Lab (#79 / SS#168) | geometry, mass, flight-controls, hardpoints, sensors, inert-stores, sms, carrier-loads, materials-zones |
| HIL bench (#80) | actuators, avionics-bus, sensors |
| Mission-computer stubs (#81) | avionics-bus, sensors, hardpoints |
| HUD/HMI (#82) | flight-controls (modes), sensors |
| Data-bus analyzer (#83) | avionics-bus |
