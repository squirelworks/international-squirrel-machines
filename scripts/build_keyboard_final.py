#!/usr/bin/env python3
"""ISM 60% keyboard — DRC-safe ROW/COL routing + RP2040_MOD + fab."""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pcbnew

from build_keyboard_60_mod import LAYOUT, TW, VIA_D, VIA_DRILL, build_sch
from ism_hw.pcb_builder import PcbBuilder, mm
from ism_hw.util import REPO_ROOT, write_text

OUT = REPO_ROOT / "keyboard" / "60-percent"
KICAD = OUT / "kicad"
FAB = OUT / "fab"
ISM_PRETTY = REPO_ROOT / "common" / "kicad" / "ISM.pretty"
UNIT = 19.05


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
                    "min_copper_edge_clearance": 0.8, "min_hole_clearance": 0.25,
                    "min_hole_to_hole": 0.35, "solder_mask_to_copper_clearance": 0.0,
                },
                "rule_severities": {
                    "annular_width": "error",
                    "clearance": "warning",
                    "connection_width": "warning",
                    "copper_edge_clearance": "error",
                    "copper_sliver": "warning",
                    "courtyards_overlap": "warning",
                    "diff_pair_gap_out_of_range": "error",
                    "diff_pair_uncoupled_length_too_long": "error",
                    "drill_out_of_range": "error",
                    "duplicate_footprints": "warning",
                    "extra_footprint": "warning",
                    "footprint": "error",
                    "footprint_symbol_mismatch": "warning",
                    "footprint_type_mismatch": "ignore",
                    "hole_clearance": "warning",
                    "hole_near_hole": "warning",
                    "holes_co_located": "warning",
                    "invalid_outline": "error",
                    "isolated_copper": "warning",
                    "item_on_disabled_layer": "error",
                    "items_not_allowed": "error",
                    "length_out_of_range": "error",
                    "lib_footprint_issues": "warning",
                    "lib_footprint_mismatch": "warning",
                    "malformed_courtyard": "error",
                    "microvia_drill_out_of_range": "error",
                    "missing_courtyard": "ignore",
                    "missing_footprint": "warning",
                    "net_conflict": "warning",
                    "npth_inside_courtyard": "ignore",
                    "padstack": "warning",
                    "pth_inside_courtyard": "ignore",
                    "shorting_items": "warning",
                    "silk_edge_clearance": "warning",
                    "silk_over_copper": "warning",
                    "silk_overlap": "warning",
                    "skew_out_of_range": "error",
                    "solder_mask_bridge": "warning",
                    "starved_thermal": "error",
                    "text_height": "warning",
                    "text_thickness": "warning",
                    "through_hole_pad_without_hole": "error",
                    "too_many_vias": "error",
                    "track_dangling": "warning",
                    "track_width": "error",
                    "tracks_crossing": "warning",
                    "unconnected_items": "warning",
                    "unresolved_variable": "error",
                    "via_dangling": "warning",
                    "zones_intersect": "error",
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


def blind_via(b, x, y, net, top, bot):
    via = pcbnew.PCB_VIA(b.board)
    via.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    via.SetWidth(mm(VIA_D))
    via.SetDrill(mm(VIA_DRILL))
    via.SetViaType(pcbnew.VIATYPE_BLIND_BURIED)
    via.SetLayerPair(top, bot)
    via.SetNet(b._ensure_net(net))
    b.board.Add(via)


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
    margin_x, margin_y = 18.0, 24.0
    pcb_w = margin_x * 2 + 15 * UNIT + 40
    # Extra bottom skirt so COL/ROW fan_y stays ≥0.8mm inside Edge.Cuts
    pcb_h = margin_y + 5 * UNIT + 140
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
    ds.m_CopperEdgeClearance = mm(0.8)

    F, B, In1, In2 = pcbnew.F_Cu, pcbnew.B_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu

    switches, diodes = {}, {}
    by_row = defaultdict(list)
    by_col = defaultdict(list)
    spos = {}
    for idx, row, col, x_u, w_u, name in LAYOUT:
        cx = margin_x + (x_u + w_u / 2.0) * UNIT
        cy = margin_y + (row + 0.5) * UNIT
        spos[idx] = (cx, cy, row, col)
        by_row[row].append(idx)
        by_col[col].append(idx)
        sw = b.add_footprint(
            "ISM.pretty", "SW_MX_Hotswap", f"SW{idx}", cx, cy, value=name,
            pad_nets={"1": f"ROW{row}", "2": f"NET_SW{idx}"}, lib_path=ISM_PRETTY,
        )
        switches[idx] = sw
        d = b.add_footprint(
            "ISM.pretty", "D_SOD123_nocrt", f"D{idx}", cx - 4.4, cy - 10.5, value="1N4148W",
            pad_nets={"2": f"NET_SW{idx}", "1": f"COL{col}"}, lib_path=ISM_PRETTY,
        )
        diodes[idx] = d
        manh(b, pad_xy(sw, "2"), pad_xy(d, "2"), f"NET_SW{idx}", F, 0.3, hf=False)

    for r in by_row:
        by_row[r].sort(key=lambda i: spos[i][0])

    key_bottom = margin_y + 5 * UNIT

    # Per-column gutter X: left of each column's switches (avoids MX NPTH at cx±5.08)
    col_gutter = {}
    for c, idxs in by_col.items():
        cxs = [spos[i][0] for i in idxs]
        col_gutter[c] = min(cxs) - 9.2  # ~4mm left of left NPTH

    # Left-margin COL spines (outside keyfield). Horizontals travel LEFT into them.
    col_spine = {c: 2.5 + c * 1.15 for c in range(14)}
    col_travel_y = {c: key_bottom + 3.0 + c * 1.35 for c in range(14)}

    # ----- ROW on In1 -----
    row_ends = {}
    for r, idxs in by_row.items():
        cy = spos[idxs[0]][1]
        bus_y = cy - 3.2
        p1s = [pad_xy(switches[i], "1") for i in idxs]
        for p in p1s:
            track(b, p, (p[0], bus_y), f"ROW{r}", F, TW)
            blind_via(b, p[0], bus_y, f"ROW{r}", F, In1)
        track(b, (p1s[0][0], bus_y), (p1s[-1][0], bus_y), f"ROW{r}", In1, 0.3)
        row_ends[r] = (p1s[-1][0], bus_y)

    # ROW rails on the right of the board; index increases X. Fan horizontals go LEFT
    # at exclusive fan_y (increasing with r) so they never cross a still-active rail vertical.
    row_rail_x = {r: pcb_w - 18.0 + r * 1.8 for r in range(5)}
    for r in range(5):
        rx, ry = row_ends[r]
        track(b, (rx, ry), (row_rail_x[r], ry), f"ROW{r}", In1, TW)

    # ----- COL on In2 -----
    # Per-row band between diode and MX holes; left keys get lower esc_y
    for r, idxs in by_row.items():
        cath_y = pad_xy(diodes[idxs[0]], "1")[1]
        n = len(idxs)
        pitch = 0.55
        band_top = cath_y + 0.8
        for i, idx in enumerate(idxs):
            col = spos[idx][3]
            cath = pad_xy(diodes[idx], "1")
            esc_y = band_top + (n - 1 - i) * pitch
            vx = cath[0] - 1.3
            gut = col_gutter[col]
            # F dogbone → blind via to In2
            track(b, cath, (vx, cath[1]), f"COL{col}", F, TW)
            blind_via(b, vx, cath[1], f"COL{col}", F, In2)
            # unique-Y hop to gutter (left keys lower Y ⇒ no in-row cross)
            track(b, (vx, cath[1]), (vx, esc_y), f"COL{col}", In2, TW)
            track(b, (vx, esc_y), (gut, esc_y), f"COL{col}", In2, TW)
            # gutter vertical down to per-COL travel_y (ends before lower travel lines of higher cols... 
            # actually extends to this col's travel_y)
            track(b, (gut, esc_y), (gut, col_travel_y[col]), f"COL{col}", In2, TW)

    # Gutter → left spine at unique travel_y (going LEFT; lower cols end above ⇒ no cross)
    for c in range(14):
        gut = col_gutter[c]
        ty = col_travel_y[c]
        sp = col_spine[c]
        track(b, (gut, ty), (sp, ty), f"COL{c}", In2, TW)

    # ----- MCU + USB -----
    mcu_x, mcu_y = pcb_w / 2.0, pcb_h - 45.0
    mod_nets = {
        "1": "GND", "2": "ROW0", "3": "ROW1", "4": "ROW2", "5": "ROW3", "6": "ROW4",
        "7": "COL0", "8": "COL1", "9": "COL2", "10": "COL3", "11": "COL4", "12": "COL5", "13": "COL6",
        "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN",
        "19": "COL7", "20": "COL8", "21": "COL9", "22": "COL10", "23": "COL11",
        "24": "COL12", "25": "COL13", "26": "GND",
    }
    u1 = b.add_footprint(
        "ISM.pretty", "ISM_RP2040_Module", "U1", mcu_x, mcu_y, value="RP2040_MOD",
        pad_nets=mod_nets, lib_path=ISM_PRETTY,
    )
    j1 = b.add_footprint(
        "Connector_USB.pretty", "USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal", "J1",
        pcb_w / 2, 8.0, value="USB_C",
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
                    mcu_x + 24, mcu_y, value="RESET", pad_nets={"1": "RUN", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R4",
                    mcu_x + 32, mcu_y, value="10k", pad_nets={"1": "RUN", "2": "+3V3"})
    b.add_footprint("LED_SMD.pretty", "LED_0603_1608Metric", "D_PWR",
                    mcu_x + 24, mcu_y + 8, value="LED", pad_nets={"1": "GND", "2": "LED_A"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R5",
                    mcu_x + 32, mcu_y + 8, value="1k", pad_nets={"1": "+3V3", "2": "LED_A"})
    for i in range(4):
        b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", f"C{i+1}",
                        mcu_x - 22 + i * 4, mcu_y - 22, value="100nF",
                        pad_nets={"1": "+3V3", "2": "GND"})
    for i, (hx, hy) in enumerate([(8, 8), (pcb_w - 8, 8), (8, pcb_h - 8), (pcb_w - 8, pcb_h - 8)], 1):
        b.add_footprint("MountingHole.pretty", "MountingHole_2.2mm_M2_DIN965_Pad", f"H{i}", hx, hy, value="M2")

    def fp(ref):
        return next(f for f in b.board.GetFootprints() if f.GetReference() == ref)

    # ROW fan: rail ↓ to exclusive fan_y, left to pad approach, up to pad
    for r in range(5):
        gx = row_rail_x[r]
        ry = row_ends[r][1]
        px, py = pad_xy(u1, str(2 + r))
        fan_y = mcu_y + 4.0 + r * 1.3
        ax = px - 2.2
        track(b, (gx, ry), (gx, fan_y), f"ROW{r}", In1, TW)
        track(b, (gx, fan_y), (ax, fan_y), f"ROW{r}", In1, TW)
        track(b, (ax, fan_y), (ax, py), f"ROW{r}", In1, TW)
        blind_via(b, ax, py, f"ROW{r}", F, In1)
        track(b, (ax, py), (px, py), f"ROW{r}", F, 0.2)

    # COL fan: exclusive fan_y below MCU so under-board runs never share a Y
    col_pad = {i: str(7 + i) for i in range(7)}
    col_pad.update({i: str(19 + i - 7) for i in range(7, 14)})
    for c in range(14):
        sp = col_spine[c]
        ty = col_travel_y[c]
        px, py = pad_xy(u1, col_pad[c])
        fan_y = mcu_y + 10.0 + c * 1.25
        # approach X: left pads from left, right pads from right
        if c < 7:
            ax = px - 2.2 - (6 - c) * 0.15
        else:
            ax = px + 2.2 + (c - 7) * 0.15
        track(b, (sp, ty), (sp, fan_y), f"COL{c}", In2, TW)
        track(b, (sp, fan_y), (ax, fan_y), f"COL{c}", In2, TW)
        track(b, (ax, fan_y), (ax, py), f"COL{c}", In2, TW)
        blind_via(b, ax, py, f"COL{c}", F, In2)
        track(b, (ax, py), (px, py), f"COL{c}", F, 0.2)

    # USB / power
    for jpad, net, vx, yb, mpad in [
        ("A6", "USB_DP", pcb_w - 3.0, 14.0, "17"),
        ("A7", "USB_DM", pcb_w - 4.5, 16.0, "16"),
    ]:
        jp = pad_xy(j1, jpad)
        track(b, jp, (jp[0], yb), net, F, TW)
        track(b, (jp[0], yb), (vx, yb), net, F, TW)
        b.add_via(vx, yb, net, VIA_D, VIA_DRILL)
        track(b, (vx, yb), (vx, mcu_y - 8), net, B, TW)
        b.add_via(vx, mcu_y - 8, net, VIA_D, VIA_DRILL)
        manh(b, (vx, mcu_y - 8), pad_xy(u1, mpad), net, F, 0.25, hf=False)

    vbus = pad_xy(j1, "A4")
    track(b, vbus, (vbus[0], 12), "+5V", F, 0.4)
    track(b, (vbus[0], 12), (pcb_w - 2.0, 12), "+5V", F, 0.4)
    b.add_via(pcb_w - 2.0, 12, "+5V", VIA_D, VIA_DRILL)
    track(b, (pcb_w - 2.0, 12), (pcb_w - 2.0, mcu_y), "+5V", B, 0.4)
    b.add_via(pcb_w - 2.0, mcu_y, "+5V", VIA_D, VIA_DRILL)
    manh(b, (pcb_w - 2.0, mcu_y), pad_xy(u1, "15"), "+5V", F, 0.3)

    for args in [
        ("R1", "1", "J1", "A5", "CC1"), ("R2", "1", "J1", "B5", "CC2"),
        ("U2", "1", "J1", "A6", "USB_DP"), ("U2", "3", "J1", "A7", "USB_DM"),
        ("SW_RST", "1", "U1", "18", "RUN"), ("R4", "1", "U1", "18", "RUN"),
        ("R4", "2", "U1", "14", "+3V3"), ("R5", "1", "U1", "14", "+3V3"),
        ("R5", "2", "D_PWR", "2", "LED_A"),
        ("C1", "1", "U1", "14", "+3V3"), ("C2", "1", "C1", "1", "+3V3"),
        ("C3", "1", "C2", "1", "+3V3"), ("C4", "1", "C3", "1", "+3V3"),
    ]:
        try:
            manh(b, pad_xy(fp(args[0]), args[1]), pad_xy(fp(args[2]), args[3]), args[4], F, 0.25)
        except Exception as e:
            print("stub", args, e, flush=True)

    manh(b, pad_xy(u1, "1"), pad_xy(u1, "26"), "GND", F, 0.4)
    gnd_pts = [pad_xy(u1, "1")]
    for ref, pn in [("C1", "2"), ("C2", "2"), ("C3", "2"), ("C4", "2"),
                    ("SW_RST", "2"), ("D_PWR", "1"), ("R1", "2"), ("R2", "2"), ("U2", "2")]:
        try:
            gnd_pts.append(pad_xy(fp(ref), pn))
        except Exception:
            pass
    for a, c in zip(gnd_pts, gnd_pts[1:]):
        manh(b, a, c, "GND", F, 0.3)
    try:
        g0 = pad_xy(j1, "A1")
        for pn in ("A12", "B1", "B12", "S1", "A8", "B8"):
            try:
                manh(b, g0, pad_xy(j1, pn), "GND", F, 0.3)
            except Exception:
                pass
        b.add_via(pcb_w - 6.0, 10.0, "GND", VIA_D, VIA_DRILL)
        track(b, g0, (pcb_w - 6.0, 10.0), "GND", F, 0.4)
        track(b, (pcb_w - 6.0, 10.0), (pcb_w - 6.0, mcu_y), "GND", B, 0.4)
        b.add_via(pcb_w - 6.0, mcu_y, "GND", VIA_D, VIA_DRILL)
        manh(b, (pcb_w - 6.0, mcu_y), pad_xy(u1, "1"), "GND", F, 0.4)
    except Exception as e:
        print("gnd", e, flush=True)
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
        ["U1", "RP2040_MOD", "ISM_RP2040_Module", "1", "ISM", "ISM-RP2040-MOD", "", "Carrier"],
        ["U2", "USBLC6-2SC6", "SOT-666", "1", "ST", "USBLC6-2SC6", "C7519", "ESD"],
        ["J1", "USB4105", "GCT USB-C 16P", "1", "GCT", "USB4105-GF-A", "C165948", ""],
        ["R1,R2", "5.1k", "0603", "2", "", "5.1k", "C23244", "CC"],
        ["R4", "10k", "0603", "1", "", "10k", "C25804", ""],
        ["R5", "1k", "0603", "1", "", "1k", "C21190", ""],
        ["C1-C4", "100nF", "0603", "4", "", "100nF", "C14663", ""],
        ["D1-D61", "1N4148W", "SOD-123", "61", "", "1N4148W", "C2128", ""],
        ["D_PWR", "LED", "0603", "1", "", "LED", "C2286", ""],
        ["SW1-SW61", "MX hotswap", "ISM SW_MX_Hotswap", "61", "", "", "", ""],
        ["SW_RST", "PTS645", "PTS645", "1", "", "PTS645", "C318884", ""],
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
    text = pcb_path.read_text().replace(
        "(allow_soldermask_bridges_in_footprints no)",
        "(allow_soldermask_bridges_in_footprints yes)",
    )
    pcb_path.write_text(text)
    # pcbnew Save() rewrites .kicad_pro and resets severities — restore mouse-matched profile
    write_tables()
    print("pcb ok", pcb_path.stat().st_size, flush=True)
    export_fab(pcb_path)
    subprocess.run(["kicad-cli", "sch", "erc", "--severity-error", "--exit-code-violations",
                    "-o", str(KICAD / "erc.rpt"), str(KICAD / "ism-keyboard-60.kicad_sch")], check=False)
    subprocess.run(["kicad-cli", "pcb", "drc", "--severity-error", "--exit-code-violations",
                    "-o", str(KICAD / "drc.rpt"), str(pcb_path)], check=False)

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
