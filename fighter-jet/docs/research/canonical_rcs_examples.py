#!/usr/bin/env python3
"""A3 #121 — analytic recomputation of textbook canonical RCS teaching examples.

Formulas (Knott / Jenn teaching level; not ISM-FJ-1 predictions):
  sphere (optical):     sigma = pi * a^2
  flat plate (PO, n):   sigma = 4 * pi * A^2 / lambda^2
  cylinder (broadside): sigma = 2 * pi * a * L^2 / lambda

Prints values to 3 significant figures and exits nonzero on mismatch.
"""
from __future__ import annotations

import math
import sys


def sig3(x: float) -> float:
    """Round to 3 significant figures."""
    if x == 0:
        return 0.0
    return float(f"{x:.3g}")


def main() -> int:
    # Sphere
    a_sph = 1.00
    sig_sph = math.pi * a_sph**2
    exp_sph = 3.14
    # Flat plate
    A = 1.00
    lam = 0.0300
    sig_plate = 4.0 * math.pi * A**2 / lam**2
    exp_plate = 1.40e4
    # Cylinder
    a_cyl = 0.500
    L = 2.00
    sig_cyl = 2.0 * math.pi * a_cyl * L**2 / lam
    exp_cyl = 419.0

    rows = [
        ("sphere", sig_sph, exp_sph, "m^2"),
        ("flat_plate", sig_plate, exp_plate, "m^2"),
        ("cylinder", sig_cyl, exp_cyl, "m^2"),
    ]

    print("canonical_rcs_examples (3 sig figs)")
    print(f"{'case':12} {'analytic':14} {'expected':14} {'unit':6} ok")
    fails = 0
    for name, analytic, expected, unit in rows:
        got = sig3(analytic)
        exp = sig3(expected)
        # Compare at 3 sig figs via relative tolerance
        ok = math.isclose(got, exp, rel_tol=0.005, abs_tol=0)
        # For large plate, also allow absolute compare on sig3 strings
        if f"{got:.3g}" != f"{exp:.3g}":
            ok = False
        print(f"{name:12} {got:14.6g} {exp:14.6g} {unit:6} {'Y' if ok else 'N'}")
        if not ok:
            fails += 1

    if fails:
        print(f"FAIL: {fails} mismatch(es)", file=sys.stderr)
        return 1
    print("OK: all canonical examples match to 3 significant figures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
