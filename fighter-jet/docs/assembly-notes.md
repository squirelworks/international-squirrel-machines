# Assembly Notes — ISM-FJ-1 Prototype Path (#78)

Buildable **study → iron-bird → article** sequence. Tooling: `../tooling/`. Shop machines: Eric.

## Sequence
1. **Datum & jigs** — Fuse splice jig (TOOL-010), wing box jig (TOOL-020), empennage jig (TOOL-030); FS/WS from `aircraft-geometry.yaml`.
2. **Primary structure** — A01→A02→A03 splices; carry-through at FS-62; wing boxes; HT/VT. Materials per `materials-zones.yaml`.
3. **Gear & hook** — NLG FS-18, MLG FS-55, arresting hook/keel; envelopes in `mechanical-airframe.yaml` / `carrier-loads.yaml`.
4. **Actuation** — Mount EHAs per `actuators.yaml`; harness A1–A4; no fluid in avionics bay.
5. **Avionics bay** — PDU → FCC×4 → MC×2 → IMU tray → bay I/O PCB (`kicad/` + `firmware/` bring-up).
6. **Sensors** — Radome/R1, EO chin, air-data probes; S1 fabric to MC (`sensors.yaml`).
7. **Stores** — Pylons/rails; SMS safeing discretes; **inert only** on lab articles (`sms-interface.yaml`).
8. **Close-out** — Bonding (G1), BIT, WOW/NWS ground checks, polish checklist.

## Break points
Field splices at FS-42 / FS-72; wing fold latch WS-4; LRU swaps without wing removal where noted in `mechanical/maintainability.md`.
