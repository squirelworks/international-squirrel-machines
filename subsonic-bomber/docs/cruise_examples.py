#!/usr/bin/env python3
"""#38 — teaching cruise / payload-mass check for ISM-SB-1.

Classroom Breguet stub and inert payload fraction only.
No weapons effectiveness, seekers, or live stores models.
"""
from __future__ import annotations

import math
import sys

# Teaching stubs
L_D = 16.0
SFC_PER_HR = 0.55  # 1/h class
V_KTAS = 420.0
W_EMPTY_KG = 45000.0
W_FUEL_KG = 30000.0
W_PAYLOAD_INERT_KG = 10000.0
W_CREW_SYS_KG = 5000.0


def takeoff_mass() -> float:
    return W_EMPTY_KG + W_FUEL_KG + W_PAYLOAD_INERT_KG + W_CREW_SYS_KG


def breguet_nm(ld: float, sfc: float, v_ktas: float, w0: float, w1: float) -> float:
    """Simplified Breguet: R = (V / SFC) * (L/D) * ln(W0/W1), V in kt, SFC 1/h → nm."""
    return (v_ktas / sfc) * ld * math.log(w0 / w1)


def main() -> int:
    w0 = takeoff_mass()
    w1 = w0 - W_FUEL_KG  # burn all fuel stub
    r = breguet_nm(L_D, SFC_PER_HR, V_KTAS, w0, w1)
    frac = W_PAYLOAD_INERT_KG / w0
    fails = 0

    if abs(w0 - 90000.0) > 1e-9:
        print(f"FAIL: W0 got {w0}, expected 90000", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: W0_kg={w0:.0f}")

    # ln(90000/60000)=ln(1.5)≈0.405465
    expected_r = (420.0 / 0.55) * 16.0 * math.log(1.5)
    if abs(r - expected_r) > 1e-6:
        print(f"FAIL: range got {r}, expected {expected_r}", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: range_nm≈{r:.0f}")

    if abs(frac - (10000.0 / 90000.0)) > 1e-12:
        print(f"FAIL: payload frac {frac}", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: inert_payload_frac={frac:.4f}")

    if fails:
        return 1
    print("OK: cruise_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
