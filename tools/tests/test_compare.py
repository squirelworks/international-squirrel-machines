"""Synthetic before/after tests for cad_verify ERC/DRC comparison. Run: python3 test_compare.py"""
import json, sys, tempfile, copy, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import cad_verify as cv

def v(sev, typ, desc, items, x=0):
    return {"severity": sev, "type": typ, "description": desc,
            "items": [{"description": d, "pos": {"x": x, "y": 0}} for d in items]}

SHORT = v("error", "shorting_items", "Items shorting two nets (nets A and B)", ["Pad 1 [A] of U2", "Pad 2 [B] of U2"])
UNC = v("error", "unconnected_items", "Missing connection between items", ["Pad 1 [ROW0] of SW1", "Pad 1 [ROW0] of U1"])
PIN = v("error", "pin_not_connected", "Pin not connected", ["Symbol U1 Pin 4 [GND, Power input, Line]"])
WARN = v("warning", "lib_footprint_issues", "lib missing", ["Footprint U1"])

def mk(root, projects):
    """projects: {name: {"erc": [viols] | "FAIL", "drc": [viols] | "FAIL"}}"""
    root = Path(root); summ = {"kicad": []}
    for name, kinds in projects.items():
        d = root / "kicad" / name.replace("/", "__"); d.mkdir(parents=True, exist_ok=True)
        p = {"project": name}
        for kind, viols in kinds.items():
            if viols == "FAIL":
                p[kind] = {"status": "TOOL_FAILURE"}; continue
            rep = {"sheets": [{"path": "/", "violations": viols}]} if kind == "erc" else {"violations": viols, "unconnected_items": [], "schematic_parity": []}
            (d / f"{kind}.json").write_text(json.dumps(rep))
            p[kind] = {"status": "ERRORS" if any(x["severity"] == "error" for x in viols) else "OK"}
        summ["kicad"].append(p)
    (root / "summary.json").write_text(json.dumps(summ)); return summ

BASE = {"kb": {"erc": [PIN, WARN], "drc": [UNC]}, "jet": {"erc": [], "drc": [SHORT]}}
def moved(x): y = copy.deepcopy(x); [i["pos"].update(x=99) for i in y["items"]]; return y
CASES = [  # name, head projects, expected (new, fixed)
    ("identical", BASE, (0, 0)),
    ("positions moved only", {"kb": {"erc": [moved(PIN), WARN], "drc": [moved(UNC)]}, "jet": {"erc": [], "drc": [moved(SHORT)]}}, (0, 0)),
    ("new warning only", {"kb": {"erc": [PIN, WARN, WARN], "drc": [UNC]}, "jet": {"erc": [], "drc": [SHORT]}}, (0, 0)),
    ("one new error", {"kb": {"erc": [PIN, WARN], "drc": [UNC, SHORT]}, "jet": {"erc": [], "drc": [SHORT]}}, (1, 0)),
    ("duplicate count rises", {"kb": {"erc": [PIN, PIN, WARN], "drc": [UNC]}, "jet": {"erc": [], "drc": [SHORT]}}, (1, 0)),
    ("error fixed", {"kb": {"erc": [WARN], "drc": [UNC]}, "jet": {"erc": [], "drc": [SHORT]}}, (0, 1)),
    ("same type, different refs", {"kb": {"erc": [v("error", "pin_not_connected", "Pin not connected", ["Symbol U1 Pin 5 [X]"]), WARN], "drc": [UNC]}, "jet": {"erc": [], "drc": [SHORT]}}, (1, 1)),
    ("new project with errors", {**BASE, "mouse": {"erc": [PIN], "drc": [UNC, SHORT]}}, (3, 0)),
    ("project removed", {"kb": BASE["kb"]}, (0, 1)),
    ("new tool failure", {"kb": {"erc": "FAIL", "drc": [UNC]}, "jet": {"erc": [], "drc": [SHORT]}}, (1, 1)),
]

fails = 0
with tempfile.TemporaryDirectory() as t:
    bs = mk(Path(t) / "base", BASE)
    for i, (name, head, (en, ef)) in enumerate(CASES):
        hs = mk(Path(t) / f"h{i}", head)
        c = cv.compare(Path(t) / "base", bs, Path(t) / f"h{i}", hs)
        ok = (c["total_new"], c["total_fixed"]) == (en, ef)
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name}: new={c['total_new']} fixed={c['total_fixed']} (expected {en},{ef})")
    # CLI exit codes via --compare-only
    for i, want in ((0, 0), (3, 1)):
        rc = subprocess.run([sys.executable, str(HERE.parent / "cad_verify.py"), "--compare-only",
                             "--baseline", str(Path(t) / "base"), "--out", str(Path(t) / f"h{i}")], capture_output=True).returncode
        ok = rc == want; fails += not ok
        print(f"{'PASS' if ok else 'FAIL'}  CLI --compare-only exit code case {CASES[i][0]}: rc={rc} (expected {want})")
print("ALL PASS" if not fails else f"{fails} FAILED"); sys.exit(1 if fails else 0)
