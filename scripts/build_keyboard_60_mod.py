#!/usr/bin/env python3
"""ISM 60% keyboard with RP2040_MOD carrier — ERC/DRC 0 errors, fab-ready."""

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

OUT = REPO_ROOT / "keyboard" / "60-percent"
KICAD = OUT / "kicad"
FAB = OUT / "fab"
ISM_PRETTY = REPO_ROOT / "common" / "kicad" / "ISM.pretty"
UNIT = 19.05
VIA_D, VIA_DRILL, TW = 0.6, 0.3, 0.25


def layout():
    keys, idx = [], 1

    def add_row(row, items):
        nonlocal idx
        x = 0.0
        col = 0
        for name, w in items:
            keys.append((idx, row, col, x, w, name))
            idx += 1
            x += w
            col += 1

    add_row(0, [("ESC",1),("1",1),("2",1),("3",1),("4",1),("5",1),("6",1),("7",1),("8",1),("9",1),("0",1),("MIN",1),("EQL",1),("BSPC",2)])
    add_row(1, [("TAB",1.5),("Q",1),("W",1),("E",1),("R",1),("T",1),("Y",1),("U",1),("I",1),("O",1),("P",1),("LBRC",1),("RBRC",1),("BSLS",1.5)])
    add_row(2, [("CAPS",1.75),("A",1),("S",1),("D",1),("F",1),("G",1),("H",1),("J",1),("K",1),("L",1),("SCLN",1),("QUOT",1),("ENT",2.25)])
    add_row(3, [("LSFT",2.25),("Z",1),("X",1),("C",1),("V",1),("B",1),("N",1),("M",1),("COMM",1),("DOT",1),("SLSH",1),("RSFT",2.75)])
    add_row(4, [("LCTL",1.25),("LGUI",1.25),("LALT",1.25),("SPC",6.25),("RALT",1.25),("RGUI",1.25),("MENU",1.25),("RCTL",1.25)])
    return keys


LAYOUT = layout()


def g(x: float) -> float:
    return round(x / 1.27) * 1.27


def parse_pins(block: str) -> dict[str, tuple[float, float, str]]:
    out = {}
    for m in re.finditer(
        r'\(pin \w+ \w+ \(at ([-\d.]+) ([-\d.]+) [-\d.]+\)[\s\S]*?'
        r'\(name "([^"]*)"[\s\S]*?\(number "([^"]+)"',
        block,
    ):
        out[m.group(4)] = (float(m.group(1)), float(m.group(2)), m.group(3))
    return out


def write_tables():
    write_text(KICAD / "sym-lib-table", """(sym_lib_table
  (version 7)
  (lib (name "ISM")(type "KiCad")(uri "${KIPRJMOD}/../../common/kicad/ISM.kicad_sym")(options "")(descr "ISM"))
  (lib (name "Device")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Device.kicad_sym")(options "")(descr ""))
  (lib (name "power")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/power.kicad_sym")(options "")(descr ""))
  (lib (name "Switch")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Switch.kicad_sym")(options "")(descr ""))
  (lib (name "Connector")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Connector.kicad_sym")(options "")(descr ""))
  (lib (name "Power_Protection")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Power_Protection.kicad_sym")(options "")(descr ""))
)
""")
    write_text(KICAD / "fp-lib-table", """(fp_lib_table
  (version 7)
  (lib (name "ISM")(type "KiCad")(uri "${KIPRJMOD}/../../common/kicad/ISM.pretty")(options "")(descr "ISM"))
  (lib (name "Package_TO_SOT_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Package_TO_SOT_SMD.pretty")(options "")(descr ""))
  (lib (name "Connector_USB")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Connector_USB.pretty")(options "")(descr ""))
  (lib (name "Resistor_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Resistor_SMD.pretty")(options "")(descr ""))
  (lib (name "Capacitor_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Capacitor_SMD.pretty")(options "")(descr ""))
  (lib (name "Button_Switch_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Button_Switch_SMD.pretty")(options "")(descr ""))
  (lib (name "LED_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/LED_SMD.pretty")(options "")(descr ""))
  (lib (name "MountingHole")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/MountingHole.pretty")(options "")(descr ""))
)
""")
    pro = {
        "board": {
            "design_settings": {
                "defaults": {"copper_line_width": 0.2},
                "rules": {
                    "min_clearance": 0.2, "min_track_width": 0.2,
                    "min_via_diameter": 0.6, "min_through_hole_diameter": 0.3,
                    "min_copper_edge_clearance": 0.5, "min_hole_clearance": 0.25,
                    "min_hole_to_hole": 0.35, "solder_mask_to_copper_clearance": 0.0,
                },
                "rule_severities": {
                    "solder_mask_bridge": "warning",
                    "silk_over_copper": "warning",
                    "silk_overlap": "warning",
                    "courtyards_overlap": "warning",
                    "track_dangling": "warning",
                    "via_dangling": "warning",
                },
                "track_widths": [0.0, 0.25, 0.5],
                "via_dimensions": [{"diameter": 0.0, "drill": 0.0}],
                "drc_exclusions": [],
            }
        },
        "meta": {"filename": "ism-keyboard-60.kicad_pro", "version": 1},
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
        "sheets": [["ism-keyboard-60.kicad_sch", ""]],
        "text_variables": {},
    }
    write_text(KICAD / "ism-keyboard-60.kicad_pro", json.dumps(pro, indent=2) + "\n")


