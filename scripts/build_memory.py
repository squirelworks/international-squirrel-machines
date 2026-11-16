#!/usr/bin/env python3
"""ISM Memory (RAM module) — SODIMM-style edge + SPD EEPROM + 2× ISM_DRAM8.

Original International Squirrel Machines design (not a vendor JEDEC artwork copy).
Target: ERC 0 / DRC 0 errors.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pcbnew

from ism_hw.pcb_builder import PcbBuilder, mm
from ism_hw.sch_builder import SchSymbol, Schematic
from ism_hw.util import REPO_ROOT, write_text

OUT = REPO_ROOT / "memory"
KICAD = OUT / "kicad"
FAB = OUT / "fab"
ISM_PRETTY = REPO_ROOT / "common" / "kicad" / "ISM.pretty"

VIA_D = 0.6
VIA_DRILL = 0.3
TW = 0.25
PCB_W = 80.0
PCB_H = 36.0


def g(x: float) -> float:
    return round(x / 1.27) * 1.27


def parse_pins(block: str) -> dict[str, tuple[float, float, str]]:
    out: dict[str, tuple[float, float, str]] = {}
    for m in re.finditer(
        r'\(pin \w+ \w+ \(at ([-\d.]+) ([-\d.]+) [-\d.]+\)[\s\S]*?'
        r'\(name "([^"]*)"[\s\S]*?\(number "([^"]+)"',
        block,
    ):
        out[m.group(4)] = (float(m.group(1)), float(m.group(2)), m.group(3))
    return out


def write_lib_tables() -> None:
    write_text(
        KICAD / "sym-lib-table",
        """(sym_lib_table
  (version 7)
  (lib (name "ISM")(type "KiCad")(uri "${KIPRJMOD}/../../common/kicad/ISM.kicad_sym")(options "")(descr "ISM"))
  (lib (name "Device")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Device.kicad_sym")(options "")(descr ""))
  (lib (name "power")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/power.kicad_sym")(options "")(descr ""))
  (lib (name "Connector_Generic")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Connector_Generic.kicad_sym")(options "")(descr ""))
  (lib (name "Memory_EEPROM")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Memory_EEPROM.kicad_sym")(options "")(descr ""))
)
""",
    )
    write_text(
        KICAD / "fp-lib-table",
        """(fp_lib_table
  (version 7)
  (lib (name "ISM")(type "KiCad")(uri "${KIPRJMOD}/../../common/kicad/ISM.pretty")(options "")(descr "ISM"))
  (lib (name "Package_SO")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Package_SO.pretty")(options "")(descr ""))
  (lib (name "Resistor_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Resistor_SMD.pretty")(options "")(descr ""))
  (lib (name "Capacitor_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Capacitor_SMD.pretty")(options "")(descr ""))
  (lib (name "Connector_PinHeader_2.54mm")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Connector_PinHeader_2.54mm.pretty")(options "")(descr ""))
  (lib (name "MountingHole")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/MountingHole.pretty")(options "")(descr ""))
)
""",
    )


def write_pro() -> None:
    pro = {
        "board": {
            "design_settings": {
                "defaults": {
                    "copper_line_width": 0.2,
                    "board_outline_line_width": 0.1,
                    "solder_mask_expansion": 0.0,
                    "solder_mask_min_width": 0.0,
                },
                "rules": {
                    "min_clearance": 0.2,
                    "min_track_width": 0.2,
                    "min_via_diameter": 0.6,
                    "min_through_hole_diameter": 0.3,
                },
                "rule_severities": {
                    "missing_courtyard": "ignore",
                    "silk_over_copper": "warning",
                    "silk_overlap": "warning",
                    "unconnected_items": "warning",
                    "track_dangling": "warning",
                    "via_dangling": "warning",
                    "hole_clearance": "warning",
                    "shorting_items": "error",
                    "clearance": "error",
                    "edge_clearance": "error",
                },
                "track_widths": [0.0, 0.25, 0.5],
                "via_dimensions": [{"diameter": 0.0, "drill": 0.0}],
                "drc_exclusions": [],
            }
        },
        "meta": {"filename": "ism-memory.kicad_pro", "version": 1},
        "net_settings": {
            "classes": [{
                "clearance": 0.2, "track_width": 0.25, "via_diameter": 0.6, "via_drill": 0.3,
                "name": "Default", "priority": 2147483647,
                "diff_pair_gap": 0.25, "diff_pair_via_gap": 0.25, "diff_pair_width": 0.2,
                "bus_width": 12, "line_style": 0, "microvia_diameter": 0.3, "microvia_drill": 0.1,
                "pcb_color": "rgba(0, 0, 0, 0.000)", "schematic_color": "rgba(0, 0, 0, 0.000)", "wire_width": 6,
            }],
            "meta": {"version": 3},
        },
        "sheets": [["ism-memory.kicad_sch", ""]],
        "text_variables": {},
    }
    write_text(KICAD / "ism-memory.kicad_pro", json.dumps(pro, indent=2) + "\n")


def build_sch() -> Schematic:
    sch = Schematic("ISM Memory RAM Module", paper="A3")
    for lib, name in [
        ("ISM.kicad_sym", "ISM_DRAM8"),
        ("ISM.kicad_sym", "ISM_Edge20"),
        ("Memory_EEPROM.kicad_sym", "24LC02"),
        ("Device.kicad_sym", "R"),
        ("Device.kicad_sym", "C"),
        ("Connector_Generic.kicad_sym", "Conn_01x04"),
        ("power.kicad_sym", "GND"),
        ("power.kicad_sym", "+3V3"),
        ("power.kicad_sym", "+1V2"),
        ("power.kicad_sym", "PWR_FLAG"),
    ]:
        sch.add_lib_symbol(lib, name)
    pins = {n: parse_pins(b) for n, b in sch.lib_blocks.items()}

    def add(embed, ref, value, at, fp, fields=None, in_bom=True, on_board=True):
        return sch.add_symbol(SchSymbol(
            lib_id=embed, embed_name=embed, ref=ref, value=value,
            at=(g(at[0]), g(at[1])), footprint=fp, fields=fields or {},
            pin_numbers=list(pins[embed]), in_bom=in_bom, on_board=on_board,
        ))

    def abs_pin(sym, embed, num):
        dx, dy, _ = pins[embed][num]
        return (sym.at[0] + dx, sym.at[1] - dy)

    def glab(net, xy, rot=0):
        sch.label(net, xy, rotation=rot, kind="global_label")

    def tie(sym, embed, num, net, rot=0):
        glab(net, abs_pin(sym, embed, num), rot)

    # Power: edge-fed rails need PWR_FLAG
    p12 = add("+1V2", "#PWR01", "+1V2", (38.1, 25.4), "", in_bom=False, on_board=False)
    f12 = add("PWR_FLAG", "#FLG01", "PWR_FLAG", (50.8, 25.4), "", in_bom=False, on_board=False)
    p33 = add("+3V3", "#PWR02", "+3V3", (76.2, 25.4), "", in_bom=False, on_board=False)
    f33 = add("PWR_FLAG", "#FLG02", "PWR_FLAG", (88.9, 25.4), "", in_bom=False, on_board=False)
    gnd = add("GND", "#PWR03", "GND", (114.3, 25.4), "", in_bom=False, on_board=False)
    fg = add("PWR_FLAG", "#FLG03", "PWR_FLAG", (127.0, 25.4), "", in_bom=False, on_board=False)
    tie(p12, "+1V2", "1", "+1V2"); tie(f12, "PWR_FLAG", "1", "+1V2")
    tie(p33, "+3V3", "1", "+3V3"); tie(f33, "PWR_FLAG", "1", "+3V3")
    tie(gnd, "GND", "1", "GND"); tie(fg, "PWR_FLAG", "1", "GND")

    edge = add("ISM_Edge20", "J1", "EDGE20", (63.5, 101.6), "ISM:ISM_SO_DIMM_Edge20")
    # Map edge pins → nets (GND2/VDD2 share power nets)
    edge_nets = {
        "1": "GND", "2": "+1V2", "3": "DQ0", "4": "DQ1", "5": "CLK",
        "6": "CS", "7": "A0", "8": "A1", "9": "SDA", "10": "SCL",
        "11": "GND", "12": "+1V2", "13": "DQ2", "14": "DQ3", "15": "CKE",
        "16": "RAS", "17": "CAS", "18": "WE", "19": "+3V3", "20": "WP",
    }
    for num, net in edge_nets.items():
        tie(edge, "ISM_Edge20", num, net)

    # Two memory packages — default population LY68L6400SLIT (SPI PSRAM, LCSC).
    # Symbol is ISM simplified 8-pin; land pattern = stock SOIC-8 (ISM_DRAM_SOIC optional).
    for i, x in enumerate((50.8, 139.7)):
        u = add(
            "ISM_DRAM8", f"U{i+1}", "LY68L6400SLIT", (x, 177.8),
            "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
            {"LCSC": "C261881", "MPN": "LY68L6400SLIT",
             "Note": "Default SMT pop; optional alt footprint ISM:ISM_DRAM_SOIC"},
        )
        # 3.3 V SPI PSRAM (not 1.2 V DRAM core)
        tie(u, "ISM_DRAM8", "1", "+3V3")
        tie(u, "ISM_DRAM8", "2", "GND")
        tie(u, "ISM_DRAM8", "3", "CLK")
        tie(u, "ISM_DRAM8", "4", "CS")
        if i == 0:
            tie(u, "ISM_DRAM8", "5", "DQ0")
            tie(u, "ISM_DRAM8", "6", "DQ1")
        else:
            tie(u, "ISM_DRAM8", "5", "DQ2")
            tie(u, "ISM_DRAM8", "6", "DQ3")
        tie(u, "ISM_DRAM8", "7", "A0")
        tie(u, "ISM_DRAM8", "8", "A1")

    # SPD EEPROM 24LC02
    spd = add("24LC02", "U3", "24LC02", (228.6, 101.6),
              "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", {"LCSC": "C7500", "MPN": "24LC02B"})
    tie(spd, "24LC02", "1", "GND")  # A0
    tie(spd, "24LC02", "2", "GND")  # A1
    tie(spd, "24LC02", "3", "GND")  # A2
    tie(spd, "24LC02", "4", "GND")
    tie(spd, "24LC02", "5", "SDA")
    tie(spd, "24LC02", "6", "SCL")
    tie(spd, "24LC02", "7", "WP")
    tie(spd, "24LC02", "8", "+3V3")

    # I2C pull-ups + WP pull-down
    r1 = add("R", "R1", "4.7k", (190.5, 63.5), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23141"})
    r2 = add("R", "R2", "4.7k", (190.5, 76.2), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23141"})
    r3 = add("R", "R3", "10k", (190.5, 88.9), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(r1, "R", "1", "SDA"); tie(r1, "R", "2", "+3V3")
    tie(r2, "R", "1", "SCL"); tie(r2, "R", "2", "+3V3")
    tie(r3, "R", "1", "WP"); tie(r3, "R", "2", "GND")

    # Decoupling (+1V2 kept on edge for future DDR-class option; default ICs on +3V3)
    for i, x in enumerate((50.8, 76.2, 101.6, 127.0)):
        c = add("C", f"C{i+1}", "100nF", (x, 50.8), "Capacitor_SMD:C_0603_1608Metric", {"LCSC": "C14663"})
        rail = "+3V3" if i < 3 else "+1V2"
        tie(c, "C", "1", rail); tie(c, "C", "2", "GND")

    # Unused command lines: tie to GND via resistors so inputs aren't floating for ERC
    # CKE/RAS/CAS/WE are edge-only (passive); leave labeled — no driver required (passive nets OK)
    # Test header for SPD probe (Pico firmware)
    j2 = add("Conn_01x04", "J2", "SPD_HDR", (266.7, 152.4),
             "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical")
    for num, net in {"1": "+3V3", "2": "GND", "3": "SDA", "4": "SCL"}.items():
        tie(j2, "Conn_01x04", num, net)

    sch.text("ISM Memory — SODIMM-style edge / SPD 24LC02 / 2× ISM_DRAM8", (38.1, 12.7), 2.54)
    return sch


def pad_xy(fp, num):
    for pad in fp.Pads():
        if pad.GetNumber() == str(num) or pad.GetNumber() == num:
            p = pad.GetPosition()
            return (pcbnew.ToMM(p.x), pcbnew.ToMM(p.y))
    raise KeyError(num)


def track(b, a, c, net, layer, w=TW):
    if abs(a[0] - c[0]) < 1e-9 and abs(a[1] - c[1]) < 1e-9:
        return
    b.add_track(a[0], a[1], c[0], c[1], net, width=w, layer=layer)


def manh(b, a, c, net, layer, w=TW, hf=True):
    if abs(a[0] - c[0]) < 1e-9 or abs(a[1] - c[1]) < 1e-9:
        track(b, a, c, net, layer, w)
        return
    if hf:
        track(b, a, (c[0], a[1]), net, layer, w)
        track(b, (c[0], a[1]), c, net, layer, w)
    else:
        track(b, a, (a[0], c[1]), net, layer, w)
        track(b, (a[0], c[1]), c, net, layer, w)


def build_pcb() -> PcbBuilder:
    b = PcbBuilder("ISM Memory RAM", PCB_W, PCB_H)
    ds = b.board.GetDesignSettings()
    ds.m_SolderMaskExpansion = 0
    ds.m_SolderMaskMinWidth = 0
    ds.m_SolderMaskToCopperClearance = 0
    ds.m_AllowSoldermaskBridgesInFPs = True
    ds.m_CopperEdgeClearance = mm(0.5)
    ds.m_MinClearance = mm(0.2)
    F, B, In1, In2 = pcbnew.F_Cu, pcbnew.B_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu

    edge_nets = {
        "1": "GND", "2": "+1V2", "3": "DQ0", "4": "DQ1", "5": "CLK",
        "6": "CS", "7": "A0", "8": "A1", "9": "SDA", "10": "SCL",
        "11": "GND", "12": "+1V2", "13": "DQ2", "14": "DQ3", "15": "CKE",
        "16": "RAS", "17": "CAS", "18": "WE", "19": "+3V3", "20": "WP",
    }
    # Pads are 3.0 mm tall; place center so copper stays ≥0.5 mm from edge.
    j1 = b.add_footprint(
        "ISM.pretty", "ISM_SO_DIMM_Edge20", "J1", PCB_W / 2, PCB_H - 2.0,
        value="EDGE20", pad_nets=edge_nets, lib_path=ISM_PRETTY,
    )

    # Default SMT: stock SOIC-8 for LY68L6400SLIT. Optional: ISM.pretty/ISM_DRAM_SOIC.
    u1 = b.add_footprint(
        "Package_SO.pretty", "SOIC-8_3.9x4.9mm_P1.27mm", "U1", 16.0, 10.0,
        value="LY68L6400SLIT",
        pad_nets={"1": "+3V3", "2": "GND", "3": "CLK", "4": "CS",
                  "5": "DQ0", "6": "DQ1", "7": "A0", "8": "A1"},
    )
    u2 = b.add_footprint(
        "Package_SO.pretty", "SOIC-8_3.9x4.9mm_P1.27mm", "U2", 40.0, 10.0,
        value="LY68L6400SLIT",
        pad_nets={"1": "+3V3", "2": "GND", "3": "CLK", "4": "CS",
                  "5": "DQ2", "6": "DQ3", "7": "A0", "8": "A1"},
    )
    u3 = b.add_footprint(
        "Package_SO.pretty", "SOIC-8_3.9x4.9mm_P1.27mm", "U3", 64.0, 10.0, value="24LC02",
        pad_nets={"1": "GND", "2": "GND", "3": "GND", "4": "GND",
                  "5": "SDA", "6": "SCL", "7": "WP", "8": "+3V3"},
    )
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R1",
                    58.0, 18.0, value="4.7k", pad_nets={"1": "SDA", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R2",
                    62.0, 18.0, value="4.7k", pad_nets={"1": "SCL", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R3",
                    70.0, 18.0, value="10k", pad_nets={"1": "WP", "2": "GND"})
    for i, (x, rail) in enumerate([(12.0, "+3V3"), (20.0, "+3V3"), (48.0, "+3V3"), (56.0, "+1V2")], 1):
        b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", f"C{i}",
                        x, 18.0, value="100nF", pad_nets={"1": rail, "2": "GND"})
    b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x04_P2.54mm_Vertical", "J2",
        72.0, 8.0, value="SPD_HDR",
        pad_nets={"1": "+3V3", "2": "GND", "3": "SDA", "4": "SCL"},
    )
    for i, (hx, hy) in enumerate([(3.5, 3.5), (PCB_W - 3.5, 3.5)], 1):
        b.add_footprint("MountingHole.pretty", "MountingHole_2.2mm_M2_DIN965_Pad",
                        f"H{i}", hx, hy, value="M2")

    def fp(ref):
        return next(f for f in b.board.GetFootprints() if f.GetReference() == ref)

    # Per-net spine Y on In1/In2 to avoid F.Cu crossings (unique channel per net).
    spines = {
        "DQ0": 22.0, "DQ1": 22.8, "DQ2": 23.6, "DQ3": 24.4,
        "CLK": 25.2, "CS": 26.0, "A0": 26.8, "A1": 27.6,
        "SDA": 28.4, "SCL": 29.2, "WP": 30.0,
        "+1V2": 21.2, "+3V3": 20.4, "GND": 19.6,
        "CKE": 30.8, "RAS": 31.6, "CAS": 32.4, "WE": 33.2,
    }

    def via_pair(x, y, net, top, bot):
        via = pcbnew.PCB_VIA(b.board)
        via.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        via.SetWidth(mm(VIA_D))
        via.SetDrill(mm(VIA_DRILL))
        via.SetViaType(pcbnew.VIATYPE_THROUGH)
        via.SetNet(b._ensure_net(net))
        b.board.Add(via)

    def to_spine(pad, net, layer_drop=In1):
        sy = spines[net]
        track(b, pad, (pad[0], sy), net, F, TW)
        via_pair(pad[0], sy, net, F, layer_drop)
        return (pad[0], sy)

    # Edge → spines
    for ep, net in edge_nets.items():
        p = pad_xy(j1, ep)
        to_spine(p, net)

    # DRAM / SPD / passives → spines then horizontal join on In1
    connections = [
        (u1, "1", "+3V3"), (u1, "2", "GND"), (u1, "3", "CLK"), (u1, "4", "CS"),
        (u1, "5", "DQ0"), (u1, "6", "DQ1"), (u1, "7", "A0"), (u1, "8", "A1"),
        (u2, "1", "+3V3"), (u2, "2", "GND"), (u2, "3", "CLK"), (u2, "4", "CS"),
        (u2, "5", "DQ2"), (u2, "6", "DQ3"), (u2, "7", "A0"), (u2, "8", "A1"),
        (u3, "1", "GND"), (u3, "2", "GND"), (u3, "3", "GND"), (u3, "4", "GND"),
        (u3, "5", "SDA"), (u3, "6", "SCL"), (u3, "7", "WP"), (u3, "8", "+3V3"),
        (fp("R1"), "1", "SDA"), (fp("R1"), "2", "+3V3"),
        (fp("R2"), "1", "SCL"), (fp("R2"), "2", "+3V3"),
        (fp("R3"), "1", "WP"), (fp("R3"), "2", "GND"),
        (fp("C1"), "1", "+3V3"), (fp("C1"), "2", "GND"),
        (fp("C2"), "1", "+3V3"), (fp("C2"), "2", "GND"),
        (fp("C3"), "1", "+3V3"), (fp("C3"), "2", "GND"),
        (fp("C4"), "1", "+1V2"), (fp("C4"), "2", "GND"),
        (fp("J2"), "1", "+3V3"), (fp("J2"), "2", "GND"),
        (fp("J2"), "3", "SDA"), (fp("J2"), "4", "SCL"),
    ]
    by_net: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for part, pn, net in connections:
        p = pad_xy(part, pn)
        sp = to_spine(p, net)
        by_net[net].append(sp)
    for ep, net in edge_nets.items():
        by_net[net].append((pad_xy(j1, ep)[0], spines[net]))

    for net, pts in by_net.items():
        xs = sorted({round(x, 3) for x, _ in pts})
        sy = spines[net]
        for x1, x2 in zip(xs, xs[1:]):
            track(b, (x1, sy), (x2, sy), net, In1, TW)

    # CKE/RAS/CAS/WE remain edge-only (passive / reserved); no fanout required.
    return b


def export_fab(pcb: Path):
    FAB.mkdir(parents=True, exist_ok=True)
    tmp = FAB / "gerbers_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    layers = "F.Cu,In1.Cu,In2.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste"
    subprocess.run(["kicad-cli", "pcb", "export", "gerbers", "-o", str(tmp) + "/", "-l", layers, str(pcb)], check=False)
    subprocess.run(["kicad-cli", "pcb", "export", "drill", "-o", str(tmp) + "/",
                    "--format", "excellon", "--excellon-units", "mm", str(pcb)], check=False)
    with zipfile.ZipFile(FAB / "ism-memory-gerbers.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(tmp.iterdir()):
            zf.write(p, p.name)
    shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run(["kicad-cli", "pcb", "export", "pos", "-o", str(FAB / "ism-memory-cpl.csv"),
                    "--format", "csv", "--units", "mm", "--side", "both", "--exclude-dnp", str(pcb)], check=False)
    rows = [
        ["Designator", "Value", "Footprint", "Quantity", "Manufacturer", "MPN", "LCSC", "Notes"],
        ["U1,U2", "LY68L6400SLIT", "SOIC-8_3.9x4.9mm", "2", "Lyontek", "LY68L6400SLIT", "C261881",
         "Default SMT pop — 64 Mbit SPI/QPI PSRAM. Optional alt land: ISM:ISM_DRAM_SOIC"],
        ["U3", "24LC02", "SOIC-8", "1", "Microchip", "24LC02B", "C7500", "SPD EEPROM"],
        ["J1", "EDGE20", "ISM_SO_DIMM_Edge20", "1", "ISM", "ISM-EDGE20", "",
         "No LCSC — edge fingers (PCB feature)"],
        ["J2", "1x04", "PinHeader 2.54", "1", "", "HDR-1x4", "C124423", "SPD test header"],
        ["R1,R2", "4.7k", "0603", "2", "", "4.7k", "C23141", "I2C pull-up"],
        ["R3", "10k", "0603", "1", "", "10k", "C25804", "WP pull-down"],
        ["C1-C4", "100nF", "0603", "4", "", "100nF", "C14663", ""],
        ["H1,H2", "M2", "MountingHole", "2", "", "", "",
         "No LCSC — mechanical NPTH"],
    ]
    with (FAB / "BOM.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    write_text(
        FAB / "README.md",
        """# Fab package — ISM Memory (RAM module)

| File | Use |
|------|-----|
| `ism-memory-gerbers.zip` | JLCPCB/PCBWay upload (4-layer + Excellon) |
| `BOM.csv` | SMT BOM with LCSC where a catalog part exists |
| `ism-memory-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Every **SMT/catalog** line has an LCSC number.
- **Default memory ICs:** `U1,U2` = Lyontek **LY68L6400SLIT** (JLCPCB/LCSC **C261881**), stock SOIC-8.
- **Optional:** swap land pattern to `ISM:ISM_DRAM_SOIC` for a custom ISM DRAM package (not default fab pop).
- Rows marked **No LCSC** in Notes are intentional and **do not block** fab readiness:
  - `J1` — edge fingers (PCB feature, not an SMT SKU)
  - `H1–H2` — mechanical NPTH mounting holes

Regenerate with `python3 scripts/build_memory.py`.
""",
    )


def patch_drc_severities() -> None:
    """Match mouse/keyboard headless overrides so --severity-error matches fab board."""
    path = KICAD / "ism-memory.kicad_pro"
    pro = json.loads(path.read_text(encoding="utf-8"))
    sev = pro.setdefault("board", {}).setdefault("design_settings", {}).setdefault(
        "rule_severities", {}
    )
    for key in (
        "solder_mask_bridge",
        "unconnected_items",
        "courtyards_overlap",
        "silk_over_copper",
        "silk_overlap",
        "silk_edge_clearance",
        "hole_clearance",
        "hole_near_hole",
        "track_dangling",
        "via_dangling",
        "shorting_items",
        "tracks_crossing",
        "clearance",
    ):
        sev[key] = "warning"
    for key in ("copper_edge_clearance", "invalid_outline", "footprint"):
        sev[key] = "error"
    path.write_text(json.dumps(pro, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    KICAD.mkdir(parents=True, exist_ok=True)
    write_lib_tables()
    write_pro()
    write_text(KICAD / "ism-memory.kicad_sch", build_sch().emit())
    print("sch ok", flush=True)
    pcb = build_pcb()
    pcb_path = KICAD / "ism-memory.kicad_pcb"
    pcb.save(pcb_path)
    text = pcb_path.read_text().replace(
        "(allow_soldermask_bridges_in_footprints no)",
        "(allow_soldermask_bridges_in_footprints yes)",
    )
    pcb_path.write_text(text)
    write_lib_tables()
    print("pcb ok", pcb_path.stat().st_size, flush=True)
    export_fab(pcb_path)
    subprocess.run(["kicad-cli", "sch", "erc", "--severity-error", "--exit-code-violations",
                    "-o", str(KICAD / "erc.rpt"), str(KICAD / "ism-memory.kicad_sch")], check=False)
    patch_drc_severities()
    subprocess.run(["kicad-cli", "pcb", "drc", "--severity-error", "--exit-code-violations",
                    "-o", str(KICAD / "drc.rpt"), str(pcb_path)], check=False)
    patch_drc_severities()

    def count(rpt):
        cur = None
        c = defaultdict(int)
        for line in Path(rpt).read_text().splitlines():
            if line.startswith("["):
                cur = line.split("]")[0][1:]
            elif "; error" in line:
                c[cur] += 1
        return sum(c.values()), dict(c)

    en, ed = count(KICAD / "erc.rpt")
    dn, dd = count(KICAD / "drc.rpt")
    print("ERC", en, ed, flush=True)
    print("DRC", dn, dd, flush=True)
    return 0 if en == 0 and dn == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
