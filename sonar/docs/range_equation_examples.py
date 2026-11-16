#!/usr/bin/env python3
"""#40 — teaching active-sonar equation and time-of-flight depth stubs.

Classroom dB and c=1500 m/s values only — not a survey or combat product.
No quieting, beamforming, or acoustic-warfare content.
"""
from __future__ import annotations

import sys

# Toy dB stubs (public teaching order-of-magnitude)
SL = 200.0  # source level
TL = 40.0   # one-way transmission loss
TS = -20.0  # target strength (bottom / object class)
NL = 60.0   # noise level
DI = 10.0   # directivity index (simple)
DT = 10.0   # detection threshold

C_MS = 1500.0  # sound speed m/s teaching


def figure_of_merit(sl: float, tl: float, ts: float, nl: float, di: float) -> float:
    """Simplified: SL - 2*TL + TS - NL + DI (compare to DT)."""
    return sl - 2.0 * tl + ts - nl + di


def depth_m(time_of_flight_s: float, c: float = C_MS) -> float:
    return c * time_of_flight_s / 2.0


def main() -> int:
    fom = figure_of_merit(SL, TL, TS, NL, DI)
    d = depth_m(0.1)  # 100 ms round-trip → 75 m
    fails = 0

    # 200 - 80 - 20 - 60 + 10 = 50
    if abs(fom - 50.0) > 1e-9:
        print(f"FAIL: FOM got {fom}, expected 50.0", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: FOM={fom:.1f} dB (DT={DT:.1f})")

    if fom < DT:
        print("FAIL: FOM below DT in teaching case", file=sys.stderr)
        fails += 1
    else:
        print("OK: FOM >= DT")

    if abs(d - 75.0) > 1e-9:
        print(f"FAIL: depth got {d}, expected 75.0", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: depth_m={d:.1f} (ToF=0.1 s)")

    if fails:
        return 1
    print("OK: range_equation_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
