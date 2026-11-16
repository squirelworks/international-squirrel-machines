#!/usr/bin/env python3
"""ISM CAD verification: OpenSCAD renders, KiCad ERC/DRC, fab-readiness.

Usage: cad_verify.py [--repo .] [--out cad-verify-out] [--timeout 600]
                     [--kicad-mode report|new|all] [--baseline BASE_OUT_DIR]
                     [--fail-on-warning] [--require-fab] [--skip-scad] [--skip-kicad]
       cad_verify.py --compare-only --baseline BASE_OUT_DIR --out HEAD_OUT_DIR

Writes <out>/summary.json, <out>/summary.md, per-file logs, STLs and KiCad JSON
reports. Always fails (exit 1) on OpenSCAD ERROR/TIMEOUT/EMPTY renders.
KiCad ERC/DRC handling (--kicad-mode):
  report  never fail on ERC/DRC violations (default); counts go to summary.md
  new     fail only on error-severity violations that are NEW versus --baseline
          (another cad_verify output dir, e.g. from the PR base commit) or on a
          kicad-cli tool failure that the baseline did not have
  all     fail on any ERC/DRC error (old behaviour)
Violations are fingerprinted as (project, erc|drc, type, description, sorted item
descriptions) -- positions are ignored so moving a part does not create a "new"
error -- and compared as multisets.
"""
import argparse, csv, io, json, os, re, struct, subprocess, sys, time, zipfile
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".github"}
PRIORITY = ["fighter-jet/tooling/", "fighter-jet/shell/airframe.scad", "/shell/"]

def walk(repo, exts):
    for root, dirs, files in os.walk(repo):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for f in sorted(files):
            if any(f.endswith(e) for e in exts):
                yield Path(root, f).relative_to(repo)

def prio(p):
    s = str(p)
    for i, k in enumerate(PRIORITY):
        if k in s:
            return (i, s)
    return (len(PRIORITY), s)

# ---------- OpenSCAD ----------
def strip_comments(src):
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    src = re.sub(r"//[^\n]*", " ", src)
    return re.sub(r'"(\\.|[^"\\])*"', '""', src)

def top_level_statements(src):
    """Remove module/function definitions; return remaining top-level text."""
    s = strip_comments(src)
    out, i = [], 0
    pat = re.compile(r"\b(module|function)\s+[A-Za-z_]\w*\s*\(")
    while True:
        m = pat.search(s, i)
        if not m:
            out.append(s[i:]); break
        out.append(s[i:m.start()])
        j, depth = m.end(), 1
        while j < len(s) and depth:            # close the parameter list
            depth += {"(": 1, ")": -1}.get(s[j], 0); j += 1
        if m.group(1) == "function":
            j = s.find(";", j) + 1 or len(s)
        else:
            while j < len(s) and s[j].isspace(): j += 1
            if j < len(s) and s[j] == "{":
                depth, j = 1, j + 1
                while j < len(s) and depth:
                    depth += {"{": 1, "}": -1}.get(s[j], 0); j += 1
            else:
                j = s.find(";", j) + 1 or len(s)
        i = j
    return "".join(out)

def draws_something(src):
    rest = top_level_statements(src)
    rest = re.sub(r"\b(include|use)\s*<[^>]*>", " ", rest)
    rest = re.sub(r"\$?[A-Za-z_]\w*\s*=[^;]*;", " ", rest)   # assignments
    return bool(re.search(r"[A-Za-z_]\w*\s*\(|[#%!*]\s*[A-Za-z_]", rest))

def included_targets(repo, scads):
    targets = set()
    for f in scads:
        src = (repo / f).read_text(errors="replace")
        for m in re.finditer(r"\b(?:include|use)\s*<([^>]+)>", strip_comments(src)):
            cand = (repo / f).parent / m.group(1)
            try: targets.add(cand.resolve().relative_to(repo.resolve()))
            except ValueError: pass
    return targets

