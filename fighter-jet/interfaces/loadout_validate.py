#!/usr/bin/env python3
"""A4 #122 / SS#173 — loadout legality check against hardpoints + catalogues.

Loads machine-readable interface YAML (no unknown required keys). Rejects
deliberately illegal fixture loadouts (e.g. LO-ILLEGAL-TIP-FUEL).

Usage:
  python3 fighter-jet/interfaces/loadout_validate.py
  python3 fighter-jet/interfaces/loadout_validate.py --loadout LO-TIP-AAM-SYM
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    # Minimal subset parser not needed — PyYAML is expected in CI / tools
    print("error: PyYAML required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent


def load(name: str) -> dict:
    path = ROOT / name
    with path.open() as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise SystemExit(f"error: {name} is not a mapping")
    return data


def store_mass(store_id: str, inert: dict, multi: dict) -> float | None:
    for s in inert.get("stores") or []:
        if s.get("id") == store_id:
            return float(s["mass_kg"])
    for s in multi.get("inert_catalogue") or []:
        if s.get("id") == store_id and "mass_kg" in s:
            return float(s["mass_kg"])
    return None


def store_ok_for_station(store_id: str, station_id: str, inert: dict, multi: dict) -> bool:
    for s in inert.get("stores") or []:
        if s.get("id") == store_id:
            return station_id in (s.get("compatible_stations") or [])
    # multi-origin: check compatibility_matrix
    for row in multi.get("compatibility_matrix") or []:
        if store_id in (row.get("stores") or []) and station_id in (row.get("stations") or []):
            return True
    # catalogue entry without matrix row → unknown
    for s in multi.get("inert_catalogue") or []:
        if s.get("id") == store_id:
            return False
    return False


def validate_loadout(loadout: dict, hardpoints: dict, inert: dict, multi: dict) -> list[str]:
    errors: list[str] = []
    stations_by_id = {s["id"]: s for s in hardpoints.get("stations") or []}
    for sta_id, store_id in (loadout.get("stations") or {}).items():
        sta = stations_by_id.get(sta_id)
        if sta is None:
            errors.append(f"unknown station {sta_id}")
            continue
        mass = store_mass(store_id, inert, multi)
        if mass is None:
            errors.append(f"unknown store {store_id}")
            continue
        max_kg = sta.get("max_store_class", {}).get("mass_kg_max", sta.get("mass_class_kg_max"))
        if max_kg is not None and mass > float(max_kg):
            errors.append(
                f"{store_id} mass {mass} kg exceeds {sta_id} max {max_kg} kg"
            )
        if not store_ok_for_station(store_id, sta_id, inert, multi):
            errors.append(f"{store_id} not compatible with {sta_id}")
        # required A4 keys present on station
        for key in ("max_store_class", "lug_class", "clearance_envelope"):
            if key not in sta:
                errors.append(f"{sta_id} missing {key}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--loadout", default=None, help="Loadout id from carriage-drag.yaml")
    args = ap.parse_args()

    hardpoints = load("hardpoints.yaml")
    inert = load("inert-stores.yaml")
    multi = load("multi-origin-stores.yaml")
    carriage = load("carriage-drag.yaml")
    safe = load("safe-inhibit-table.yaml")
    sensors = load("sensors.yaml")

    # Schema presence for SS#173 consumers
    required_top = [
        (hardpoints, "stations"),
        (carriage, "stores"),
        (carriage, "loadouts"),
        (safe, "rows"),
        (sensors, "apertures"),
        (multi, "station_limits"),
    ]
    for doc, key in required_top:
        if key not in doc:
            print(f"FAIL: missing key {key}", file=sys.stderr)
            return 1

    # Every safe-inhibit row output is SAFE or INHIBIT
    for row in safe["rows"]:
        if row.get("output") not in ("SAFE", "INHIBIT"):
            print(f"FAIL: row {row.get('id')} output {row.get('output')} not allowed", file=sys.stderr)
            return 1
        for bad in ("ARM", "RELEASE"):
            if bad in str(row.get("output")):
                print(f"FAIL: ARM/RELEASE in table row {row.get('id')}", file=sys.stderr)
                return 1

    # Every station has max / lug / clearance
    for sta in hardpoints["stations"]:
        for key in ("max_store_class", "lug_class", "clearance_envelope"):
            if key not in sta:
                print(f"FAIL: {sta.get('id')} missing {key}", file=sys.stderr)
                return 1

    loadouts = {lo["id"]: lo for lo in carriage["loadouts"]}
    targets = [args.loadout] if args.loadout else list(loadouts)
    rejected_illegal = False
    for lid in targets:
        lo = loadouts.get(lid)
        if lo is None:
            print(f"FAIL: unknown loadout {lid}", file=sys.stderr)
            return 1
        errs = validate_loadout(lo, hardpoints, inert, multi)
        if lo.get("deliberately_illegal"):
            if not errs:
                print(f"FAIL: {lid} should be rejected but passed", file=sys.stderr)
                return 1
            print(f"OK: rejected illegal loadout {lid}: {errs[0]}")
            rejected_illegal = True
        else:
            if errs:
                print(f"FAIL: {lid}: {'; '.join(errs)}", file=sys.stderr)
                return 1
            print(f"OK: loadout {lid}")

    if args.loadout is None and not rejected_illegal:
        print("FAIL: expected LO-ILLEGAL-TIP-FUEL rejection", file=sys.stderr)
        return 1

    print("OK: loadout_validate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
