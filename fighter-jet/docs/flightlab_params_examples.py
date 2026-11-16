#!/usr/bin/env python3
"""#88 — Soft-parseable ISM-FJ params / bay-io sanity check.

Verifies Soft headers and key geometry / channel lines Soft Flight Lab expects.
Stores keys remain inert-integration placeholders only.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARAMS = ROOT / "parameters" / "ism-fj-1.ismfj-params"
IFACE = ROOT / "interfaces" / "bay-io.ismfj-iface"


def load_kv(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        # Soft channel lines: "channel act_aileron: header J1 trunk A1"
        key, _, val = line.partition(":")
        out[key.strip()] = val.strip()
    return out


def main() -> int:
    fails = 0
    ptxt = PARAMS.read_text()
    itxt = IFACE.read_text()

    if not ptxt.startswith("ISM-FJ parameters 1"):
        print("FAIL: params missing Soft header", file=sys.stderr)
        fails += 1
    else:
        print("OK: params Soft header")

    if not itxt.startswith("ISM-FJ interface 1"):
        print("FAIL: iface missing Soft header", file=sys.stderr)
        fails += 1
    else:
        print("OK: iface Soft header")

    pk = load_kv(PARAMS)
    for key, want in (
        ("vehicle_id", "ISM-FJ-1"),
        ("fuselage_length_mm", "420"),
        ("wing_span_mm", "280"),
        ("stores_scope", "inert_mass_geometry_drag_only"),
    ):
        got = pk.get(key)
        if got != want:
            print(f"FAIL: params {key}={got!r} want {want!r}", file=sys.stderr)
            fails += 1
        else:
            print(f"OK: {key}={got}")

    ik = load_kv(IFACE)
    for key, want_sub in (
        ("channel act_aileron", "header J1 trunk A1"),
        ("channel act_elevator", "header J2 trunk A2"),
        ("channel act_rudder", "header J3 trunk A3"),
        ("channel act_throttle", "header J4 trunk A4"),
        ("stores_policy", "inert_integration_only"),
    ):
        got = ik.get(key, "")
        if want_sub not in got and got != want_sub:
            print(f"FAIL: iface {key}={got!r}", file=sys.stderr)
            fails += 1
        else:
            print(f"OK: {key}")

    if fails:
        return 1
    print("OK: flightlab_params_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
