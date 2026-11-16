# Sensors & Weapons — ISM-FJ-1 (Fictional Product Line)

Radar/EO/#76 sensors ICD, stores integration, EW stubs. **Fictional ISM systems only.** Soft sensor apps → Steve.

**Weapons boundary:** stores = inert/attach/SMS only — **no** guidance, seekers, propulsion, warheads, fuzing, arming codes.

| Doc | Content |
|-----|---------|
| `radar-eo.md` | Sensor suite, mounts, power/data, FOV (#76) |
| `sensor-integration.md` | Aperture table, FOR keep-outs, OML check (A4 #122) |
| `sensor-fov-keepouts.svg` | Nose FOV / NLG keep-out sketch |
| `stores.md` | Stations, pylons, safeing philosophy (#77) |
| `stores-safeing.md` | Force-SAFE table, SMC discretes (#77) |
| `lab-policy.md` | Simulated vs physical fit (A4 #122) |
| `stores-integration.md` | Rails/ejectors, inert models (#94) |
| `multi-origin-stores.md` | NATO/RU/CN/JP adapters (#101) |
| `ew.md` | EW / self-protect textbook stubs + SAFE/INHIBIT |

**Flight Lab YAML:** `../interfaces/sensors.yaml`, `hardpoints.yaml`, `inert-stores.yaml`, `sms-interface.yaml`, `multi-origin-stores.yaml`, `carriage-drag.yaml`, `safe-inhibit-table.yaml`, `ew-placeholders.yaml` · validator `loadout_validate.py` · EW check `../docs/ew_inhibit_examples.py`