def stl_stats(path):
    data = path.read_bytes()
    tris = []
    if data[:5].lower() == b"solid" and b"facet" in data[:400]:
        vs = [tuple(map(float, l.split()[1:4])) for l in data.decode(errors="replace").splitlines()
              if l.strip().startswith("vertex")]
        tris = [vs[i:i+3] for i in range(0, len(vs) - len(vs) % 3, 3)]
    elif len(data) >= 84:
        n = struct.unpack("<I", data[80:84])[0]
        for k in range(n):
            o = 84 + 50 * k + 12
            if o + 36 > len(data): break
            v = struct.unpack("<9f", data[o:o+36])
            tris.append([v[0:3], v[3:6], v[6:9]])
    st = {"facets": len(tris)}
    if tris:
        pts = [p for t in tris for p in t]
        st["bbox_min"] = [round(min(p[i] for p in pts), 3) for i in range(3)]
        st["bbox_max"] = [round(max(p[i] for p in pts), 3) for i in range(3)]
        st["size"] = [round(st["bbox_max"][i] - st["bbox_min"][i], 3) for i in range(3)]
    try:
        import trimesh
        m = trimesh.load(str(path), force="mesh", process=True)
        st["watertight"] = bool(m.is_watertight)
        st["winding_consistent"] = bool(m.is_winding_consistent)
        st["bodies"] = len(m.split(only_watertight=False))
        st["volume_mm3"] = round(float(m.volume), 1) if m.is_watertight else None
        from collections import Counter
        import numpy as np
        ec = Counter(map(tuple, np.sort(m.edges, axis=1).tolist()))
        st["nonmanifold_edges"] = sum(1 for c in ec.values() if c > 2)
        st["boundary_edges"] = sum(1 for c in ec.values() if c == 1)
    except ImportError:
        st["trimesh"] = "not installed"
    except Exception as e:
        st["trimesh_error"] = repr(e)
    return st

