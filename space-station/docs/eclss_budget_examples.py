#!/usr/bin/env python3
"""#42 — teaching ECLSS / power budget check for ISM-SSN-1 study.

Crew metabolic O2 and power load averages are classroom stubs, not flight analysis.
"""
from __future__ import annotations

import sys

# Teaching: ~0.84 kg O2 / person / day (public life-support order-of-magnitude)
O2_KG_PER_PERSON_DAY = 0.84
CREW = 4

POWER_KW = {
    "eclss": 4.0,
    "avionics": 2.0,
    "comms": 1.5,
    "thermal": 3.0,
    "payload_science": 2.5,
    "margin": 2.0,
}


def o2_kg_day(crew: int) -> float:
    return crew * O2_KG_PER_PERSON_DAY


def power_total_kw(loads: dict[str, float]) -> float:
    return sum(loads.values())


def main() -> int:
    o2 = o2_kg_day(CREW)
    pwr = power_total_kw(POWER_KW)
    solar_kw_orbit_avg = 20.0  # teaching array class
    fails = 0

    if abs(o2 - 3.36) > 1e-9:
        print(f"FAIL: O2 got {o2}, expected 3.36", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: o2_kg_day={o2:.2f} (crew={CREW})")

    if abs(pwr - 15.0) > 1e-9:
        print(f"FAIL: power got {pwr}, expected 15.0", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: power_kw={pwr:.1f}")

    if pwr > solar_kw_orbit_avg:
        print("FAIL: load exceeds teaching solar orbit-average", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: {pwr:.1f} kW <= solar {solar_kw_orbit_avg:.1f} kW")

    if fails:
        return 1
    print("OK: eclss_budget_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
