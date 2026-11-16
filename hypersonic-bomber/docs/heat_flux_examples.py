#!/usr/bin/env python3
"""#37 — teaching cold-wall heat-flux stub (educational only).

Uses a simplified Sutton–Graves–style identity for classroom order-of-magnitude:

  q ≈ k * sqrt(rho / Rn) * V^3

Constants are toy teaching values — not a trajectory prediction, not a TPS
sizing product, and not tied to any operational vehicle.
"""
from __future__ import annotations

import math
import sys

# Toy teaching constant (SI-ish classroom stub)
K_TEACH = 1.83e-4  # W·s³/(kg^0.5·m) order placeholder
RHO = 0.001  # kg/m³ rarefied/high-alt stub
RN = 0.5  # m nose radius
V = 6000.0  # m/s


def cold_wall_q(rho: float, rn: float, v: float, k: float = K_TEACH) -> float:
    return k * math.sqrt(rho / rn) * (v ** 3)


def main() -> int:
    q = cold_wall_q(RHO, RN, V)
    expected = K_TEACH * math.sqrt(RHO / RN) * (V ** 3)
    fails = 0

    if abs(q - expected) > 1e-6:
        print(f"FAIL: q got {q}, expected {expected}", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: q_W_m2≈{q:.3e}")

    # Blunter nose → lower q (teaching monotonicity)
    q_blunt = cold_wall_q(RHO, RN * 2.0, V)
    if not (q_blunt < q):
        print("FAIL: larger Rn should reduce q", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: q_blunter={q_blunt:.3e} < q")

    if q <= 0:
        print("FAIL: non-positive heat flux", file=sys.stderr)
        fails += 1

    if fails:
        return 1
    print("OK: heat_flux_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
