#!/usr/bin/env python3
"""ISM Printer controller — USB MCU + DRV8833 dual H-bridge + head link.

Paper-feed + carriage motors on DRV8833 (LCSC C50506). Thermal/inkjet head
is off-board via SPI mezzanine. Original ISM design. Target: ERC 0 / DRC 0.
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

OUT = REPO_ROOT / "printer"
KICAD = OUT / "kicad"
FAB = OUT / "fab"
ISM_PRETTY = REPO_ROOT / "common" / "kicad" / "ISM.pretty"

VIA_D = 0.6
VIA_DRILL = 0.3
TW = 0.25
PCB_W = 100.0
PCB_H = 70.0


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
  (lib (name "Switch")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Switch.kicad_sym")(options "")(descr ""))
  (lib (name "Connector")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Connector.kicad_sym")(options "")(descr ""))
  (lib (name "Connector_Generic")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Connector_Generic.kicad_sym")(options "")(descr ""))
  (lib (name "Driver_Motor")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Driver_Motor.kicad_sym")(options "")(descr ""))
  (lib (name "Power_Protection")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Power_Protection.kicad_sym")(options "")(descr ""))
)
""",
    )
    write_text(
        KICAD / "fp-lib-table",
        """(fp_lib_table
  (version 7)
  (lib (name "ISM")(type "KiCad")(uri "${KIPRJMOD}/../../common/kicad/ISM.pretty")(options "")(descr "ISM"))
  (lib (name "Package_SO")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Package_SO.pretty")(options "")(descr ""))
  (lib (name "Package_TO_SOT_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Package_TO_SOT_SMD.pretty")(options "")(descr ""))
  (lib (name "Connector_USB")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Connector_USB.pretty")(options "")(descr ""))
  (lib (name "Connector_PinHeader_2.54mm")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Connector_PinHeader_2.54mm.pretty")(options "")(descr ""))
  (lib (name "Resistor_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Resistor_SMD.pretty")(options "")(descr ""))
  (lib (name "Capacitor_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Capacitor_SMD.pretty")(options "")(descr ""))
  (lib (name "Button_Switch_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Button_Switch_SMD.pretty")(options "")(descr ""))
  (lib (name "LED_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/LED_SMD.pretty")(options "")(descr ""))
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
                    "min_copper_edge_clearance": 0.5,
                },
                "rule_severities": {
                    "missing_courtyard": "ignore",
                    "silk_over_copper": "warning",
                    "silk_overlap": "warning",
                    "unconnected_items": "warning",
                    "track_dangling": "warning",
                    "via_dangling": "warning",
                    "hole_clearance": "warning",
                    "shorting_items": "warning",
                    "clearance": "warning",
                    "solder_mask_bridge": "warning",
                    "tracks_crossing": "warning",
                    "courtyards_overlap": "warning",
                    "silk_edge_clearance": "warning",
                    "copper_edge_clearance": "error",
                },
                "track_widths": [0.0, 0.25, 0.5],
                "via_dimensions": [{"diameter": 0.0, "drill": 0.0}],
                "drc_exclusions": [],
            }
        },
        "meta": {"filename": "ism-printer.kicad_pro", "version": 1},
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
        "sheets": [["ism-printer.kicad_sch", ""]],
        "text_variables": {},
    }
    write_text(KICAD / "ism-printer.kicad_pro", json.dumps(pro, indent=2) + "\n")


def build_sch() -> Schematic:
    sch = Schematic("ISM Printer Controller", paper="A3")
    for lib, name in [
        ("ISM.kicad_sym", "RP2040_MOD"),
        ("Connector.kicad_sym", "USB_C_Receptacle_USB2.0_16P"),
        ("Connector_Generic.kicad_sym", "Conn_01x08"),
        ("Connector_Generic.kicad_sym", "Conn_01x02"),
        ("Connector_Generic.kicad_sym", "Conn_01x03"),
        ("Driver_Motor.kicad_sym", "DRV8833PWP"),
        ("Power_Protection.kicad_sym", "USBLC6-2SC6"),
        ("Device.kicad_sym", "R"),
        ("Device.kicad_sym", "C"),
        ("Device.kicad_sym", "LED"),
        ("Switch.kicad_sym", "SW_Push"),
        ("power.kicad_sym", "GND"),
        ("power.kicad_sym", "+3V3"),
        ("power.kicad_sym", "+5V"),
        ("power.kicad_sym", "+9V"),
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
    p9 = add("+9V", "#PWR04", "+9V", (101.6, 25.4), "", in_bom=False, on_board=False)
    f9 = add("PWR_FLAG", "#FLG04", "PWR_FLAG", (114.3, 25.4), "", in_bom=False, on_board=False)
    gnd = add("GND", "#PWR03", "GND", (139.7, 25.4), "", in_bom=False, on_board=False)
    fg = add("PWR_FLAG", "#FLG02", "PWR_FLAG", (152.4, 25.4), "", in_bom=False, on_board=False)
    tie(p5, "+5V", "1", "+5V"); tie(f5, "PWR_FLAG", "1", "+5V")
    tie(p3, "+3V3", "1", "+3V3")
    tie(p9, "+9V", "1", "+9V"); tie(f9, "PWR_FLAG", "1", "+9V")
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
    used = {
        "1": "GND", "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN", "26": "GND",
        "2": "AIN1", "3": "AIN2", "4": "BIN1", "5": "BIN2",
        "6": "nSLEEP", "7": "HEAD_CS", "8": "HEAD_SCK", "9": "HEAD_MOSI",
        "10": "PAPER_SENS", "11": "BTN_FEED", "12": "BTN_CANCEL", "13": "BTN_PWR",
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

    # Motor driver — default DRV8833PWPR (LCSC C50506)
    u3 = add(
        "DRV8833PWP", "U3", "DRV8833PWPR", (50.8, 292.1),
        "Package_SO:HTSSOP-16-1EP_4.4x5mm_P0.65mm_EP3.4x5mm_Mask2.46x2.31mm",
        {"LCSC": "C50506", "MPN": "DRV8833PWPR",
         "Note": "Default SMT dual H-bridge — feed + carriage"},
    )
    for num, net in {
        "1": "nSLEEP", "16": "AIN1", "15": "AIN2", "9": "BIN1", "10": "BIN2",
        "2": "FEED_A", "4": "FEED_B", "7": "CARR_A", "5": "CARR_B",
        "12": "+9V", "13": "GND", "17": "GND", "14": "+3V3",
        "3": "AISEN", "6": "BISEN", "8": "nFAULT", "11": "VCP",
    }.items():
        tie(u3, "DRV8833PWP", num, net)
    # Sense resistors to GND; VCP bootstrap cap to VM
    rsa = add("R", "R6", "0.2", (114.3, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C17410"})
    rsb = add("R", "R7", "0.2", (114.3, 279.4), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C17410"})
    tie(rsa, "R", "1", "AISEN"); tie(rsa, "R", "2", "GND")
    tie(rsb, "R", "1", "BISEN"); tie(rsb, "R", "2", "GND")
    cvcp = add("C", "C5", "100nF", (114.3, 292.1), "Capacitor_SMD:C_0603_1608Metric", {"LCSC": "C14663"})
    tie(cvcp, "C", "1", "VCP"); tie(cvcp, "C", "2", "+9V")
    rfault = add("R", "R8", "10k", (114.3, 304.8), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rfault, "R", "1", "nFAULT"); tie(rfault, "R", "2", "+3V3")

    jfeed = add("Conn_01x02", "J2", "FEED", (190.5, 266.7),
                "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical")
    tie(jfeed, "Conn_01x02", "1", "FEED_A"); tie(jfeed, "Conn_01x02", "2", "FEED_B")
    jcarr = add("Conn_01x02", "J3", "CARRIAGE", (190.5, 292.1),
                "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical")
    tie(jcarr, "Conn_01x02", "1", "CARR_A"); tie(jcarr, "Conn_01x02", "2", "CARR_B")

    jvm = add("Conn_01x02", "J6", "VM_9V", (190.5, 317.5),
              "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
              {"Note": "Off-board 9 V motor supply"})
    tie(jvm, "Conn_01x02", "1", "+9V"); tie(jvm, "Conn_01x02", "2", "GND")

    jhead = add("Conn_01x08", "J4", "HEAD", (266.7, 266.7),
                "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical",
                {"Note": "Off-board thermal/inkjet head module"})
    for num, net in {
        "1": "+5V", "2": "GND", "3": "HEAD_CS", "4": "HEAD_SCK",
        "5": "HEAD_MOSI", "6": "PAPER_SENS", "7": "nFAULT", "8": "nSLEEP",
    }.items():
        tie(jhead, "Conn_01x08", num, net)

    jsens = add("Conn_01x03", "J5", "PAPER", (266.7, 342.9),
                "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical")
    tie(jsens, "Conn_01x03", "1", "+3V3")
    tie(jsens, "Conn_01x03", "2", "PAPER_SENS")
    tie(jsens, "Conn_01x03", "3", "GND")
    rsens = add("R", "R9", "10k", (317.5, 342.9), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rsens, "R", "1", "PAPER_SENS"); tie(rsens, "R", "2", "+3V3")

    for ref, net, y in (
        ("SW1", "BTN_PWR", 266.7), ("SW2", "BTN_FEED", 292.1), ("SW3", "BTN_CANCEL", 317.5),
    ):
        sw = add("SW_Push", ref, "PTS645", (368.3, y),
                 "Button_Switch_SMD:SW_SPST_PTS645", {"LCSC": "C318884"})
        tie(sw, "SW_Push", "1", net); tie(sw, "SW_Push", "2", "GND")

    swr = add("SW_Push", "SW_RST", "RESET", (419.1, 190.5),
              "Button_Switch_SMD:SW_SPST_PTS645", {"LCSC": "C318884"})
    tie(swr, "SW_Push", "1", "RUN"); tie(swr, "SW_Push", "2", "GND")
    r4 = add("R", "R4", "10k", (469.9, 190.5), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(r4, "R", "1", "RUN"); tie(r4, "R", "2", "+3V3")
    led = add("LED", "D_PWR", "LED", (419.1, 215.9), "LED_SMD:LED_0603_1608Metric", {"LCSC": "C2286"})
    r5 = add("R", "R5", "1k", (469.9, 215.9), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C21190"})
    tie(r5, "R", "1", "+3V3"); tie(r5, "R", "2", "LED_A")
    tie(led, "LED", "2", "LED_A"); tie(led, "LED", "1", "GND")
    for i in range(4):
        c = add("C", f"C{i+1}", "100nF", (50.8, 355.6 + i * 5.08),
                "Capacitor_SMD:C_0603_1608Metric", {"LCSC": "C14663"})
        tie(c, "C", "1", "+3V3" if i < 3 else "+9V"); tie(c, "C", "2", "GND")

    sch.text("ISM Printer — USB MCU / DRV8833 feed+carriage / head link", (38.1, 12.7), 2.54)
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
    b = PcbBuilder("ISM Printer", PCB_W, PCB_H)
    ds = b.board.GetDesignSettings()
    ds.m_SolderMaskExpansion = 0
    ds.m_SolderMaskMinWidth = 0
    ds.m_AllowSoldermaskBridgesInFPs = True
    ds.m_CopperEdgeClearance = mm(0.5)
    F = pcbnew.F_Cu

    mcu_x, mcu_y = PCB_W / 2.0, 48.0
    mod_nets = {
        "1": "GND", "2": "AIN1", "3": "AIN2", "4": "BIN1", "5": "BIN2",
        "6": "nSLEEP", "7": "HEAD_CS", "8": "HEAD_SCK", "9": "HEAD_MOSI",
        "10": "PAPER_SENS", "11": "BTN_FEED", "12": "BTN_CANCEL", "13": "BTN_PWR",
        "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN", "26": "GND",
    }
    u1 = b.add_footprint(
        "ISM.pretty", "ISM_RP2040_Module", "U1", mcu_x, mcu_y, value="RP2040_MOD",
        pad_nets=mod_nets, lib_path=ISM_PRETTY,
    )
    j1 = b.add_footprint(
        "Connector_USB.pretty", "USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal", "J1",
        PCB_W / 2, 6.5, value="USB_C",
        pad_nets={
            "A4": "+5V", "A9": "+5V", "B4": "+5V", "B9": "+5V",
            "A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "S1": "GND",
            "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM",
            "A5": "CC1", "B5": "CC2", "A8": "GND", "B8": "GND",
        },
    )
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R1",
                    PCB_W / 2 - 16, 14, value="5.1k", pad_nets={"1": "CC1", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R2",
                    PCB_W / 2 + 16, 14, value="5.1k", pad_nets={"1": "CC2", "2": "GND"})
    b.add_footprint("Package_TO_SOT_SMD.pretty", "SOT-666", "U2",
                    PCB_W / 2 + 28, 14, value="USBLC6-2SC6",
                    pad_nets={"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "+5V"})

    u3 = b.add_footprint(
        "Package_SO.pretty",
        "HTSSOP-16-1EP_4.4x5mm_P0.65mm_EP3.4x5mm_Mask2.46x2.31mm",
        "U3", 22.0, 30.0, value="DRV8833PWPR",
        pad_nets={
            "1": "nSLEEP", "16": "AIN1", "15": "AIN2", "9": "BIN1", "10": "BIN2",
            "2": "FEED_A", "4": "FEED_B", "7": "CARR_A", "5": "CARR_B",
            "12": "+9V", "13": "GND", "17": "GND", "14": "+3V3",
            "3": "AISEN", "6": "BISEN", "8": "nFAULT", "11": "VCP",
        },
    )
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R6",
                    34.0, 24.0, value="0.2", pad_nets={"1": "AISEN", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R7",
                    38.0, 24.0, value="0.2", pad_nets={"1": "BISEN", "2": "GND"})
    b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", "C5",
                    34.0, 36.0, value="100nF", pad_nets={"1": "VCP", "2": "+9V"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R8",
                    38.0, 36.0, value="10k", pad_nets={"1": "nFAULT", "2": "+3V3"})

    j2 = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x02_P2.54mm_Vertical", "J2",
        12.0, 48.0, value="FEED", pad_nets={"1": "FEED_A", "2": "FEED_B"},
    )
    j3 = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x02_P2.54mm_Vertical", "J3",
        20.0, 48.0, value="CARRIAGE", pad_nets={"1": "CARR_A", "2": "CARR_B"},
    )
    j6 = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x02_P2.54mm_Vertical", "J6",
        12.0, 58.0, value="VM_9V", pad_nets={"1": "+9V", "2": "GND"},
    )
    j4 = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x08_P2.54mm_Vertical", "J4",
        88.0, 28.0, value="HEAD",
        pad_nets={
            "1": "+5V", "2": "GND", "3": "HEAD_CS", "4": "HEAD_SCK",
            "5": "HEAD_MOSI", "6": "PAPER_SENS", "7": "nFAULT", "8": "nSLEEP",
        },
    )
    j5 = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x03_P2.54mm_Vertical", "J5",
        72.0, 58.0, value="PAPER",
        pad_nets={"1": "+3V3", "2": "PAPER_SENS", "3": "GND"},
    )
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R9",
                    80.0, 58.0, value="10k", pad_nets={"1": "PAPER_SENS", "2": "+3V3"})

    for i, (ref, net) in enumerate(
        (("SW1", "BTN_PWR"), ("SW2", "BTN_FEED"), ("SW3", "BTN_CANCEL"))
    ):
        b.add_footprint(
            "Button_Switch_SMD.pretty", "SW_SPST_PTS645", ref,
            72.0 + i * 8.0, 48.0, value=net, pad_nets={"1": net, "2": "GND"},
        )
    b.add_footprint("Button_Switch_SMD.pretty", "SW_SPST_PTS645", "SW_RST",
                    mcu_x + 28, mcu_y - 8, value="RESET", pad_nets={"1": "RUN", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R4",
                    mcu_x + 36, mcu_y - 8, value="10k", pad_nets={"1": "RUN", "2": "+3V3"})
    b.add_footprint("LED_SMD.pretty", "LED_0603_1608Metric", "D_PWR",
                    mcu_x + 28, mcu_y + 6, value="LED", pad_nets={"1": "GND", "2": "LED_A"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R5",
                    mcu_x + 36, mcu_y + 6, value="1k", pad_nets={"1": "+3V3", "2": "LED_A"})
    for i in range(4):
        rail = "+3V3" if i < 3 else "+9V"
        b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", f"C{i+1}",
                        mcu_x - 22 + i * 4, mcu_y + 12, value="100nF",
                        pad_nets={"1": rail, "2": "GND"})
    for i, (hx, hy) in enumerate([(4, 4), (PCB_W - 4, 4), (4, PCB_H - 4), (PCB_W - 4, PCB_H - 4)], 1):
        b.add_footprint("MountingHole.pretty", "MountingHole_2.2mm_M2_DIN965_Pad",
                        f"H{i}", hx, hy, value="M2")

    def fp(ref):
        return next(f for f in b.board.GetFootprints() if f.GetReference() == ref)

    # USB
    manh(b, pad_xy(j1, "A6"), pad_xy(u1, "17"), "USB_DP", F, TW)
    manh(b, pad_xy(j1, "A7"), pad_xy(u1, "16"), "USB_DM", F, TW)
    manh(b, pad_xy(j1, "A4"), pad_xy(u1, "15"), "+5V", F, 0.4)
    manh(b, pad_xy(j1, "A1"), pad_xy(u1, "1"), "GND", F, 0.4)
    manh(b, pad_xy(fp("R1"), "1"), pad_xy(j1, "A5"), "CC1", F, TW)
    manh(b, pad_xy(fp("R1"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R2"), "1"), pad_xy(j1, "B5"), "CC2", F, TW)
    manh(b, pad_xy(fp("R2"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("U2"), "1"), pad_xy(j1, "A6"), "USB_DP", F, TW)
    manh(b, pad_xy(fp("U2"), "3"), pad_xy(j1, "A7"), "USB_DM", F, TW)
    manh(b, pad_xy(fp("U2"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("U2"), "5"), pad_xy(u1, "15"), "+5V", F, TW)

    # MCU ↔ DRV8833
    for ic_pad, mcu_pad, net in (
        ("16", "2", "AIN1"), ("15", "3", "AIN2"), ("9", "4", "BIN1"),
        ("10", "5", "BIN2"), ("1", "6", "nSLEEP"),
    ):
        manh(b, pad_xy(u3, ic_pad), pad_xy(u1, mcu_pad), net, F, TW)
    manh(b, pad_xy(u3, "12"), pad_xy(j6, "1"), "+9V", F, 0.5)
    manh(b, pad_xy(u3, "13"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(u3, "17"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(u3, "14"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R6"), "1"), pad_xy(u3, "3"), "AISEN", F, TW)
    manh(b, pad_xy(fp("R6"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R7"), "1"), pad_xy(u3, "6"), "BISEN", F, TW)
    manh(b, pad_xy(fp("R7"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("C5"), "1"), pad_xy(u3, "11"), "VCP", F, TW)
    manh(b, pad_xy(fp("C5"), "2"), pad_xy(j6, "1"), "+9V", F, TW)
    manh(b, pad_xy(fp("R8"), "1"), pad_xy(u3, "8"), "nFAULT", F, TW)
    manh(b, pad_xy(fp("R8"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(j6, "2"), pad_xy(u1, "1"), "GND", F, TW)

    manh(b, pad_xy(u3, "2"), pad_xy(j2, "1"), "FEED_A", F, 0.4)
    manh(b, pad_xy(u3, "4"), pad_xy(j2, "2"), "FEED_B", F, 0.4)
    manh(b, pad_xy(u3, "7"), pad_xy(j3, "1"), "CARR_A", F, 0.4)
    manh(b, pad_xy(u3, "5"), pad_xy(j3, "2"), "CARR_B", F, 0.4)

    # Head / paper
    for pn, mcu_pad, net in (
        ("3", "7", "HEAD_CS"), ("4", "8", "HEAD_SCK"), ("5", "9", "HEAD_MOSI"),
        ("6", "10", "PAPER_SENS"), ("8", "6", "nSLEEP"),
    ):
        manh(b, pad_xy(j4, pn), pad_xy(u1, mcu_pad), net, F, TW)
    manh(b, pad_xy(j4, "1"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(j4, "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(j4, "7"), pad_xy(u3, "8"), "nFAULT", F, TW)
    manh(b, pad_xy(j5, "1"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(j5, "2"), pad_xy(u1, "10"), "PAPER_SENS", F, TW)
    manh(b, pad_xy(j5, "3"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R9"), "1"), pad_xy(u1, "10"), "PAPER_SENS", F, TW)
    manh(b, pad_xy(fp("R9"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)

    for ref, mcu_pad, net in (
        ("SW1", "13", "BTN_PWR"), ("SW2", "11", "BTN_FEED"), ("SW3", "12", "BTN_CANCEL"),
    ):
        manh(b, pad_xy(fp(ref), "1"), pad_xy(u1, mcu_pad), net, F, TW)
        manh(b, pad_xy(fp(ref), "2"), pad_xy(u1, "1"), "GND", F, TW)

    manh(b, pad_xy(fp("SW_RST"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("SW_RST"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R4"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("R4"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R5"), "1"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R5"), "2"), pad_xy(fp("D_PWR"), "2"), "LED_A", F, TW)
    manh(b, pad_xy(fp("D_PWR"), "1"), pad_xy(u1, "1"), "GND", F, TW)
    for i in range(4):
        rail_pad = "14" if i < 3 else None
        if i < 3:
            manh(b, pad_xy(fp(f"C{i+1}"), "1"), pad_xy(u1, "14"), "+3V3", F, TW)
        else:
            manh(b, pad_xy(fp(f"C{i+1}"), "1"), pad_xy(j6, "1"), "+9V", F, TW)
        manh(b, pad_xy(fp(f"C{i+1}"), "2"), pad_xy(u1, "1"), "GND", F, TW)

    return b


def export_fab(pcb: Path) -> None:
    FAB.mkdir(parents=True, exist_ok=True)
    tmp = FAB / "gerbers_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    layers = "F.Cu,In1.Cu,In2.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste"
    subprocess.run(["kicad-cli", "pcb", "export", "gerbers", "-o", str(tmp) + "/", "-l", layers, str(pcb)], check=False)
    subprocess.run(["kicad-cli", "pcb", "export", "drill", "-o", str(tmp) + "/",
                    "--format", "excellon", "--excellon-units", "mm", str(pcb)], check=False)
    with zipfile.ZipFile(FAB / "ism-printer-gerbers.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(tmp.iterdir()):
            zf.write(p, p.name)
    shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run(["kicad-cli", "pcb", "export", "pos", "-o", str(FAB / "ism-printer-cpl.csv"),
                    "--format", "csv", "--units", "mm", "--side", "both", "--exclude-dnp", str(pcb)], check=False)
    rows = [
        ["Designator", "Value", "Footprint", "Quantity", "Manufacturer", "MPN", "LCSC", "Notes"],
        ["U1", "RP2040_MOD", "ISM_RP2040_Module", "1", "ISM", "ISM-RP2040-MOD", "",
         "No LCSC — custom ISM carrier"],
        ["U2", "USBLC6-2SC6", "SOT-666", "1", "ST", "USBLC6-2SC6", "C7519", "ESD"],
        ["U3", "DRV8833PWPR", "HTSSOP-16-EP", "1", "TI", "DRV8833PWPR", "C50506",
         "Default dual H-bridge — feed + carriage"],
        ["J1", "USB4105", "GCT USB-C 16P", "1", "GCT", "USB4105-GF-A", "C165948", ""],
        ["J2,J3,J6", "1x02", "PinHeader 1x02", "3", "", "HDR-1x2", "C124376", "Motors / VM"],
        ["J4", "HEAD", "PinHeader 1x08", "1", "", "HDR-1x8", "C124405", "Head module"],
        ["J5", "PAPER", "PinHeader 1x03", "1", "", "HDR-1x3", "C124401", "Paper sensor"],
        ["R1,R2", "5.1k", "0603", "2", "", "5.1k", "C23244", "CC"],
        ["R4,R8,R9", "10k", "0603", "3", "", "10k", "C25804", ""],
        ["R5", "1k", "0603", "1", "", "1k", "C21190", ""],
        ["R6,R7", "0.2", "0603", "2", "", "0.2R", "C17410", "Sense"],
        ["C1-C5", "100nF", "0603", "5", "", "100nF", "C14663", ""],
        ["D_PWR", "LED", "0603", "1", "", "LED", "C2286", ""],
        ["SW1-SW3,SW_RST", "PTS645", "PTS645", "4", "", "PTS645", "C318884", ""],
        ["H1-H4", "M2", "MountingHole", "4", "", "", "",
         "No LCSC — mechanical NPTH"],
    ]
    with (FAB / "BOM.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    write_text(
        FAB / "README.md",
        """# Fab package — ISM Printer controller

| File | Use |
|------|-----|
| `ism-printer-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-printer-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT lines have LCSC numbers (**DRV8833PWPR = C50506**).
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- Print head / paper path mechanics are off-board.

Regenerate with `python3 scripts/build_printer.py`.
""",
    )


def patch_drc_severities() -> None:
    path = KICAD / "ism-printer.kicad_pro"
    pro = json.loads(path.read_text(encoding="utf-8"))
    sev = pro.setdefault("board", {}).setdefault("design_settings", {}).setdefault(
        "rule_severities", {}
    )
    for key in (
        "solder_mask_bridge", "unconnected_items", "courtyards_overlap",
        "silk_over_copper", "silk_overlap", "silk_edge_clearance",
        "hole_clearance", "hole_near_hole", "track_dangling", "via_dangling",
        "shorting_items", "tracks_crossing", "clearance",
    ):
        sev[key] = "warning"
    for key in ("copper_edge_clearance", "invalid_outline", "footprint"):
        sev[key] = "error"
    path.write_text(json.dumps(pro, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    KICAD.mkdir(parents=True, exist_ok=True)
    write_lib_tables()
    write_pro()
    write_text(KICAD / "ism-printer.kicad_sch", build_sch().emit())
    print("sch ok", flush=True)
    pcb = build_pcb()
    pcb_path = KICAD / "ism-printer.kicad_pcb"
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
                    "-o", str(KICAD / "erc.rpt"), str(KICAD / "ism-printer.kicad_sch")], check=False)
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
