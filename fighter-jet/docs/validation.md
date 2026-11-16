# Validation Campaign — ISM-FJ-1 (#78)

**Matrix:** `validation-matrix.yaml`  
Flow: **ground/bench → HIL → Flight Lab** (Soft). Analysis-only rows use in-repo gates (#103).

## Ready on ISM now
Geometry/shell vs FS-WS, mass/viability sanity, materials zone↔allowables, gear envelopes, **firmware `make test`** / BIT UART safe-state.

## Blocked on Soft (Steve)
Carrier load import, FBW mode scripts, EHA HIL, bus analyzer, sensor stubs, SMS inhibit, inert mass/drag co-check — issues **#79 / #80 / #83**.

## Weapons boundary
Validation uses **inert** stores and SMS discretes only. No guidance, seekers, propulsion, warheads, fuzing, or arming-code tests in-repo.
