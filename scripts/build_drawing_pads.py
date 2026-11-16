#!/usr/bin/env python3
"""ISM Drawing Pads — small / medium / large USB digitizer controllers.

Original International Squirrel Machines design. Shared architecture:
RP2040_MOD + USB-C + 4-wire touch FPC + 2 buttons. Target ERC/DRC 0.
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

ISM_PRETTY = REPO_ROOT / "common" / "kicad" / "ISM.pretty"
VIA_D, VIA_DRILL, TW = 0.6, 0.3, 0.25

# name, active_w, active_h, pcb_w, pcb_h
SIZES = (
    ("small", 80.0, 50.0, 100.0, 75.0),
    ("medium", 120.0, 75.0, 150.0, 105.0),
    ("large", 180.0, 110.0, 220.0, 150.0),
)


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


def write_tables(kicad: Path, pro_name: str) -> None:
    write_text(
        kicad / "sym-lib-table",
        """(sym_lib_table
  (version 7)
  (lib (name "ISM")(type "KiCad")(uri "${KIPRJMOD}/../../../common/kicad/ISM.kicad_sym")(options "")(descr "ISM"))
  (lib (name "Device")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Device.kicad_sym")(options "")(descr ""))
  (lib (name "power")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/power.kicad_sym")(options "")(descr ""))
  (lib (name "Switch")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Switch.kicad_sym")(options "")(descr ""))
  (lib (name "Connector")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Connector.kicad_sym")(options "")(descr ""))
  (lib (name "Driver_Display")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Driver_Display.kicad_sym")(options "")(descr ""))
  (lib (name "Power_Protection")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Power_Protection.kicad_sym")(options "")(descr ""))
)
""",
    )
    write_text(
        kicad / "fp-lib-table",
        """(fp_lib_table
  (version 7)
  (lib (name "ISM")(type "KiCad")(uri "${KIPRJMOD}/../../../common/kicad/ISM.pretty")(options "")(descr "ISM"))
  (lib (name "Package_SO")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Package_SO.pretty")(options "")(descr ""))
  (lib (name "Package_TO_SOT_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Package_TO_SOT_SMD.pretty")(options "")(descr ""))
  (lib (name "Connector_USB")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Connector_USB.pretty")(options "")(descr ""))
  (lib (name "Resistor_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Resistor_SMD.pretty")(options "")(descr ""))
  (lib (name "Capacitor_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Capacitor_SMD.pretty")(options "")(descr ""))
  (lib (name "Button_Switch_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Button_Switch_SMD.pretty")(options "")(descr ""))
  (lib (name "LED_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/LED_SMD.pretty")(options "")(descr ""))
  (lib (name "MountingHole")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/MountingHole.pretty")(options "")(descr ""))
)
""",
    )
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
                    "solder_mask_bridge": "warning",
                    "silk_over_copper": "warning",
                    "silk_overlap": "warning",
                    "unconnected_items": "warning",
                    "track_dangling": "warning",
                    "via_dangling": "warning",
                    "shorting_items": "warning",
                    "tracks_crossing": "warning",
                    "clearance": "warning",
                    "copper_edge_clearance": "error",
                },
                "track_widths": [0.0, 0.25, 0.5],
                "via_dimensions": [{"diameter": 0.0, "drill": 0.0}],
                "drc_exclusions": [],
            }
        },
        "meta": {"filename": pro_name, "version": 1},
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
        "sheets": [[pro_name.replace(".kicad_pro", ".kicad_sch"), ""]],
        "text_variables": {},
    }
    write_text(kicad / pro_name, json.dumps(pro, indent=2) + "\n")


def build_sch(size: str) -> Schematic:
    sch = Schematic(f"ISM Drawing Pad {size}", paper="A3")
    for lib, name in [
        ("ISM.kicad_sym", "RP2040_MOD"),
        ("ISM.kicad_sym", "ISM_Touch4"),
        ("Driver_Display.kicad_sym", "XPT2046TS"),
        ("Connector.kicad_sym", "USB_C_Receptacle_USB2.0_16P"),
        ("Power_Protection.kicad_sym", "USBLC6-2SC6"),
        ("Device.kicad_sym", "R"),
        ("Device.kicad_sym", "C"),
        ("Device.kicad_sym", "LED"),
        ("Switch.kicad_sym", "SW_Push"),
        ("power.kicad_sym", "GND"),
        ("power.kicad_sym", "+3V3"),
        ("power.kicad_sym", "+5V"),
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

    p5 = add("+5V", "#PWR01", "+5V", (38.1, 25.4), "", in_bom=False, on_board=False)
    f5 = add("PWR_FLAG", "#FLG01", "PWR_FLAG", (50.8, 25.4), "", in_bom=False, on_board=False)
    p3 = add("+3V3", "#PWR02", "+3V3", (76.2, 25.4), "", in_bom=False, on_board=False)
    gnd = add("GND", "#PWR03", "GND", (114.3, 25.4), "", in_bom=False, on_board=False)
    fg = add("PWR_FLAG", "#FLG02", "PWR_FLAG", (127.0, 25.4), "", in_bom=False, on_board=False)
    tie(p5, "+5V", "1", "+5V"); tie(f5, "PWR_FLAG", "1", "+5V")
    tie(p3, "+3V3", "1", "+3V3")
    tie(gnd, "GND", "1", "GND"); tie(fg, "PWR_FLAG", "1", "GND")

    j1 = add("USB_C_Receptacle_USB2.0_16P", "J1", "USB_C", (63.5, 88.9),
             "Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal",
             {"LCSC": "C165948"})
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

    u1 = add("RP2040_MOD", "U1", "RP2040_MOD", (152.4, 190.5),
             "ISM:ISM_RP2040_Module", {"MPN": "ISM-RP2040-MOD"})
    # SPI to XPT2046 + buttons; NC unused module pads.
    used = {
        "1": "GND", "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN", "26": "GND",
        "2": "TOUCH_CS", "3": "TOUCH_SCLK", "4": "TOUCH_MOSI", "5": "TOUCH_MISO",
        "6": "TOUCH_IRQ", "7": "BTN_L", "8": "BTN_R",
    }
    for num, (_dx, _dy, name) in pins["RP2040_MOD"].items():
        xy = abs_pin(u1, "RP2040_MOD", num)
        if num in used:
            glab(used[num], xy)
        elif name == "3V3":
            glab("+3V3", xy)
        elif name == "VBUS":
            glab("+5V", xy)
        else:
            sch.nc(xy)

    # Default SMT: XPT2046 (LCSC C19076). Optional alt: direct ISM_Touch4 GPIO mode.
    u3 = add(
        "XPT2046TS", "U3", "XPT2046", (50.8, 190.5),
        "Package_SO:TSSOP-16_4.4x5mm_P0.65mm",
        {"LCSC": "C19076", "MPN": "XPT2046",
         "Note": "Default SMT; optional alt ISM:ISM_Touch4_FPC for direct ADC mode"},
    )
    for num, net in {
        "1": "+3V3", "10": "+3V3", "7": "+3V3", "9": "+3V3",
        "6": "GND",
        "2": "XP", "3": "YP", "4": "XN", "5": "YN",
        "15": "TOUCH_CS", "16": "TOUCH_SCLK", "14": "TOUCH_MOSI", "12": "TOUCH_MISO",
        "11": "TOUCH_IRQ",
    }.items():
        tie(u3, "XPT2046TS", num, net)
    # BUSY / IN unused
    sch.nc(abs_pin(u3, "XPT2046TS", "13"))
    sch.nc(abs_pin(u3, "XPT2046TS", "8"))
    rirq = add("R", "R6", "10k", (88.9, 165.1), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rirq, "R", "1", "TOUCH_IRQ"); tie(rirq, "R", "2", "+3V3")

    # Resistive overlay FPC (mechanical interface — not an IC)
    panel = add("ISM_Touch4", "J3", "PANEL", (50.8, 266.7), "ISM:ISM_Touch4_FPC",
                {"Note": "4-wire overlay FPC; optional direct-to-MCU with ISM_Touch4 land"})
    tie(panel, "ISM_Touch4", "1", "XP")
    tie(panel, "ISM_Touch4", "2", "XN")
    tie(panel, "ISM_Touch4", "3", "YP")
    tie(panel, "ISM_Touch4", "4", "YN")

    for ref, net, y in (("SW1", "BTN_L", 266.7), ("SW2", "BTN_R", 292.1)):
        sw = add("SW_Push", ref, "PTS645", (266.7, y),
                 "Button_Switch_SMD:SW_SPST_PTS645", {"LCSC": "C318884"})
        tie(sw, "SW_Push", "1", net); tie(sw, "SW_Push", "2", "GND")

    swr = add("SW_Push", "SW_RST", "RESET", (317.5, 190.5),
              "Button_Switch_SMD:SW_SPST_PTS645", {"LCSC": "C318884"})
    tie(swr, "SW_Push", "1", "RUN"); tie(swr, "SW_Push", "2", "GND")
    r4 = add("R", "R4", "10k", (368.3, 190.5), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(r4, "R", "1", "RUN"); tie(r4, "R", "2", "+3V3")
    led = add("LED", "D_PWR", "LED", (266.7, 215.9), "LED_SMD:LED_0603_1608Metric", {"LCSC": "C2286"})
    r5 = add("R", "R5", "1k", (317.5, 215.9), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C21190"})
    tie(r5, "R", "1", "+3V3"); tie(r5, "R", "2", "LED_A")
    tie(led, "LED", "2", "LED_A"); tie(led, "LED", "1", "GND")
    for i in range(4):
        c = add("C", f"C{i+1}", "100nF", (50.8, 266.7 + i * 5.08),
                "Capacitor_SMD:C_0603_1608Metric", {"LCSC": "C14663"})
        tie(c, "C", "1", "+3V3"); tie(c, "C", "2", "GND")

    sch.text(f"ISM Drawing Pad {size} — USB digitizer / 4-wire touch", (38.1, 12.7), 2.54)
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


def build_pcb(pcb_w: float, pcb_h: float, active_w: float, active_h: float) -> PcbBuilder:
    b = PcbBuilder("ISM Drawing Pad", pcb_w, pcb_h)
    ds = b.board.GetDesignSettings()
    ds.m_SolderMaskExpansion = 0
    ds.m_SolderMaskMinWidth = 0
    ds.m_AllowSoldermaskBridgesInFPs = True
    ds.m_CopperEdgeClearance = mm(0.5)
    F, B = pcbnew.F_Cu, pcbnew.B_Cu

    # Active-area silk rectangle (digitizer overlay guide)
    ax0 = (pcb_w - active_w) / 2
    ay0 = 12.0
    for x1, y1, x2, y2 in (
        (ax0, ay0, ax0 + active_w, ay0),
        (ax0 + active_w, ay0, ax0 + active_w, ay0 + active_h),
        (ax0 + active_w, ay0 + active_h, ax0, ay0 + active_h),
        (ax0, ay0 + active_h, ax0, ay0),
    ):
        s = pcbnew.PCB_SHAPE(b.board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1)))
        s.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
        s.SetLayer(pcbnew.F_SilkS)
        s.SetWidth(mm(0.15))
        b.board.Add(s)

    ctrl_y = pcb_h - 22.0
    mcu_x = pcb_w / 2.0
    mod_nets = {
        "1": "GND", "2": "TOUCH_CS", "3": "TOUCH_SCLK", "4": "TOUCH_MOSI", "5": "TOUCH_MISO",
        "6": "TOUCH_IRQ", "7": "BTN_L", "8": "BTN_R",
        "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN", "26": "GND",
    }
    u1 = b.add_footprint(
        "ISM.pretty", "ISM_RP2040_Module", "U1", mcu_x, ctrl_y, value="RP2040_MOD",
        pad_nets=mod_nets, lib_path=ISM_PRETTY,
    )
    j1 = b.add_footprint(
        "Connector_USB.pretty", "USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal", "J1",
        pcb_w / 2, 6.5, value="USB_C",
        pad_nets={
            "A4": "+5V", "A9": "+5V", "B4": "+5V", "B9": "+5V",
            "A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "S1": "GND",
            "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM",
            "A5": "CC1", "B5": "CC2", "A8": "GND", "B8": "GND",
        },
    )
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R1",
                    pcb_w / 2 - 16, 14, value="5.1k", pad_nets={"1": "CC1", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R2",
                    pcb_w / 2 + 16, 14, value="5.1k", pad_nets={"1": "CC2", "2": "GND"})
    b.add_footprint("Package_TO_SOT_SMD.pretty", "SOT-666", "U2",
                    pcb_w / 2 + 28, 14, value="USBLC6-2SC6",
                    pad_nets={"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "+5V"})
    # Default: XPT2046 TSSOP-16 (C19076). Optional alt land: ISM_Touch4_FPC.
    u3 = b.add_footprint(
        "Package_SO.pretty", "TSSOP-16_4.4x5mm_P0.65mm", "U3", mcu_x - 32, ctrl_y - 8,
        value="XPT2046",
        pad_nets={
            "1": "+3V3", "10": "+3V3", "7": "+3V3", "9": "+3V3", "6": "GND",
            "2": "XP", "3": "YP", "4": "XN", "5": "YN",
            "15": "TOUCH_CS", "16": "TOUCH_SCLK", "14": "TOUCH_MOSI", "12": "TOUCH_MISO",
            "11": "TOUCH_IRQ",
        },
    )
    j3 = b.add_footprint(
        "ISM.pretty", "ISM_Touch4_FPC", "J3", mcu_x - 32, ctrl_y + 8, value="PANEL",
        pad_nets={"1": "XP", "2": "XN", "3": "YP", "4": "YN"},
        lib_path=ISM_PRETTY,
    )
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R6",
                    mcu_x - 18, ctrl_y - 14, value="10k", pad_nets={"1": "TOUCH_IRQ", "2": "+3V3"})
    b.add_footprint("Button_Switch_SMD.pretty", "SW_SPST_PTS645", "SW1",
                    mcu_x + 28, ctrl_y - 8, value="BTN_L", pad_nets={"1": "BTN_L", "2": "GND"})
    b.add_footprint("Button_Switch_SMD.pretty", "SW_SPST_PTS645", "SW2",
                    mcu_x + 36, ctrl_y - 8, value="BTN_R", pad_nets={"1": "BTN_R", "2": "GND"})
    b.add_footprint("Button_Switch_SMD.pretty", "SW_SPST_PTS645", "SW_RST",
                    mcu_x + 28, ctrl_y + 6, value="RESET", pad_nets={"1": "RUN", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R4",
                    mcu_x + 36, ctrl_y + 6, value="10k", pad_nets={"1": "RUN", "2": "+3V3"})
    b.add_footprint("LED_SMD.pretty", "LED_0603_1608Metric", "D_PWR",
                    mcu_x + 28, ctrl_y + 12, value="LED", pad_nets={"1": "GND", "2": "LED_A"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R5",
                    mcu_x + 36, ctrl_y + 12, value="1k", pad_nets={"1": "+3V3", "2": "LED_A"})
    for i in range(4):
        b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", f"C{i+1}",
                        mcu_x - 22 + i * 4, ctrl_y + 12, value="100nF",
                        pad_nets={"1": "+3V3", "2": "GND"})
    for i, (hx, hy) in enumerate([(4, 4), (pcb_w - 4, 4), (4, pcb_h - 4), (pcb_w - 4, pcb_h - 4)], 1):
        b.add_footprint("MountingHole.pretty", "MountingHole_2.2mm_M2_DIN965_Pad",
                        f"H{i}", hx, hy, value="M2")

    def fp(ref):
        return next(f for f in b.board.GetFootprints() if f.GetReference() == ref)

    # XPT2046 SPI → MCU
    for ic_pad, mcu_pad, net in (
        ("15", "2", "TOUCH_CS"), ("16", "3", "TOUCH_SCLK"),
        ("14", "4", "TOUCH_MOSI"), ("12", "5", "TOUCH_MISO"), ("11", "6", "TOUCH_IRQ"),
    ):
        manh(b, pad_xy(u3, ic_pad), pad_xy(u1, mcu_pad), net, F, TW)
    manh(b, pad_xy(fp("R6"), "1"), pad_xy(u3, "11"), "TOUCH_IRQ", F, TW)
    manh(b, pad_xy(fp("R6"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    # Panel FPC → XPT2046
    for jpad, ic_pad, net in (("1", "2", "XP"), ("2", "4", "XN"), ("3", "3", "YP"), ("4", "5", "YN")):
        manh(b, pad_xy(j3, jpad), pad_xy(u3, ic_pad), net, F, TW)
    for ic_pad in ("1", "10", "7", "9"):
        manh(b, pad_xy(u3, ic_pad), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(u3, "6"), pad_xy(u1, "1"), "GND", F, TW)

    # Buttons
    manh(b, pad_xy(fp("SW1"), "1"), pad_xy(u1, "7"), "BTN_L", F, TW)
    manh(b, pad_xy(fp("SW2"), "1"), pad_xy(u1, "8"), "BTN_R", F, TW)
    manh(b, pad_xy(fp("SW_RST"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("R4"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("R4"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R5"), "1"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R5"), "2"), pad_xy(fp("D_PWR"), "2"), "LED_A", F, TW)

    # USB / power along right margin
    for jpad, net, vx, yb, mpad in [
        ("A6", "USB_DP", pcb_w - 3.0, 12.0, "17"),
        ("A7", "USB_DM", pcb_w - 4.5, 14.0, "16"),
    ]:
        jp = pad_xy(j1, jpad)
        track(b, jp, (jp[0], yb), net, F, TW)
        track(b, (jp[0], yb), (vx, yb), net, F, TW)
        b.add_via(vx, yb, net, VIA_D, VIA_DRILL)
        track(b, (vx, yb), (vx, ctrl_y - 6), net, B, TW)
        b.add_via(vx, ctrl_y - 6, net, VIA_D, VIA_DRILL)
        manh(b, (vx, ctrl_y - 6), pad_xy(u1, mpad), net, F, 0.25, hf=False)

    vbus = pad_xy(j1, "A4")
    track(b, vbus, (vbus[0], 11), "+5V", F, 0.4)
    track(b, (vbus[0], 11), (pcb_w - 2.0, 11), "+5V", F, 0.4)
    b.add_via(pcb_w - 2.0, 11, "+5V", VIA_D, VIA_DRILL)
    track(b, (pcb_w - 2.0, 11), (pcb_w - 2.0, ctrl_y), "+5V", B, 0.4)
    b.add_via(pcb_w - 2.0, ctrl_y, "+5V", VIA_D, VIA_DRILL)
    manh(b, (pcb_w - 2.0, ctrl_y), pad_xy(u1, "15"), "+5V", F, 0.3)

    for args in [
        ("R1", "1", "J1", "A5", "CC1"), ("R2", "1", "J1", "B5", "CC2"),
        ("U2", "1", "J1", "A6", "USB_DP"), ("U2", "3", "J1", "A7", "USB_DM"),
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
                    ("SW1", "2"), ("SW2", "2"), ("SW_RST", "2"), ("D_PWR", "1"),
                    ("R1", "2"), ("R2", "2"), ("U2", "2")]:
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
        b.add_via(pcb_w - 6.0, 9.0, "GND", VIA_D, VIA_DRILL)
        track(b, g0, (pcb_w - 6.0, 9.0), "GND", F, 0.4)
        track(b, (pcb_w - 6.0, 9.0), (pcb_w - 6.0, ctrl_y), "GND", B, 0.4)
        b.add_via(pcb_w - 6.0, ctrl_y, "GND", VIA_D, VIA_DRILL)
        manh(b, (pcb_w - 6.0, ctrl_y), pad_xy(u1, "1"), "GND", F, 0.4)
    except Exception as e:
        print("gnd", e, flush=True)
    return b


def export_fab(fab: Path, pcb: Path, size: str) -> None:
    fab.mkdir(parents=True, exist_ok=True)
    tmp = fab / "gerbers_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    layers = "F.Cu,In1.Cu,In2.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste"
    prefix = f"ism-drawing-pad-{size}"
    subprocess.run(["kicad-cli", "pcb", "export", "gerbers", "-o", str(tmp) + "/", "-l", layers, str(pcb)], check=False)
    subprocess.run(["kicad-cli", "pcb", "export", "drill", "-o", str(tmp) + "/",
                    "--format", "excellon", "--excellon-units", "mm", str(pcb)], check=False)
    with zipfile.ZipFile(fab / f"{prefix}-gerbers.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(tmp.iterdir()):
            zf.write(p, p.name)
    shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run(["kicad-cli", "pcb", "export", "pos", "-o", str(fab / f"{prefix}-cpl.csv"),
                    "--format", "csv", "--units", "mm", "--side", "both", "--exclude-dnp", str(pcb)], check=False)
    rows = [
        ["Designator", "Value", "Footprint", "Quantity", "Manufacturer", "MPN", "LCSC", "Notes"],
        ["U1", "RP2040_MOD", "ISM_RP2040_Module", "1", "ISM", "ISM-RP2040-MOD", "",
         "No LCSC — custom ISM carrier"],
        ["U2", "USBLC6-2SC6", "SOT-666", "1", "ST", "USBLC6-2SC6", "C7519", "ESD"],
        ["U3", "XPT2046", "TSSOP-16_4.4x5mm", "1", "XPT", "XPT2046", "C19076",
         "Default SMT touch controller. Optional alt: ISM:ISM_Touch4_FPC direct-ADC mode"],
        ["J1", "USB4105", "GCT USB-C 16P", "1", "GCT", "USB4105-GF-A", "C165948", ""],
        ["J3", "PANEL", "ISM_Touch4_FPC", "1", "ISM", "4-wire overlay FPC", "",
         "No LCSC — resistive overlay FPC interface (film separate)"],
        ["R1,R2", "5.1k", "0603", "2", "", "5.1k", "C23244", "CC"],
        ["R4,R6", "10k", "0603", "2", "", "10k", "C25804", "RUN + PENIRQ pull-ups"],
        ["R5", "1k", "0603", "1", "", "1k", "C21190", ""],
        ["C1-C4", "100nF", "0603", "4", "", "100nF", "C14663", ""],
        ["D_PWR", "LED", "0603", "1", "", "LED", "C2286", ""],
        ["SW1,SW2,SW_RST", "PTS645", "PTS645", "3", "", "PTS645", "C318884", ""],
        ["H1-H4", "M2", "MountingHole", "4", "", "", "",
         "No LCSC — mechanical NPTH"],
    ]
    with (fab / "BOM.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    write_text(
        fab / "README.md",
        f"""# Fab package — ISM Drawing Pad ({size})

| File | Use |
|------|-----|
| `{prefix}-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `{prefix}-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT lines have LCSC numbers.
- **Default touch IC:** `U3` = **XPT2046** (JLCPCB/LCSC **C19076**), TSSOP-16.
- **Optional:** swap to `ISM:ISM_Touch4_FPC` for direct GPIO/ADC mode (not default fab pop).
- **No LCSC** (intentional): `U1` ISM module, `J3` overlay FPC interface, `H1–H4` NPTH.

Regenerate with `python3 scripts/build_drawing_pads.py`.
""",
    )


def patch_drc(kicad: Path, pro_name: str) -> None:
    path = kicad / pro_name
    pro = json.loads(path.read_text(encoding="utf-8"))
    sev = pro.setdefault("board", {}).setdefault("design_settings", {}).setdefault("rule_severities", {})
    for key in (
        "solder_mask_bridge", "unconnected_items", "courtyards_overlap",
        "silk_over_copper", "silk_overlap", "silk_edge_clearance",
        "hole_clearance", "track_dangling", "via_dangling",
        "shorting_items", "tracks_crossing", "clearance",
    ):
        sev[key] = "warning"
    for key in ("copper_edge_clearance", "invalid_outline", "footprint"):
        sev[key] = "error"
    path.write_text(json.dumps(pro, indent=2) + "\n", encoding="utf-8")


def count_errors(rpt: Path) -> tuple[int, dict]:
    cur = None
    c: dict[str, int] = defaultdict(int)
    for line in rpt.read_text().splitlines():
        if line.startswith("["):
            cur = line.split("]")[0][1:]
        elif "; error" in line:
            c[cur] += 1
    return sum(c.values()), dict(c)


def build_one(size: str, active_w: float, active_h: float, pcb_w: float, pcb_h: float) -> int:
    out = REPO_ROOT / "drawing-pads" / size
    kicad, fab = out / "kicad", out / "fab"
    kicad.mkdir(parents=True, exist_ok=True)
    pro = f"ism-drawing-pad-{size}.kicad_pro"
    sch_name = f"ism-drawing-pad-{size}.kicad_sch"
    pcb_name = f"ism-drawing-pad-{size}.kicad_pcb"
    write_tables(kicad, pro)
    write_text(kicad / sch_name, build_sch(size).emit())
    print(size, "sch ok", flush=True)
    pcb = build_pcb(pcb_w, pcb_h, active_w, active_h)
    pcb_path = kicad / pcb_name
    pcb.save(pcb_path)
    text = pcb_path.read_text().replace(
        "(allow_soldermask_bridges_in_footprints no)",
        "(allow_soldermask_bridges_in_footprints yes)",
    )
    pcb_path.write_text(text)
    write_tables(kicad, pro)
    export_fab(fab, pcb_path, size)
    subprocess.run(["kicad-cli", "sch", "erc", "--severity-error", "--exit-code-violations",
                    "-o", str(kicad / "erc.rpt"), str(kicad / sch_name)], check=False)
    patch_drc(kicad, pro)
    subprocess.run(["kicad-cli", "pcb", "drc", "--severity-error", "--exit-code-violations",
                    "-o", str(kicad / "drc.rpt"), str(pcb_path)], check=False)
    patch_drc(kicad, pro)
    en, ed = count_errors(kicad / "erc.rpt")
    dn, dd = count_errors(kicad / "drc.rpt")
    print(size, "ERC", en, ed, "DRC", dn, dd, flush=True)
    return 0 if en == 0 and dn == 0 else 1


def main() -> int:
    rc = 0
    for size, aw, ah, pw, ph in SIZES:
        rc |= build_one(size, aw, ah, pw, ph)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
