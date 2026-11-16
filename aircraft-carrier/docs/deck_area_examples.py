#!/usr/bin/env python3
"""#45 — teaching flight-deck area / parking budget for ISM-CV-1.

Classroom m² stubs only — not a real air-wing plan or combat fit.
No weapons interfaces or fire-control content.
"""
from __future__ import annotations

import sys

DECK_L_M = 300.0
DECK_B_M = 70.0
ANGLED_LANDING_M2 = 3500.0  # keep-out / landing strip class
PARKING_SPOT_M2 = 120.0     # teaching spot including taxi margin
SPOTS_TARGET = 40


def deck_area_m2(length_m: float, beam_m: float) -> float:
    return length_m * beam_m


def parking_capacity(deck_m2: float, landing_m2: float, spot_m2: float) -> int:
    usable = deck_m2 - landing_m2
    if usable <= 0 or spot_m2 <= 0:
        return 0
    return int(usable // spot_m2)


def main() -> int:
    area = deck_area_m2(DECK_L_M, DECK_B_M)
    spots = parking_capacity(area, ANGLED_LANDING_M2, PARKING_SPOT_M2)
    fails = 0

    if abs(area - 21000.0) > 1e-9:
        print(f"FAIL: area got {area}, expected 21000", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: deck_area_m2={area:.0f}")

    # (21000 - 3500) // 120 = 17500 // 120 = 145
    if spots != 145:
        print(f"FAIL: spots got {spots}, expected 145", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: parking_spots={spots}")

    if spots < SPOTS_TARGET:
        print("FAIL: below teaching spot target", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: spots >= target {SPOTS_TARGET}")

    if fails:
        return 1
    print("OK: deck_area_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
