#!/usr/bin/env python3
"""#39 — teaching recovery/stagnation temperature stub for ISM-XB-1.

Classroom isentropic recovery only (γ=1.4). Not a hypersonic TPS analysis
(#37) and not a materials allowables product. No weapons content.
"""
from __future__ import annotations

import sys

GAMMA = 1.4
T_INF_K = 216.65  # ISA tropopause-class freestream stub
M_CRUISE = 2.0


def recovery_temperature_k(t_inf: float, mach: float, gamma: float = GAMMA) -> float:
    """Adiabatic wall / stagnation temperature: T0 = T∞ (1 + (γ-1)/2 M²)."""
    return t_inf * (1.0 + (gamma - 1.0) / 2.0 * mach * mach)


def main() -> int:
    t0 = recovery_temperature_k(T_INF_K, M_CRUISE)
    # 216.65 * (1 + 0.2 * 4) = 216.65 * 1.8 = 389.97
    expected = T_INF_K * 1.8
    fails = 0

    if abs(t0 - expected) > 1e-9:
        print(f"FAIL: T0 got {t0}, expected {expected}", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: T0_K={t0:.2f} (M={M_CRUISE})")

    if t0 <= T_INF_K:
        print("FAIL: recovery not above freestream", file=sys.stderr)
        fails += 1
    else:
        print("OK: T0 > T_inf")

    # Milder than typical hypersonic teaching cases (M~5+)
    t0_hyp = recovery_temperature_k(T_INF_K, 5.0)
    if t0 >= t0_hyp:
        print("FAIL: cruise T0 should be below M5 stub", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: T0_M2 < T0_M5 ({t0_hyp:.2f})")

    if fails:
        return 1
    print("OK: thermal_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