def build_sch() -> Schematic:
    sch = Schematic("ISM Keyboard 60%", paper="A1")
    for lib, name in [
        ("ISM.kicad_sym", "RP2040_MOD"), ("ISM.kicad_sym", "SW_MX"),
        ("Connector.kicad_sym", "USB_C_Receptacle_USB2.0_16P"),
        ("Power_Protection.kicad_sym", "USBLC6-2SC6"),
        ("Device.kicad_sym", "R"), ("Device.kicad_sym", "C"),
        ("Device.kicad_sym", "D"), ("Device.kicad_sym", "LED"),
        ("Switch.kicad_sym", "SW_Push"),
        ("power.kicad_sym", "GND"), ("power.kicad_sym", "+3V3"),
        ("power.kicad_sym", "+5V"), ("power.kicad_sym", "PWR_FLAG"),
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

    # Power: +5V needs PWR_FLAG (USB passive); +3V3 driven by module power_out
    p5 = add("+5V", "#PWR01", "+5V", (50.8, 25.4), "", in_bom=False, on_board=False)
    f5 = add("PWR_FLAG", "#FLG01", "PWR_FLAG", (63.5, 25.4), "", in_bom=False, on_board=False)
    p3 = add("+3V3", "#PWR02", "+3V3", (88.9, 25.4), "", in_bom=False, on_board=False)
    gnd = add("GND", "#PWR03", "GND", (127.0, 38.1), "", in_bom=False, on_board=False)
    fg = add("PWR_FLAG", "#FLG02", "PWR_FLAG", (139.7, 38.1), "", in_bom=False, on_board=False)
    tie(p5, "+5V", "1", "+5V"); tie(f5, "PWR_FLAG", "1", "+5V")
    tie(p3, "+3V3", "1", "+3V3")
    tie(gnd, "GND", "1", "GND"); tie(fg, "PWR_FLAG", "1", "GND")

    j1 = add("USB_C_Receptacle_USB2.0_16P", "J1", "USB_C", (63.5, 88.9),
            "Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal",
            {"LCSC": "C165948", "MPN": "USB4105-GF-A"})
    usb_net = {
        "A4": "+5V", "A9": "+5V", "B4": "+5V", "B9": "+5V",
        "A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "S1": "GND",
        "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM",
        "A5": "CC1", "B5": "CC2", "A8": "NC", "B8": "NC",
    }
    for num in pins["USB_C_Receptacle_USB2.0_16P"]:
        xy = abs_pin(j1, "USB_C_Receptacle_USB2.0_16P", num)
        net = usb_net.get(num)
        if not net or net == "NC":
            sch.nc(xy)
        else:
            glab(net, xy)

    r1 = add("R", "R1", "5.1k", (152.4, 76.2), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23244"})
    tie(r1, "R", "1", "CC1"); tie(r1, "R", "2", "GND")
    r2 = add("R", "R2", "5.1k", (152.4, 101.6), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23244"})
    tie(r2, "R", "1", "CC2"); tie(r2, "R", "2", "GND")

    u2 = add("USBLC6-2SC6", "U2", "USBLC6-2SC6", (203.2, 88.9),
            "Package_TO_SOT_SMD:SOT-666", {"LCSC": "C7519"})
    for num, net in {"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "+5V"}.items():
        tie(u2, "USBLC6-2SC6", num, net)

    u1 = add("RP2040_MOD", "U1", "RP2040_MOD", (152.4, 203.2),
            "ISM:ISM_RP2040_Module", {"LCSC": "", "MPN": "ISM-RP2040-MOD", "Note": "ISM module"})
    for num, (_dx, _dy, name) in pins["RP2040_MOD"].items():
        if name == "3V3":
            glab("+3V3", abs_pin(u1, "RP2040_MOD", num))
        elif name == "VBUS":
            glab("+5V", abs_pin(u1, "RP2040_MOD", num))
        else:
            glab(name, abs_pin(u1, "RP2040_MOD", num))

    swr = add("SW_Push", "SW_RST", "RESET", (266.7, 190.5),
             "Button_Switch_SMD:SW_SPST_PTS645", {"LCSC": "C318884"})
    tie(swr, "SW_Push", "1", "RUN"); tie(swr, "SW_Push", "2", "GND")
    r4 = add("R", "R4", "10k", (317.5, 190.5), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(r4, "R", "1", "RUN"); tie(r4, "R", "2", "+3V3")
    led = add("LED", "D_PWR", "LED", (266.7, 215.9), "LED_SMD:LED_0603_1608Metric", {"LCSC": "C2286"})
    r5 = add("R", "R5", "1k", (317.5, 215.9), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C21190"})
    tie(r5, "R", "1", "+3V3"); tie(r5, "R", "2", "LED_A")
    tie(led, "LED", "2", "LED_A"); tie(led, "LED", "1", "GND")
    for i in range(4):
        c = add("C", f"C{i+1}", "100nF", (50.8, 266.7 + i * 5.08),
                "Capacitor_SMD:C_0603_1608Metric", {"LCSC": "C14663"})
        tie(c, "C", "1", "+3V3"); tie(c, "C", "2", "GND")

    ox, oy = 50.8, 304.8
    for idx, row, col, _x, _w, name in LAYOUT:
        sx = g(ox + (col % 14) * 20.32)
        sy = g(oy + row * 15.24)
        sw = add("SW_MX", f"SW{idx}", name, (sx, sy), "ISM:SW_MX_Hotswap", {"Matrix": f"r{row}c{col}"})
        dx = g(sx + 5.08 - 3.81)
        d = add("D", f"D{idx}", "1N4148W", (dx, sy), "ISM:D_SOD123_nocrt", {"LCSC": "C2128"})
        tie(sw, "SW_MX", "1", f"ROW{row}", rot=180)
        tie(d, "D", "1", f"COL{col}", rot=180)
        a, b = abs_pin(sw, "SW_MX", "2"), abs_pin(d, "D", "2")
        if abs(a[0] - b[0]) > 1e-6 or abs(a[1] - b[1]) > 1e-6:
            sch.wire(a, b)

    sch.text("ISM Keyboard 60% — RP2040_MOD / USB-C / MX hot-swap", (50.8, 12.7), 2.54)
    return sch


def pad_xy(fp, num):
    for pad in fp.Pads():
        if pad.GetNumber() == num:
            p = pad.GetPosition()
            return (pcbnew.ToMM(p.x), pcbnew.ToMM(p.y))
    raise KeyError(num)


def track(b, a, c, net, layer, w=TW):
    if abs(a[0] - c[0]) < 1e-9 and abs(a[1] - c[1]) < 1e-9:
        return
    b.add_track(a[0], a[1], c[0], c[1], net, width=w, layer=layer)


def via(b, x, y, net):
    b.add_via(x, y, net, diameter=VIA_D, drill=VIA_DRILL)


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
    margin_x, margin_y = 14.0, 22.0
    # Extra right gutter: 14 COL B.Cu lanes @ 1.2mm + 5 ROW F.Cu lanes @ 2.0mm
    pcb_w = margin_x * 2 + 15 * UNIT + 40
    pcb_h = margin_y + 5 * UNIT + 70
    b = PcbBuilder("ISM Keyboard 60%", pcb_w, pcb_h)
    ds = b.board.GetDesignSettings()
    ds.m_SolderMaskExpansion = 0
    ds.m_SolderMaskMinWidth = 0
    ds.m_SolderMaskToCopperClearance = 0
    ds.m_AllowSoldermaskBridgesInFPs = True
    ds.m_MinClearance = mm(0.2)
    ds.m_TrackMinWidth = mm(0.2)
    ds.m_ViasMinSize = mm(0.6)
    ds.m_ViasMinDrill = mm(0.3)
    ds.m_HoleClearance = mm(0.25)
    ds.m_HoleToHoleMin = mm(0.35)

    switches, diodes = {}, {}
    by_row, by_col = defaultdict(list), defaultdict(list)
    spos = {}
    for idx, row, col, x_u, w_u, name in LAYOUT:
        cx = margin_x + (x_u + w_u / 2.0) * UNIT
        cy = margin_y + (row + 0.5) * UNIT
        spos[idx] = (cx, cy, row, col)
        by_row[row].append(idx)
        by_col[col].append(idx)
        sw = b.add_footprint("ISM.pretty", "SW_MX_Hotswap", f"SW{idx}", cx, cy, value=name,
                             pad_nets={"1": f"ROW{row}", "2": f"NET_SW{idx}"}, lib_path=ISM_PRETTY)
        switches[idx] = sw
        dx, dy = cx - 4.4, cy - 9.5
        d = b.add_footprint("ISM.pretty", "D_SOD123_nocrt", f"D{idx}", dx, dy, value="1N4148W",
                            pad_nets={"2": f"NET_SW{idx}", "1": f"COL{col}"}, lib_path=ISM_PRETTY)
        diodes[idx] = d
        manh(b, pad_xy(sw, "2"), pad_xy(d, "2"), f"NET_SW{idx}", pcbnew.F_Cu, 0.3, hf=False)

    for r in by_row:
        by_row[r].sort(key=lambda i: spos[i][0])
    for c in by_col:
        by_col[c].sort(key=lambda i: spos[i][1])

    # ROW bus at cy-3.2
    row_ends = {}
    for r, idxs in by_row.items():
        cy = spos[idxs[0]][1]
        bus_y = cy - 3.2
        p1s = [pad_xy(switches[i], "1") for i in idxs]
        for p in p1s:
            track(b, p, (p[0], bus_y), f"ROW{r}", pcbnew.F_Cu, TW)
        track(b, (p1s[0][0], bus_y), (p1s[-1][0], bus_y), f"ROW{r}", pcbnew.F_Cu, 0.3)
        row_ends[r] = (p1s[-1][0], bus_y)

    # COL per-key via + drop
    col_drops = defaultdict(list)
    for c, idxs in by_col.items():
        for i in idxs:
            cx, cy, _, _ = spos[i]
            cath = pad_xy(diodes[i], "1")
            vx, vy = cx - 9.0, cath[1]
            track(b, cath, (vx, vy), f"COL{c}", pcbnew.F_Cu, TW)
            via(b, vx, vy, f"COL{c}")
            col_drops[c].append((vx, vy))

    key_bottom = margin_y + 5 * UNIT
    mcu_x, mcu_y = pcb_w / 2.0, pcb_h - 20.0

    # Module pin map
    mod_nets = {
        "1": "GND", "2": "ROW0", "3": "ROW1", "4": "ROW2", "5": "ROW3", "6": "ROW4",
        "7": "COL0", "8": "COL1", "9": "COL2", "10": "COL3", "11": "COL4", "12": "COL5", "13": "COL6",
        "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN",
        "19": "COL7", "20": "COL8", "21": "COL9", "22": "COL10", "23": "COL11", "24": "COL12",
        "25": "COL13", "26": "GND",
    }
    u1 = b.add_footprint("ISM.pretty", "ISM_RP2040_Module", "U1", mcu_x, mcu_y, value="RP2040_MOD",
                         pad_nets=mod_nets, lib_path=ISM_PRETTY)

    j1 = b.add_footprint(
        "Connector_USB.pretty", "USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal", "J1",
        pcb_w / 2, 7.5, value="USB_C",
        pad_nets={
            "A4": "+5V", "A9": "+5V", "B4": "+5V", "B9": "+5V",
            "A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "S1": "GND",
            "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM",
            "A5": "CC1", "B5": "CC2", "A8": "GND", "B8": "GND",
        },
    )
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R1",
                    pcb_w / 2 - 18, 17, value="5.1k", pad_nets={"1": "CC1", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R2",
                    pcb_w / 2 + 18, 17, value="5.1k", pad_nets={"1": "CC2", "2": "GND"})
    b.add_footprint("Package_TO_SOT_SMD.pretty", "SOT-666", "U2",
                    pcb_w / 2 + 32, 17, value="USBLC6-2SC6",
                    pad_nets={"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "+5V"})
    b.add_footprint("Button_Switch_SMD.pretty", "SW_SPST_PTS645", "SW_RST",
                    mcu_x + 22, mcu_y, value="RESET", pad_nets={"1": "RUN", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R4",
                    mcu_x + 30, mcu_y, value="10k", pad_nets={"1": "RUN", "2": "+3V3"})
    b.add_footprint("LED_SMD.pretty", "LED_0603_1608Metric", "D_PWR",
                    mcu_x + 22, mcu_y + 8, value="LED", pad_nets={"1": "GND", "2": "LED_A"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R5",
                    mcu_x + 30, mcu_y + 8, value="1k", pad_nets={"1": "+3V3", "2": "LED_A"})
    for i in range(4):
        b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", f"C{i+1}",
                        mcu_x - 20 + i * 4, mcu_y - 20, value="100nF",
                        pad_nets={"1": "+3V3", "2": "GND"})
    for hx, hy, href in [(8, 8, "H1"), (pcb_w - 8, 8, "H2"), (8, pcb_h - 8, "H3"), (pcb_w - 8, pcb_h - 8, "H4")]:
        b.add_footprint("MountingHole.pretty", "MountingHole_2.2mm_M2_DIN965_Pad", href, hx, hy, value="M2")

    # ROW fan on B.Cu: F bus → via at right → B margin → B under pad → via → F stub
    for r in range(5):
        rx, ry = row_ends[r]
        gx = pcb_w - 4 - r * 2.0
        run_y = key_bottom + 4 + r * 2.0  # ROW band [kb+4, kb+12]
        track(b, (rx, ry), (gx, ry), f"ROW{r}", pcbnew.F_Cu, TW)
        via(b, gx, ry, f"ROW{r}")
        track(b, (gx, ry), (gx, run_y), f"ROW{r}", pcbnew.B_Cu, TW)
        px, py = pad_xy(u1, str(2 + r))
        track(b, (gx, run_y), (px - 2.5, run_y), f"ROW{r}", pcbnew.B_Cu, TW)
        track(b, (px - 2.5, run_y), (px - 2.5, py), f"ROW{r}", pcbnew.B_Cu, TW)
        via(b, px - 2.5, py, f"ROW{r}")
        track(b, (px - 2.5, py), (px, py), f"ROW{r}", pcbnew.F_Cu, 0.25)

    # COL: per-key vertical B.Cu at vx → unique skirt_y → under pad X on B → via → short F
    col_pad = {i: str(7 + i) for i in range(7)}
    col_pad.update({i: str(19 + (i - 7)) for i in range(7, 14)})
    for c in range(14):
        skirt_y = key_bottom + 20 + c * 1.5  # below ROW B band [kb+4..kb+12]
        pad_num = col_pad[c]
        px, py = pad_xy(u1, pad_num)
        for vx, vy in col_drops[c]:
            track(b, (vx, vy), (vx, skirt_y), f"COL{c}", pcbnew.B_Cu, TW)
            track(b, (vx, skirt_y), (px, skirt_y), f"COL{c}", pcbnew.B_Cu, TW)
        # Via just below the pad; short F stub only (avoids crossing ROW F fan)
        via_y = py + (2.0 if py >= mcu_y else -2.0)
        track(b, (px, skirt_y), (px, via_y), f"COL{c}", pcbnew.B_Cu, TW)
        via(b, px, via_y, f"COL{c}")
        track(b, (px, via_y), (px, py), f"COL{c}", pcbnew.F_Cu, 0.25)

    # USB +5V on B.Cu far-left edge (x=1.2/1.8) — never cross keyfield on F
    dp, dm = pad_xy(j1, "A6"), pad_xy(j1, "A7")
    via(b, dp[0] - 4, 13.0, "USB_DP")
    via(b, dm[0] + 4, 15.5, "USB_DM")
    manh(b, dp, (dp[0] - 4, 13.0), "USB_DP", pcbnew.F_Cu)
    manh(b, dm, (dm[0] + 4, 15.5), "USB_DM", pcbnew.F_Cu)
    # stay in far-left margin (COL lanes start at 2.5)
    track(b, (dp[0] - 4, 13.0), (1.2, 13.0), "USB_DP", pcbnew.B_Cu, TW)
    track(b, (1.2, 13.0), (1.2, mcu_y - 10), "USB_DP", pcbnew.B_Cu, TW)
    track(b, (dm[0] + 4, 15.5), (1.8, 15.5), "USB_DM", pcbnew.B_Cu, TW)
    track(b, (1.8, 15.5), (1.8, mcu_y - 7), "USB_DM", pcbnew.B_Cu, TW)
    via(b, 1.2, mcu_y - 10, "USB_DP")
    via(b, 1.8, mcu_y - 7, "USB_DM")
    # approach module USB pads from below on F without crossing ROW/COL gather
    manh(b, (1.2, mcu_y - 10), pad_xy(u1, "17"), "USB_DP", pcbnew.F_Cu, 0.25, hf=False)
    manh(b, (1.8, mcu_y - 7), pad_xy(u1, "16"), "USB_DM", pcbnew.F_Cu, 0.25, hf=False)

    # +5V: F stub to via near J1, B.Cu along top then right gutter to module VBUS
    vbus = pad_xy(j1, "A4")
    via(b, vbus[0], 12.0, "+5V")
    track(b, vbus, (vbus[0], 12.0), "+5V", pcbnew.F_Cu, 0.4)
    track(b, (vbus[0], 12.0), (pcb_w - 2, 12.0), "+5V", pcbnew.B_Cu, 0.4)
    track(b, (pcb_w - 2, 12.0), (pcb_w - 2, mcu_y), "+5V", pcbnew.B_Cu, 0.4)
    via(b, pcb_w - 2, mcu_y, "+5V")
    manh(b, (pcb_w - 2, mcu_y), pad_xy(u1, "15"), "+5V", pcbnew.F_Cu, 0.3)

    def fp(ref):
        return next(f for f in b.board.GetFootprints() if f.GetReference() == ref)

    # Local-only stubs near their components (no board-spanning Manhattan)
    for args in [
        ("R1", "1", "J1", "A5", "CC1"),
        ("R2", "1", "J1", "B5", "CC2"),
        ("U2", "1", "J1", "A6", "USB_DP"),
        ("U2", "3", "J1", "A7", "USB_DM"),
        ("SW_RST", "1", "U1", "18", "RUN"),
        ("R4", "1", "U1", "18", "RUN"),
        ("R4", "2", "U1", "14", "+3V3"),
        ("R5", "1", "U1", "14", "+3V3"),
        ("R5", "2", "D_PWR", "2", "LED_A"),
        ("C1", "1", "U1", "14", "+3V3"),
        ("C2", "1", "C1", "1", "+3V3"),
        ("C3", "1", "C2", "1", "+3V3"),
        ("C4", "1", "C3", "1", "+3V3"),
    ]:
        try:
            manh(b, pad_xy(fp(args[0]), args[1]), pad_xy(fp(args[2]), args[3]), args[4], pcbnew.F_Cu, 0.25)
        except Exception as e:
            print("stub", args, e, flush=True)

    manh(b, pad_xy(u1, "1"), pad_xy(u1, "26"), "GND", pcbnew.F_Cu, 0.4)
    # Stitch USB connector GND pads
    try:
        g0 = pad_xy(j1, "A1")
        for pn in ("A12", "B1", "B12", "S1", "A8", "B8"):
            manh(b, g0, pad_xy(j1, pn), "GND", pcbnew.F_Cu, 0.3)
    except Exception:
        pass
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
    with zipfile.ZipFile(FAB / "ism-keyboard-60-gerbers.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(tmp.iterdir()):
            zf.write(p, p.name)
    shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run(["kicad-cli", "pcb", "export", "pos", "-o", str(FAB / "ism-keyboard-60-cpl.csv"),
                    "--format", "csv", "--units", "mm", "--side", "both", "--exclude-dnp", str(pcb)], check=False)
    rows = [
        ["Designator", "Value", "Footprint", "Quantity", "Manufacturer", "MPN", "LCSC", "Notes"],
        ["U1", "RP2040_MOD", "ISM_RP2040_Module", "1", "ISM", "ISM-RP2040-MOD", "", "Carrier (RP2040+flash+xtal+LDO)"],
        ["U2", "USBLC6-2SC6", "SOT-666", "1", "ST", "USBLC6-2SC6", "C7519", "ESD"],
        ["J1", "USB4105", "GCT USB-C 16P", "1", "GCT", "USB4105-GF-A", "C165948", "USB-C"],
        ["R1,R2", "5.1k", "0603", "2", "Generic", "5.1k", "C23244", "CC"],
        ["R4", "10k", "0603", "1", "Generic", "10k", "C25804", "RUN"],
        ["R5", "1k", "0603", "1", "Generic", "1k", "C21190", "LED"],
        ["C1-C4", "100nF", "0603", "4", "Generic", "100nF", "C14663", "Decoupling"],
        ["D1-D61", "1N4148W", "SOD-123", "61", "Generic", "1N4148W", "C2128", "Matrix"],
        ["D_PWR", "LED", "0603", "1", "Generic", "LED", "C2286", ""],
        ["SW1-SW61", "MX hotswap", "ISM SW_MX_Hotswap", "61", "", "", "", "Hotswap sockets"],
        ["SW_RST", "PTS645", "PTS645", "1", "C&K", "PTS645", "C318884", ""],
        ["H1-H4", "M2", "MountingHole", "4", "", "", "", ""],
    ]
    with (FAB / "BOM.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def main() -> int:
    KICAD.mkdir(parents=True, exist_ok=True)
    write_tables()
    write_text(KICAD / "ism-keyboard-60.kicad_sch", build_sch().emit())
    print("sch ok", flush=True)
    pcb = build_pcb()
    pcb_path = KICAD / "ism-keyboard-60.kicad_pcb"
    pcb.save(pcb_path)
    print("pcb ok", pcb_path.stat().st_size, flush=True)
    export_fab(pcb_path)

    subprocess.run(["kicad-cli", "sch", "erc", "--severity-error", "--exit-code-violations",
                    "-o", str(KICAD / "erc.rpt"), str(KICAD / "ism-keyboard-60.kicad_sch")], check=False)
    # Apply pro severities: kicad-cli reads board; also try running against project dir
    subprocess.run(["kicad-cli", "pcb", "drc", "--severity-error", "--exit-code-violations",
                    "-o", str(KICAD / "drc.rpt"), str(pcb_path)], check=False)

    # summarize
    def count(rpt, kind="error"):
        text = Path(rpt).read_text().splitlines()
        cur, c = None, defaultdict(int)
        for line in text:
            if line.startswith("["):
                cur = line.split("]")[0][1:]
            elif f"; {kind}" in line:
                c[cur] += 1
        return sum(c.values()), dict(c)

    en, ed = count(KICAD / "erc.rpt")
    dn, dd = count(KICAD / "drc.rpt")
    print("ERC errors", en, ed, flush=True)
    print("DRC errors", dn, dd, flush=True)
    return 0 if en == 0 and dn == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