def render_scad(repo, f, out, timeout, openscad):
    stl = out / "stl" / f.with_suffix(".stl")
    log = out / "logs" / "scad" / (str(f).replace("/", "__") + ".log")
    stl.parent.mkdir(parents=True, exist_ok=True); log.parent.mkdir(parents=True, exist_ok=True)
    if stl.exists(): stl.unlink()
    t0 = time.time()
    try:
        p = subprocess.run([openscad, "-o", str(stl.resolve()), str(f)], cwd=repo,
                           capture_output=True, text=True, timeout=timeout)
        rc, err = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired as e:
        rc, err = None, ((e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")) \
                       + ((e.stderr or b"").decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or ""))
    dt = round(time.time() - t0, 2)
    log.write_text(f"# openscad -o {stl} {f}\n# rc={rc} seconds={dt}\n{err}")
    lines = err.splitlines()
    errors = [l for l in lines if re.match(r"^(ERROR|Parser error|CGAL error)", l, re.I) or "ERROR:" in l]
    warns = [l for l in lines if "WARNING" in l.upper() and l not in errors]
    r = {"file": str(f), "rc": rc, "seconds": dt, "log": str(log), "errors": errors, "warnings": warns}
    empty_msg = any(k in err for k in ("Current top level object is empty", "No top level geometry",
                                       "top-level object is empty", "Nothing to export"))
    if rc is None:
        r["status"] = "TIMEOUT"
    elif rc != 0 or errors:
        r["status"] = "EMPTY" if (empty_msg and not errors) else "ERROR"
    elif empty_msg or not stl.exists() or stl.stat().st_size == 0:
        r["status"] = "EMPTY"
    else:
        r["stl"] = str(stl); r["mesh"] = stl_stats(stl)
        r["status"] = "EMPTY" if r["mesh"]["facets"] == 0 else ("WARNING" if warns else "OK")
    return r

# ---------- KiCad ----------
def kicad_projects(repo):
    projs = {}
    for f in walk(repo, (".kicad_pro", ".kicad_sch", ".kicad_pcb")):
        projs.setdefault((f.parent, f.stem), set()).add(f.suffix)
    return projs

def run_kicad(repo, out, kicad_cli):
    results = []
    for (d, stem), sufs in sorted(kicad_projects(repo).items()):
        name = str(d / stem)
        rd = out / "kicad" / name.replace("/", "__"); rd.mkdir(parents=True, exist_ok=True)
        pr = {"project": name, "files": sorted(sufs)}
        for kind, suf, cmd in (("erc", ".kicad_sch", "sch"), ("drc", ".kicad_pcb", "pcb")):
            src = d / (stem + suf)
            if suf not in sufs:
                pr[kind] = {"status": "MISSING_FILE"}; continue
            rep = rd / f"{kind}.json"
            args = [kicad_cli, cmd, kind, "--format", "json", "--severity-all", "-o", str(rep.resolve())]
            if kind == "drc": args.append("--schematic-parity")
            args.append(str(src))
            p = subprocess.run(args, cwd=repo, capture_output=True, text=True, timeout=1800)
            (rd / f"{kind}.log").write_text(f"# {' '.join(args)}\n# rc={p.returncode}\n{p.stdout}{p.stderr}")
            k = {"rc": p.returncode, "report": str(rep), "stdout": (p.stdout + p.stderr).strip()[-2000:]}
            if not rep.exists():
                k["status"] = "TOOL_FAILURE"; pr[kind] = k; continue
            j = json.loads(rep.read_text())
            viols = []
            for sheet in j.get("sheets", []):
                for v in sheet.get("violations", []): v["_sheet"] = sheet.get("path"); viols.append(v)
            for key in ("violations", "unconnected_items", "schematic_parity"):
                for v in j.get(key, []): v["_group"] = key; viols.append(v)
            sev = {}
            for v in viols: sev[v.get("severity", "?")] = sev.get(v.get("severity", "?"), 0) + 1
            types = {}
            for v in viols:
                t = (v.get("severity"), v.get("type")); types[t] = types.get(t, 0) + 1
            k.update(status="OK" if not sev.get("error") else "ERRORS", severity_counts=sev,
                     by_type=[{"severity": s, "type": t, "count": c} for (s, t), c in sorted(types.items(), key=lambda x: (str(x[0][0]), -x[1]))],
                     examples=[{"severity": v.get("severity"), "type": v.get("type"), "description": v.get("description"),
                                "items": [i.get("description") for i in v.get("items", [])][:3]} for v in viols[:40]],
                     kicad_version=j.get("kicad_version"))
            pr[kind] = k
        results.append(pr)
    return results

def load_violations(report_path):
    j = json.loads(Path(report_path).read_text())
    vs = []
    for sheet in j.get("sheets", []):
        vs += sheet.get("violations", [])
    for key in ("violations", "unconnected_items", "schematic_parity"):
        vs += j.get(key, [])
    return vs

def fingerprint(project, kind, v):
    items = tuple(sorted((i.get("description") or "") for i in v.get("items", [])))
    return (project, kind, v.get("type") or "", v.get("description") or "", items)

def error_multiset(out_dir, summary):
    """Counter of error-severity fingerprints, plus set of (project, kind) tool failures."""
    from collections import Counter
    c, failures = Counter(), set()
    for p in summary.get("kicad", []):
        for kind in ("erc", "drc"):
            k = p.get(kind, {})
            if k.get("status") == "TOOL_FAILURE": failures.add((p["project"], kind)); continue
            rep = Path(out_dir) / "kicad" / p["project"].replace("/", "__") / f"{kind}.json"
            if not rep.exists(): continue
            for v in load_violations(rep):
                if v.get("severity") == "error":
                    c[fingerprint(p["project"], kind, v)] += 1
    return c, failures

def compare(base_dir, base_summary, head_dir, head_summary):
    bc, bf = error_multiset(base_dir, base_summary)
    hc, hf = error_multiset(head_dir, head_summary)
    new, fixed = hc - bc, bc - hc
    projects = sorted({k[0] for k in list(bc) + list(hc)} | {p["project"] for p in head_summary.get("kicad", [])} | {p["project"] for p in base_summary.get("kicad", [])})
    rows = []
    for pr in projects:
        for kind in ("erc", "drc"):
            b = sum(n for k, n in bc.items() if k[:2] == (pr, kind)); h = sum(n for k, n in hc.items() if k[:2] == (pr, kind))
            nn = sum(n for k, n in new.items() if k[:2] == (pr, kind)); ff = sum(n for k, n in fixed.items() if k[:2] == (pr, kind))
            rows.append({"project": pr, "kind": kind, "base_errors": b, "head_errors": h, "new": nn, "fixed": ff})
    as_list = lambda c: [{"project": k[0], "kind": k[1], "type": k[2], "description": k[3], "items": list(k[4]), "count": n} for k, n in sorted(c.items())]
    return {"rows": rows, "new_errors": as_list(new), "fixed_errors": as_list(fixed),
            "new_tool_failures": sorted(map(list, hf - bf)), "total_new": sum(new.values()) + len(hf - bf),
            "total_fixed": sum(fixed.values())}

def compare_md(cmp):
    L = ["## ERC/DRC errors vs baseline", "", "| Project | Check | Base errors | Head errors | New | Fixed |", "|---|---|---|---|---|---|"]
    for r in cmp["rows"]:
        L.append(f"| `{r['project']}` | {r['kind'].upper()} | {r['base_errors']} | {r['head_errors']} | {r['new']} | {r['fixed']} |")
    if cmp["new_errors"] or cmp["new_tool_failures"]:
        L += ["", f"### NEW errors ({cmp['total_new']})", ""]
        for e in cmp["new_errors"]:
            L.append(f"- `{e['project']}` {e['kind'].upper()} **{e['type']}** x{e['count']}: {e['description']} | " + " / ".join(e["items"]))
        for f in cmp["new_tool_failures"]:
            L.append(f"- `{f[0]}` {f[1].upper()}: kicad-cli TOOL_FAILURE (not failing on base)")
    else:
        L += ["", "No new ERC/DRC errors versus baseline."]
    if cmp["fixed_errors"]:
        L += ["", f"### Fixed errors ({cmp['total_fixed']})", ""]
        for e in cmp["fixed_errors"][:50]:
            L.append(f"- `{e['project']}` {e['kind'].upper()} {e['type']} x{e['count']}: {e['description']} | " + " / ".join(e["items"]))
    return "\n".join(L) + "\n"

# ---------- Fab readiness ----------
LCSC = re.compile(r"^C\d{1,9}$")
NON_DEVICE_TOP = {"docs", "common", ".github", "ci", "tools"}
VARIANT_PARENTS = {"keyboard", "storage"}          # subfolders are separate devices (sizes/types)
NON_VARIANT_SUB = {"kicad", "shell", "fab", "docs", "diagrams", "common"}
def device_dirs(repo):
    devs = set()
    for f in walk(repo, (".kicad_pcb", ".kicad_pro")):
        parts = f.parts
        dev = Path(*parts[:parts.index("kicad")]) if "kicad" in parts[:-1] else f.parent
        devs.add(dev)
    for d in sorted(repo.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name in NON_DEVICE_TOP: continue
        subs = [s for s in sorted(d.iterdir()) if s.is_dir() and s.name not in NON_VARIANT_SUB] if d.name in VARIANT_PARENTS else []
        if subs: devs.update(s.relative_to(repo) for s in subs)
        else: devs.add(d.relative_to(repo))
    # drop a device if a more specific device (with its own KiCad) lives under it, unless it has its own
    return sorted(devs)

def fab_check(repo, dev):
    base = repo / dev
    r = {"device": str(dev)}
    fabs = [p for p in base.rglob("fab") if p.is_dir()]
    r["fab_dir"] = [str(p.relative_to(repo)) for p in fabs]
    allf = [p for p in base.rglob("*") if p.is_file() and ".git" not in p.parts]
    zips = [p for p in allf if p.suffix.lower() == ".zip"]
    r["zips"] = []
    for z in zips:
        try:
            names = zipfile.ZipFile(z).namelist()
        except zipfile.BadZipFile:
            names = ["<bad zip>"]
        gerb = [n for n in names if re.search(r"\.(g[tbm][lsop]|g\d+|gko|gm\d+|gbr|gtp|gbp)$", n, re.I)]
        drl = [n for n in names if re.search(r"\.(drl|xln|exc|txt)$", n, re.I)]
        r["zips"].append({"zip": str(z.relative_to(repo)), "layers": names, "gerbers": len(gerb), "drill": len(drl)})
    r["gerber_drill_zip"] = any(z["gerbers"] and z["drill"] for z in r["zips"])
    boms = [p for p in allf if re.search(r"bom.*\.csv$", p.name, re.I)]
    r["bom"] = []
    for b in boms:
        rows = list(csv.DictReader(io.StringIO(b.read_text(errors="replace"))))
        col = next((c for c in (rows[0].keys() if rows else []) if c and re.search(r"lcsc|jlc", c, re.I)), None)
        missing = malformed = 0
        for row in rows:
            v = (row.get(col) or "").strip() if col else ""
            if not v: missing += 1
            elif not LCSC.match(v): malformed += 1
        r["bom"].append({"file": str(b.relative_to(repo)), "rows": len(rows), "lcsc_column": col,
                         "missing_lcsc": missing, "malformed_lcsc": malformed})
    r["cpl"] = [str(p.relative_to(repo)) for p in allf if re.search(r"(cpl|pos|position|placement|centroid).*\.(csv|pos)$", p.name, re.I)]
    r["stl"] = [str(p.relative_to(repo)) for p in allf if p.suffix.lower() == ".stl"]
    r["step"] = [str(p.relative_to(repo)) for p in allf if p.suffix.lower() in (".step", ".stp")]
    r["ready"] = bool(r["fab_dir"] and r["gerber_drill_zip"] and r["bom"] and all(b["missing_lcsc"] == b["malformed_lcsc"] == 0 for b in r["bom"])
                      and r["cpl"] and r["stl"] and r["step"])
    return r

# ---------- main ----------
def md(summary):
    L = ["# CAD verify summary", "", f"Repo: `{summary['repo']}`  ", f"Tools: {summary['tools']}", "",
         "## OpenSCAD", "", "| File | Status | Facets | Size (mm) | Watertight | Bodies | Notes |", "|---|---|---|---|---|---|---|"]
    for r in summary["scad"]:
        m = r.get("mesh", {})
        note = "; ".join(r.get("errors", []) + r.get("warnings", [])) or r.get("lib_reason", "")
        L.append(f"| `{r['file']}` | {r['status']} | {m.get('facets','')} | {m.get('size','')} | {m.get('watertight','')} | {m.get('bodies','')} | {note} |")
    L += ["", f"## KiCad ERC/DRC (mode: {summary.get('kicad_mode','?')})", "", "| Project | Check | Status | Errors | Warnings | Top types |", "|---|---|---|---|---|---|"]
    for p in summary["kicad"]:
        for k in ("erc", "drc"):
            x = p.get(k, {}); sc = x.get("severity_counts", {})
            top = ", ".join(f"{t['type']}x{t['count']}" for t in x.get("by_type", []) if t["severity"] == "error")
            L.append(f"| `{p['project']}` | {k.upper()} | {x.get('status')} | {sc.get('error', 0)} | {sc.get('warning', 0)} | {top} |")
    if summary.get("compare"):
        L += ["", compare_md(summary["compare"])]
    L += ["", "## Fab readiness", "", "| Device | fab/ | gerber+drill zip | BOM (rows/missing/malformed LCSC) | CPL | STL | STEP | Ready |", "|---|---|---|---|---|---|---|---|"]
    for f in summary["fab"]:
        bom = ", ".join(f"{b['rows']}/{b['missing_lcsc']}/{b['malformed_lcsc']}" for b in f["bom"]) or "none"
        L.append(f"| `{f['device']}` | {'yes' if f['fab_dir'] else 'no'} | {'yes' if f['gerber_drill_zip'] else 'no'} | {bom} | {len(f['cpl'])} | {len(f['stl'])} | {len(f['step'])} | {'YES' if f['ready'] else 'NO'} |")
    L += ["", f"**Result: {'FAIL' if summary['failed'] else 'PASS'}** — " + "; ".join(summary["fail_reasons"])]
    return "\n".join(L) + "\n"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="."); ap.add_argument("--out", default="cad-verify-out")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--openscad", default=os.environ.get("OPENSCAD", "openscad"))
    ap.add_argument("--kicad-cli", default=os.environ.get("KICAD_CLI", "kicad-cli"))
    ap.add_argument("--fail-on-warning", action="store_true"); ap.add_argument("--require-fab", action="store_true")
    ap.add_argument("--skip-scad", action="store_true"); ap.add_argument("--skip-kicad", action="store_true")
    ap.add_argument("--kicad-mode", choices=("report", "new", "all"), default="report")
    ap.add_argument("--baseline", help="cad_verify output dir from the base commit (for --kicad-mode new)")
    ap.add_argument("--compare-only", action="store_true", help="only compare --baseline with existing --out")
    a = ap.parse_args()
    if a.kicad_mode == "new" and not a.baseline and not a.compare_only:
        ap.error("--kicad-mode new needs --baseline")
    if a.compare_only:
        out = Path(a.out); hs = json.loads((out / "summary.json").read_text())
        bs = json.loads((Path(a.baseline) / "summary.json").read_text())
        cmp = compare(a.baseline, bs, out, hs)
        (out / "compare.json").write_text(json.dumps(cmp, indent=2)); (out / "compare.md").write_text(compare_md(cmp))
        print(compare_md(cmp)); return 1 if cmp["total_new"] else 0
    repo, out = Path(a.repo).resolve(), Path(a.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    def ver(cmd):
        try: p = subprocess.run(cmd, capture_output=True, text=True, timeout=60); return (p.stdout + p.stderr).strip().splitlines()[-1]
        except Exception as e: return f"unavailable ({e})"
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.strip()
    summary = {"repo": f"{repo.name}@{head}", "tools": {"openscad": ver([a.openscad, "--version"]), "kicad-cli": ver([a.kicad_cli, "version"])}}
    scads = sorted(walk(repo, (".scad",)), key=prio)
    targets = included_targets(repo, scads)
    summary["scad"] = []
    if not a.skip_scad:
        for f in scads:
            src = (repo / f).read_text(errors="replace")
            if not draws_something(src):
                r = {"file": str(f), "status": "LIB",
                     "lib_reason": ("include/use target" if f in targets else "NOT referenced by any include/use")
                                   + "; no top-level geometry statements (only module/function/variable definitions)"}
                summary["scad"].append(r); print(f"[scad] LIB      {f}", flush=True); continue
            r = render_scad(repo, f, out, a.timeout, a.openscad)
            summary["scad"].append(r); print(f"[scad] {r['status']:8} {f} ({r['seconds']}s)", flush=True)
    summary["kicad"] = [] if a.skip_kicad else run_kicad(repo, out, a.kicad_cli)
    for p in summary["kicad"]:
        print(f"[kicad] {p['project']}: ERC {p.get('erc',{}).get('status')} {p.get('erc',{}).get('severity_counts','')} | DRC {p.get('drc',{}).get('status')} {p.get('drc',{}).get('severity_counts','')}", flush=True)
    summary["fab"] = [fab_check(repo, d) for d in device_dirs(repo)]
    reasons = []
    bad = [r["file"] for r in summary["scad"] if r["status"] in ("ERROR", "TIMEOUT", "EMPTY")]
    if bad: reasons.append(f"scad failures: {bad}")
    if a.fail_on_warning:
        w = [r["file"] for r in summary["scad"] if r["status"] == "WARNING"]
        if w: reasons.append(f"scad warnings: {w}")
    summary["kicad_mode"] = a.kicad_mode
    if a.baseline:
        bs = json.loads((Path(a.baseline) / "summary.json").read_text())
        summary["compare"] = cmp = compare(a.baseline, bs, out, summary)
        (out / "compare.json").write_text(json.dumps(cmp, indent=2)); (out / "compare.md").write_text(compare_md(cmp))
        print(f"[kicad] vs baseline: {cmp['total_new']} new error(s), {cmp['total_fixed']} fixed")
    if a.kicad_mode == "all":
        for p in summary["kicad"]:
            for k in ("erc", "drc"):
                st = p.get(k, {}).get("status")
                if st in ("ERRORS", "TOOL_FAILURE"): reasons.append(f"{p['project']} {k}: {st}")
    elif a.kicad_mode == "new" and summary["compare"]["total_new"]:
        reasons.append(f"{summary['compare']['total_new']} NEW ERC/DRC error(s) vs baseline (see compare.md)")
    if a.require_fab:
        nr = [f["device"] for f in summary["fab"] if not f["ready"]]
        if nr: reasons.append(f"not fab-ready: {nr}")
    summary["failed"], summary["fail_reasons"] = bool(reasons), reasons
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    (out / "summary.md").write_text(md(summary))
    print(f"RESULT: {'FAIL' if reasons else 'PASS'}"); [print(" -", r) for r in reasons]
    return 1 if reasons else 0

if __name__ == "__main__":
    sys.exit(main())
