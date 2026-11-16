#!/usr/bin/env python3
"""#46 — teaching CG / limb-mass balance for ISM-MS-1 study.

Masses are classroom stubs for packaging, not a combat fit.
No seekers, guidance, warheads, or live stores models.
"""
from __future__ import annotations

import sys

# kg stubs (torso-centered x forward, z up — teaching 2D sagittal)
MASSES = {
    "torso": (800.0, 0.0, 1.2),
    "head": (40.0, 0.05, 2.0),
    "leg_l": (120.0, -0.1, 0.5),
    "leg_r": (120.0, -0.1, 0.5),
    "arm_l": (50.0, 0.2, 1.4),
    "arm_r": (50.0, 0.2, 1.4),
    "stores_inert": (80.0, -0.3, 1.1),  # dorsal inert mass box only
}


def total_mass(parts: dict[str, tuple[float, float, float]]) -> float:
    return sum(m for m, _, _ in parts.values())


def cg_xz(parts: dict[str, tuple[float, float, float]]) -> tuple[float, float]:
    m_tot = total_mass(parts)
    x = sum(m * x for m, x, _ in parts.values()) / m_tot
    z = sum(m * z for m, _, z in parts.values()) / m_tot
    return x, z


def main() -> int:
    m = total_mass(MASSES)
    x, z = cg_xz(MASSES)
    fails = 0

    if abs(m - 1260.0) > 1e-9:
        print(f"FAIL: mass got {m}, expected 1260.0", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: mass_kg={m:.1f}")

    # Expected: x = (40*0.05 + 240*(-0.1) + 100*0.2 + 80*(-0.3)) / 1260
    # = (2 - 24 + 20 - 24) / 1260 = -26/1260 ≈ -0.020635
    # z = (800*1.2 + 40*2 + 240*0.5 + 100*1.4 + 80*1.1) / 1260
    # = (960 + 80 + 120 + 140 + 88) / 1260 = 1388/1260 ≈ 1.101587
    if abs(x - (-26.0 / 1260.0)) > 1e-9 or abs(z - (1388.0 / 1260.0)) > 1e-9:
        print(f"FAIL: CG got ({x}, {z})", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: cg_x={x:.4f} m, cg_z={z:.4f} m")

    if fails:
        return 1
    print("OK: balance_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
