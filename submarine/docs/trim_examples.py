#!/usr/bin/env python3
"""B3 #44 — submarine trim / reserve-buoyancy teaching checks.

Freshwater scale-model teaching: ρ = 1000 kg/m³.
Reserve buoyancy fraction = 1 - Δ_surf / Δ_sub  (when both > 0).

No acoustic / quieting / life-support content.
"""
from __future__ import annotations

import sys

RHO_FW = 1000.0  # kg/m^3


def displacement_kg(volume_m3: float, rho: float = RHO_FW) -> float:
    return rho * volume_m3


def reserve_buoyancy_fraction(delta_surf_kg: float, delta_sub_kg: float) -> float:
    return 1.0 - (delta_surf_kg / delta_sub_kg)


def trim_moment_n_m(mass_kg: float, lever_m: float, g: float = 9.81) -> float:
    return mass_kg * g * lever_m


def main() -> int:
    # Study scale hull: submerged volume 0.012 m³; surfaced 0.010 m³
    v_sub, v_surf = 0.012, 0.010
    d_sub = displacement_kg(v_sub)
    d_surf = displacement_kg(v_surf)
    rb = reserve_buoyancy_fraction(d_surf, d_sub)

    # Trim: 0.05 kg lead 0.15 m forward of LCB → nose-down moment
    m_trim = trim_moment_n_m(0.05, 0.15)

    fails = 0
    checks = [
        ("delta_sub_kg", d_sub, 12.0, 0.01),
        ("delta_surf_kg", d_surf, 10.0, 0.01),
        ("reserve_buoyancy", rb, 1.0 / 6.0, 1e-6),
        ("trim_moment_Nm", m_trim, 0.073575, 1e-4),
    ]
    for name, got, exp, tol in checks:
        if abs(got - exp) > tol:
            print(f"FAIL: {name}: got {got}, expected ~{exp}", file=sys.stderr)
            fails += 1
        else:
            print(f"OK: {name}={got:.6g} (ref {exp})")

    if rb <= 0:
        print("FAIL: reserve buoyancy must be positive", file=sys.stderr)
        return 1
    if fails:
        return 1
    print("OK: trim_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
