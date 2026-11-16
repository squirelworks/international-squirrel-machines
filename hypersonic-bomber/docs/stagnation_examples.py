#!/usr/bin/env python3
"""B1 #37 — perfect-gas stagnation temperature teaching examples.

T0 = T_inf * (1 + (gamma-1)/2 * M^2)

Classroom identity only — not an ISM-HB-1 trajectory prediction.
"""
from __future__ import annotations

import math
import sys

CASES = [
    # M, T_inf_K, gamma, expected_T0_K (3 sig figs)
    (5.0, 220.0, 1.4, 1320.0),
    (8.0, 220.0, 1.4, 3040.0),  # 3036 → 3040 at 3 sig
    (10.0, 220.0, 1.4, 4620.0),
]


def stagnation_temp(t_inf: float, mach: float, gamma: float = 1.4) -> float:
    return t_inf * (1.0 + (gamma - 1.0) / 2.0 * mach * mach)


def main() -> int:
    fails = 0
    for mach, t_inf, gamma, expected in CASES:
        got = stagnation_temp(t_inf, mach, gamma)
        # 3 significant figures comparison
        if not math.isclose(got, expected, rel_tol=0.005, abs_tol=5.0):
            print(f"FAIL: M={mach}: got {got:.1f} K, expected ~{expected} K", file=sys.stderr)
            fails += 1
        else:
            print(f"OK: M={mach:g} → T0={got:.0f} K (ref {expected:g})")
    if fails:
        print(f"FAIL: {fails} case(s)", file=sys.stderr)
        return 1
    print("OK: stagnation_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
