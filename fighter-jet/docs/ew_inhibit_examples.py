#!/usr/bin/env python3
"""ISM-FJ EW SAFE/INHIBIT teaching check (textbook / lab only).

No waveforms, live dispense, or classified RF. Outputs are SAFE/INHIBIT only.
"""
from __future__ import annotations

import sys

# condition -> (SAFE, INHIBIT)
TABLE = {
    "ground_maintenance": (True, True),
    "weight_on_wheels": (True, True),
    "range_unsafe_sim": (True, True),
    "airborne_sim_consent": (False, False),
}


def inhibit_dispense(condition: str) -> bool:
    return TABLE[condition][1]


def main() -> int:
    fails = 0
    for cond, (safe, inhib) in TABLE.items():
        if inhib != inhibit_dispense(cond):
            print(f"FAIL: {cond}", file=sys.stderr)
            fails += 1
        else:
            print(f"OK: {cond} SAFE={safe} INHIBIT={inhib}")

    # Ground / WOW must never allow dispense in this stub
    if not inhibit_dispense("ground_maintenance") or not inhibit_dispense("weight_on_wheels"):
        print("FAIL: ground/WOW must INHIBIT", file=sys.stderr)
        fails += 1
    else:
        print("OK: ground/WOW inhibit held")

    if fails:
        return 1
    print("OK: ew_inhibit_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
