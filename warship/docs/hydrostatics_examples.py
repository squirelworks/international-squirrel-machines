#!/usr/bin/env python3
"""B2 #43 — textbook hydrostatics teaching checks.

Δ = ρ * ∇
BM ≈ I_T / ∇
KM = KB + BM
GM = KM - KG

Classroom identities only — not a classified hull or stability booklet.
"""
from __future__ import annotations

import math
import sys

RHO_SW = 1025.0  # kg/m^3 teaching seawater


def displacement_kg(volume_m3: float, rho: float = RHO_SW) -> float:
    return rho * volume_m3


def bm_m(i_t_m4: float, volume_m3: float) -> float:
    return i_t_m4 / volume_m3


def gm_m(kb_m: float, bm: float, kg_m: float) -> float:
    return (kb_m + bm) - kg_m


def main() -> int:
    # Study ship: ∇ = 3500 m³, approx rectangle waterplane 100×12 → I_T = B*L^3/12 for beam? 
    # Use transverse I about centerline: I_T = L * B^3 / 12
    L, B = 100.0, 12.0
    volume = 3500.0
    i_t = L * (B**3) / 12.0
    kb = 3.2
    kg = 5.0

    delta = displacement_kg(volume)
    bm = bm_m(i_t, volume)
    gm = gm_m(kb, bm, kg)

    fails = 0
    checks = [
        ("displacement_t", delta / 1000.0, 3587.5, 1.0),
        ("BM_m", bm, 4.114, 0.02),
        ("GM_m", gm, 2.314, 0.02),
    ]
    for name, got, exp, tol in checks:
        if abs(got - exp) > tol:
            print(f"FAIL: {name}: got {got:.4f}, expected ~{exp}", file=sys.stderr)
            fails += 1
        else:
            print(f"OK: {name}={got:.3f} (ref {exp})")

    if fails:
        return 1
    if gm <= 0:
        print("FAIL: GM must be positive in study case", file=sys.stderr)
        return 1
    print("OK: hydrostatics_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
