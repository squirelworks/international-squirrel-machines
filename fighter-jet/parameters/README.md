# ISM-FJ parameters — Soft Flight Lab (#88)

**Canonical Soft-loadable file:** `ism-fj-1.ismfj-params`

| Consumer | Path |
|----------|------|
| SquirrelSoft Flight Lab (#79 / SS#168) | `fighter-jet/parameters/ism-fj-1.ismfj-params` |
| Bay I/O interface map | `fighter-jet/interfaces/bay-io.ismfj-iface` |

Format: Soft plain-text (`ISM-FJ parameters 1` header). Geometry/mass numbers mirror `shell/airframe.scad` and YAML companions under `interfaces/`. Prefer this file over Soft fixture snapshots when present.

**Stores boundary:** hardpoint keys are inert mass/geometry placeholders only — no seekers, guidance, warheads, fuzing, or live launch.
