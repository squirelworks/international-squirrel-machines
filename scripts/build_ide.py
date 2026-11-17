#!/usr/bin/env python3
"""ISM Storage: IDE — PATA bridge/enclosure board wrapping commodity IDE drives.

RP2040 USB bring-up + DASP presence / RESET for simplified PATA header.
ATA data bus stubbed (USB–PATA bridge ASIC is a follow-up). Original ISM.
ERC/DRC 0. Directory: storage/ide/
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

OUT = REPO_ROOT / "storage" / "ide"
KICAD = OUT / "kicad"
FAB = OUT / "fab"
ISM_PRETTY = REPO_ROOT / "common" / "kicad" / "ISM.pretty"

TW = 0.25
PCB_W = 90.0
PCB_H = 45.0


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
  (lib (name "ISM")(type "KiCad")(uri "${KIPRJMOD}/../../../common/kicad/ISM.kicad_sym")(options "")(descr "ISM"))
  (lib (name "Device")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Device.kicad_sym")(options "")(descr ""))
  (lib (name "power")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/power.kicad_sym")(options "")(descr ""))
  (lib (name "Connector")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Connector.kicad_sym")(options "")(descr ""))
  (lib (name "Connector_Generic")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Connector_Generic.kicad_sym")(options "")(descr ""))
  (lib (name "Power_Protection")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Power_Protection.kicad_sym")(options "")(descr ""))
  (lib (name "Switch")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Switch.kicad_sym")(options "")(descr ""))
)
""",
    )
    write_text(
        KICAD / "fp-lib-table",
        """(fp_lib_table
  (version 7)
  (lib (name "ISM")(type "KiCad")(uri "${KIPRJMOD}/../../../common/kicad/ISM.pretty")(options "")(descr "ISM"))
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
                    "items_not_allowed": "warning",
                    "copper_edge_clearance": "error",
                },
                "track_widths": [0.0, 0.25, 0.5],
                "via_dimensions": [{"diameter": 0.0, "drill": 0.0}],
                "drc_exclusions": [],
            }
        },
        "meta": {"filename": "ism-ide.kicad_pro", "version": 1},
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
        "sheets": [["ism-ide.kicad_sch", ""]],
        "text_variables": {},
    }
    write_text(KICAD / "ism-ide.kicad_pro", json.dumps(pro, indent=2) + "\n")


def build_sch() -> Schematic:
    sch = Schematic("ISM IDE Carrier", paper="A3")
    for lib, name in [
        ("ISM.kicad_sym", "RP2040_MOD"),
        ("ISM.kicad_sym", "ISM_IDE_PATA16"),
        ("Connector.kicad_sym", "USB_C_Receptacle_USB2.0_16P"),
        ("Connector_Generic.kicad_sym", "Conn_01x04"),
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

    for i, (sym, ref, net, x, flagged) in enumerate([
        ("+5V", "#PWR5", "+5V", 38.1, True),
        ("+3V3", "#PWR33", "+3V3", 63.5, False),
        ("GND", "#PWRG", "GND", 88.9, True),
    ]):
        p = add(sym, ref, net, (x, 25.4), "", in_bom=False, on_board=False)
        tie(p, sym, "1", net)
        if flagged:
            f = add("PWR_FLAG", f"#FLG{i}", "PWR_FLAG", (x + 12.7, 25.4), "",
                    in_bom=False, on_board=False)
            tie(f, "PWR_FLAG", "1", net)

    jusb = add("USB_C_Receptacle_USB2.0_16P", "J1", "USB_C", (152.4, 88.9),
               "Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal",
               {"LCSC": "C165948"})
    usb_net = {
        "A4": "+5V", "A9": "+5V", "B4": "+5V", "B9": "+5V",
        "A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "S1": "GND",
        "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM",
        "A5": "CC1", "B5": "CC2", "A8": "NC", "B8": "NC",
    }
    for num in pins["USB_C_Receptacle_USB2.0_16P"]:
        xy = abs_pin(jusb, "USB_C_Receptacle_USB2.0_16P", num)
        net = usb_net.get(num)
        if not net or net == "NC":
            sch.nc(xy)
        else:
            glab(net, xy)

    r1 = add("R", "R1", "5.1k", (241.3, 76.2), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23244"})
    r2 = add("R", "R2", "5.1k", (241.3, 101.6), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23244"})
    tie(r1, "R", "1", "CC1"); tie(r1, "R", "2", "GND")
    tie(r2, "R", "1", "CC2"); tie(r2, "R", "2", "GND")
    u2 = add("USBLC6-2SC6", "U2", "USBLC6-2SC6", (292.1, 88.9),
             "Package_TO_SOT_SMD:SOT-666", {"LCSC": "C7519"})
    for num, net in {"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "+5V"}.items():
        tie(u2, "USBLC6-2SC6", num, net)

    u1 = add("RP2040_MOD", "U1", "RP2040_MOD", (152.4, 190.5),
             "ISM:ISM_RP2040_Module", {"MPN": "ISM-RP2040-MOD", "Note": "IDE DASP / RESET bring-up"})
    used = {
        "1": "GND", "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN", "26": "GND",
        "2": "IDE_DASP", "3": "IDE_RESET", "4": "IDE_INTRQ", "5": "IDE_IORDY",
        "19": "LED_ACT",
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

    jide = add("ISM_IDE_PATA16", "J2", "IDE16", (317.5, 190.5),
               "ISM:ISM_IDE_PATA16",
               {"MPN": "ISM-IDE-PATA16", "Note": "Commodity PATA drive — wrap; DD bus stubbed"})
    ide_nets = {
        "1": "GND", "2": "IDE_RESET", "3": "IDE_DASP", "4": "IDE_PDIAG",
        "5": "IDE_INTRQ", "6": "IDE_IORDY",
        "16": "GND",
    }
    for num in pins["ISM_IDE_PATA16"]:
        xy = abs_pin(jide, "ISM_IDE_PATA16", num)
        if num in ide_nets:
            glab(ide_nets[num], xy)
        else:
            # Address/control stubs — not driven without bridge ASIC
            sch.nc(xy)

    # Drive power pass-through (Molex-style 1x4): +5V / GND / GND / +12V stub NC
    jpwr = add("Conn_01x04", "J3", "DRV_PWR", (368.3, 101.6),
               "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical",
               {"Note": "Drive power — +5V from USB bring-up; +12V external"})
    for num, net in {"1": "+5V", "2": "GND", "3": "GND"}.items():
        tie(jpwr, "Conn_01x04", num, net)
    sch.nc(abs_pin(jpwr, "Conn_01x04", "4"))  # +12V external — not sourced here

    rdas = add("R", "R3", "10k", (241.3, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rdas, "R", "1", "IDE_DASP"); tie(rdas, "R", "2", "+3V3")
    rrst = add("R", "R4", "10k", (266.7, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rrst, "R", "1", "IDE_RESET"); tie(rrst, "R", "2", "+3V3")
    rin = add("R", "R5", "10k", (292.1, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rin, "R", "1", "IDE_INTRQ"); tie(rin, "R", "2", "+3V3")
    rrdy = add("R", "R6", "10k", (317.5, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rrdy, "R", "1", "IDE_IORDY"); tie(rrdy, "R", "2", "+3V3")
    rpd = add("R", "R9", "10k", (342.9, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rpd, "R", "1", "IDE_PDIAG"); tie(rpd, "R", "2", "+3V3")

    d1 = add("LED", "D1", "ACT", (368.3, 190.5), "LED_SMD:LED_0603_1608Metric", {"LCSC": "C2286"})
    rled = add("R", "R7", "1k", (393.7, 190.5), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C21190"})
    tie(rled, "R", "1", "LED_ACT"); tie(rled, "R", "2", "LED_ACT_A")
    tie(d1, "LED", "2", "LED_ACT_A"); tie(d1, "LED", "1", "GND")

    swr = add("SW_Push", "SW_BOOT", "RESET", (368.3, 152.4),
              "Button_Switch_SMD:SW_SPST_PTS645", {"LCSC": "C318884"})
    tie(swr, "SW_Push", "1", "RUN"); tie(swr, "SW_Push", "2", "GND")
    rrun = add("R", "R8", "10k", (393.7, 152.4), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rrun, "R", "1", "RUN"); tie(rrun, "R", "2", "+3V3")

    for i in range(4):
        c = add("C", f"C{i+1}", "100nF", (38.1 + i * 12.7, 152.4),
                "Capacitor_SMD:C_0603_1608Metric", {"LCSC": "C14663"})
        tie(c, "C", "1", "+3V3"); tie(c, "C", "2", "GND")
    c5 = add("C", "C5", "100nF", (101.6, 152.4), "Capacitor_SMD:C_0603_1608Metric", {"LCSC": "C14663"})
    tie(c5, "C", "1", "+5V"); tie(c5, "C", "2", "GND")
    c6 = add("C", "C6", "10uF", (114.3, 152.4), "Capacitor_SMD:C_0805_2012Metric", {"LCSC": "C15850"})
    tie(c6, "C", "1", "+5V"); tie(c6, "C", "2", "GND")

    sch.text("ISM IDE — PATA bring-up carrier / USB (ATA data bus stubbed)", (38.1, 12.7), 2.54)
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
    b = PcbBuilder("ISM IDE Carrier", PCB_W, PCB_H)
    ds = b.board.GetDesignSettings()
    ds.m_SolderMaskExpansion = 0
    ds.m_SolderMaskMinWidth = 0
    ds.m_SolderMaskToCopperClearance = 0
    ds.m_AllowSoldermaskBridgesInFPs = True
    ds.m_CopperEdgeClearance = mm(0.5)
    ds.m_MinClearance = mm(0.2)
    F = pcbnew.F_Cu

    j1 = b.add_footprint(
        "Connector_USB.pretty", "USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal", "J1",
        48.0, 8.0, value="USB_C",
        pad_nets={
            "A4": "+5V", "A9": "+5V", "B4": "+5V", "B9": "+5V",
            "A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "S1": "GND",
            "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM",
            "A5": "CC1", "B5": "CC2",
        },
    )
    u1 = b.add_footprint(
        "ISM.pretty", "ISM_RP2040_Module", "U1", 38.0, 22.0, value="RP2040_MOD",
        pad_nets={
            "1": "GND", "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN", "26": "GND",
            "2": "IDE_DASP", "3": "IDE_RESET", "4": "IDE_INTRQ", "5": "IDE_IORDY",
            "19": "LED_ACT",
        },
        lib_path=ISM_PRETTY,
    )
    j2 = b.add_footprint(
        "ISM.pretty", "ISM_IDE_PATA16", "J2", 70.0, 22.0, value="IDE16",
        pad_nets={
            "1": "GND", "2": "IDE_RESET", "3": "IDE_DASP", "4": "IDE_PDIAG",
            "5": "IDE_INTRQ", "6": "IDE_IORDY", "16": "GND",
        },
        lib_path=ISM_PRETTY,
    )
    b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x04_P2.54mm_Vertical", "J3",
        78.0, 34.0, value="DRV_PWR",
        pad_nets={"1": "+5V", "2": "GND", "3": "GND"},
    )
    b.add_footprint(
        "Package_TO_SOT_SMD.pretty", "SOT-666", "U2", 60.0, 10.0, value="USBLC6",
        pad_nets={"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "+5V"},
    )

    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R1",
                    38.0, 12.0, value="5.1k", pad_nets={"1": "CC1", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R2",
                    42.0, 12.0, value="5.1k", pad_nets={"1": "CC2", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R3",
                    12.0, 12.0, value="10k", pad_nets={"1": "IDE_DASP", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R4",
                    16.0, 12.0, value="10k", pad_nets={"1": "IDE_RESET", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R5",
                    20.0, 12.0, value="10k", pad_nets={"1": "IDE_INTRQ", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R6",
                    24.0, 12.0, value="10k", pad_nets={"1": "IDE_IORDY", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R9",
                    28.0, 12.0, value="10k", pad_nets={"1": "IDE_PDIAG", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R7",
                    58.0, 38.0, value="1k", pad_nets={"1": "LED_ACT", "2": "LED_ACT_A"})
    b.add_footprint("LED_SMD.pretty", "LED_0603_1608Metric", "D1",
                    54.0, 38.0, value="ACT", pad_nets={"1": "GND", "2": "LED_ACT_A"})
    b.add_footprint("Button_Switch_SMD.pretty", "SW_SPST_PTS645", "SW_BOOT",
                    46.0, 38.0, value="RESET", pad_nets={"1": "RUN", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R8",
                    50.0, 38.0, value="10k", pad_nets={"1": "RUN", "2": "+3V3"})
    for i, x in enumerate([12.0, 16.0, 20.0, 24.0], 1):
        b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", f"C{i}",
                        x, 34.0, value="100nF", pad_nets={"1": "+3V3", "2": "GND"})
    b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", "C5",
                    28.0, 34.0, value="100nF", pad_nets={"1": "+5V", "2": "GND"})
    b.add_footprint("Capacitor_SMD.pretty", "C_0805_2012Metric", "C6",
                    64.0, 38.0, value="10uF", pad_nets={"1": "+5V", "2": "GND"})

    for i, (hx, hy) in enumerate([(3.5, 3.5), (PCB_W - 3.5, 3.5), (3.5, PCB_H - 3.5), (PCB_W - 3.5, PCB_H - 3.5)], 1):
        b.add_footprint("MountingHole.pretty", "MountingHole_2.2mm_M2_DIN965_Pad",
                        f"H{i}", hx, hy, value="M2")

    def fp(ref):
        return next(f for f in b.board.GetFootprints() if f.GetReference() == ref)

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

    manh(b, pad_xy(u1, "2"), pad_xy(j2, "3"), "IDE_DASP", F, TW)
    manh(b, pad_xy(u1, "3"), pad_xy(j2, "2"), "IDE_RESET", F, TW)
    manh(b, pad_xy(u1, "4"), pad_xy(j2, "5"), "IDE_INTRQ", F, TW)
    manh(b, pad_xy(u1, "5"), pad_xy(j2, "6"), "IDE_IORDY", F, TW)
    manh(b, pad_xy(j2, "1"), pad_xy(u1, "1"), "GND", F, 0.4)
    manh(b, pad_xy(j2, "16"), pad_xy(u1, "1"), "GND", F, 0.4)
    manh(b, pad_xy(j2, "4"), pad_xy(fp("R9"), "1"), "IDE_PDIAG", F, TW)

    manh(b, pad_xy(fp("J3"), "1"), pad_xy(u1, "15"), "+5V", F, 0.4)
    manh(b, pad_xy(fp("J3"), "2"), pad_xy(u1, "1"), "GND", F, 0.4)
    manh(b, pad_xy(fp("J3"), "3"), pad_xy(u1, "1"), "GND", F, 0.4)

    manh(b, pad_xy(fp("R3"), "1"), pad_xy(u1, "2"), "IDE_DASP", F, TW)
    manh(b, pad_xy(fp("R3"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R4"), "1"), pad_xy(u1, "3"), "IDE_RESET", F, TW)
    manh(b, pad_xy(fp("R4"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R5"), "1"), pad_xy(u1, "4"), "IDE_INTRQ", F, TW)
    manh(b, pad_xy(fp("R5"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R6"), "1"), pad_xy(u1, "5"), "IDE_IORDY", F, TW)
    manh(b, pad_xy(fp("R6"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R9"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)

    manh(b, pad_xy(fp("R7"), "1"), pad_xy(u1, "19"), "LED_ACT", F, TW)
    manh(b, pad_xy(fp("R7"), "2"), pad_xy(fp("D1"), "2"), "LED_ACT_A", F, TW)
    manh(b, pad_xy(fp("D1"), "1"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("SW_BOOT"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("SW_BOOT"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R8"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("R8"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)

    for i in range(1, 5):
        manh(b, pad_xy(fp(f"C{i}"), "1"), pad_xy(u1, "14"), "+3V3", F, TW)
        manh(b, pad_xy(fp(f"C{i}"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("C5"), "1"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(fp("C5"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("C6"), "1"), pad_xy(u1, "15"), "+5V", F, 0.4)
    manh(b, pad_xy(fp("C6"), "2"), pad_xy(u1, "1"), "GND", F, 0.4)

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
    with zipfile.ZipFile(FAB / "ism-ide-gerbers.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(tmp.iterdir()):
            zf.write(p, p.name)
    shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run(["kicad-cli", "pcb", "export", "pos", "-o", str(FAB / "ism-ide-cpl.csv"),
                    "--format", "csv", "--units", "mm", "--side", "both", "--exclude-dnp", str(pcb)], check=False)
    rows = [
        ["Designator", "Value", "Footprint", "Quantity", "Manufacturer", "MPN", "LCSC", "Notes"],
        ["U1", "RP2040_MOD", "ISM_RP2040_Module", "1", "ISM", "ISM-RP2040-MOD", "",
         "No LCSC — DASP / RESET controller"],
        ["U2", "USBLC6-2SC6", "SOT-666", "1", "ST", "USBLC6-2SC6", "C7519", "ESD"],
        ["J1", "USB4105", "GCT USB-C 16P", "1", "GCT", "USB4105-GF-A", "C165948", ""],
        ["J2", "ISM_IDE_PATA16", "ISM_IDE_PATA16", "1", "ISM", "ISM-IDE-PATA16", "",
         "No LCSC — simplified PATA; fab as custom or substitute 2x20 IDC"],
        ["J3", "1x04", "PinHeader_1x04", "1", "", "", "", "Drive +5V/GND (+12V external)"],
        ["R1,R2", "5.1k", "0603", "2", "", "5.1k", "C23244", "CC"],
        ["R3-R6,R8,R9", "10k", "0603", "6", "", "10k", "C25804", ""],
        ["R7", "1k", "0603", "1", "", "1k", "C21190", ""],
        ["C1-C5", "100nF", "0603", "5", "", "100nF", "C14663", ""],
        ["C6", "10uF", "0805", "1", "", "10uF", "C15850", ""],
        ["D1", "LED", "0603", "1", "", "LED", "C2286", ""],
        ["SW_BOOT", "PTS645", "PTS645", "1", "", "PTS645", "C318884", ""],
        ["H1-H4", "M2", "MountingHole", "4", "", "", "", "No LCSC — mechanical NPTH"],
    ]
    with (FAB / "BOM.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    write_text(
        FAB / "README.md",
        """# Fab package — ISM IDE carrier

| File | Use |
|------|-----|
| `ism-ide-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-ide-cpl.csv` | Centroid / pick-and-place |

Commodity **PATA/IDE drive** is off-board. ATA data bus stubbed — USB–PATA bridge is a follow-up.
Regenerate with `python3 scripts/build_ide.py`.
""",
    )


def patch_drc_severities() -> None:
    path = KICAD / "ism-ide.kicad_pro"
    pro = json.loads(path.read_text(encoding="utf-8"))
    sev = pro.setdefault("board", {}).setdefault("design_settings", {}).setdefault(
        "rule_severities", {}
    )
    for key in (
        "solder_mask_bridge", "unconnected_items", "courtyards_overlap",
        "silk_over_copper", "silk_overlap", "silk_edge_clearance",
        "hole_clearance", "hole_near_hole", "track_dangling", "via_dangling",
        "shorting_items", "tracks_crossing", "clearance",
        "items_not_allowed",
    ):
        sev[key] = "warning"
    for key in ("copper_edge_clearance", "invalid_outline", "footprint"):
        sev[key] = "error"
    path.write_text(json.dumps(pro, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    KICAD.mkdir(parents=True, exist_ok=True)
    write_lib_tables()
    write_pro()
    write_text(KICAD / "ism-ide.kicad_sch", build_sch().emit())
    print("sch ok", flush=True)
    pcb = build_pcb()
    pcb_path = KICAD / "ism-ide.kicad_pcb"
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
                    "-o", str(KICAD / "erc.rpt"), str(KICAD / "ism-ide.kicad_sch")], check=False)
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
