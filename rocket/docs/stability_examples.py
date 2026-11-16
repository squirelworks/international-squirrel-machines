#!/usr/bin/env python3
"""B4 #41 — static-margin teaching check (hobby rocket).

static_margin_calibers = (x_cp - x_cg) / diameter

Classroom identity for stable coast (target ~1–2 cal). Not a flight clearance.
No guidance / active control content.
"""
from __future__ import annotations

import sys


def static_margin_cal(x_cp_m: float, x_cg_m: float, diameter_m: float) -> float:
    return (x_cp_m - x_cg_m) / diameter_m


def main() -> int:
    # Study: D=40 mm, CG at 0.35 m from nose, CP at 0.42 m
    d = 0.040
    x_cg = 0.35
    x_cp = 0.42
    sm = static_margin_cal(x_cp, x_cg, d)

    fails = 0
    if abs(sm - 1.75) > 1e-9:
        print(f"FAIL: static margin got {sm}, expected 1.75", file=sys.stderr)
        fails += 1
    else:
        print(f"OK: static_margin_cal={sm:.2f} (ref 1.75)")

    if not (1.0 <= sm <= 2.5):
        print("FAIL: study case should sit in 1–2.5 cal teaching band", file=sys.stderr)
        fails += 1
    else:
        print("OK: within hobby teaching band 1–2.5 cal")

    if fails:
        return 1
    print("OK: stability_examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
