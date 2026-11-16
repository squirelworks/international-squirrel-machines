#!/usr/bin/env python3
"""B5 #31 — orbit-average power budget teaching check.

Sum of subsystem averages must be <= solar_orbit_avg_w (with margin).
Not a flight power analysis.
"""
from __future__ import annotations

import sys

LOADS_W = {
    "obc": 0.8,
    "comms": 1.2,
    "adcs": 0.5,
    "payload": 1.0,
    "margin_charge": 1.5,
}


def total_load(loads: dict[str, float]) -> float:
    return sum(loads.values())


def main() -> int:
    total = total_load(LOADS_W)
    solar_orbit_avg = 6.0  # teaching BOL orbit-average class
    fails = 0
    if abs(total - 5.0) > 1e-9:
        print(f"FAIL: total got {total}, expected 5.0", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: load_total_w={total:.1f}")

    if total > solar_orbit_avg:
        print("FAIL: load exceeds teaching solar orbit-average", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: {total:.1f} W <= solar {solar_orbit_avg:.1f} W")

    margin = solar_orbit_avg - total
    if margin < 0.5:
        print("FAIL: teaching margin < 0.5 W", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: margin_w={margin:.1f}")

    if fails:
        return 1
    print("OK: power_budget_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
