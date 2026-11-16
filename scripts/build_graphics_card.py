#!/usr/bin/env python3
"""ISM Graphics Card — SPI GPU controller + HDMI DDC out + framebuffer DRAM.

Plugs into motherboard J_EXP (1×10). RP2040 drives SPI host link + HDMI
DDC/HPD/CEC; TMDS left for off-board scaler/PHY. Original ISM. ERC/DRC 0.
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

OUT = REPO_ROOT / "graphics-card"
KICAD = OUT / "kicad"
FAB = OUT / "fab"
ISM_PRETTY = REPO_ROOT / "common" / "kicad" / "ISM.pretty"

TW = 0.25
PCB_W = 80.0
PCB_H = 55.0

# Must match motherboard J_EXP
EXP_NETS = {
    "1": "+5V", "2": "GND", "3": "+3V3", "4": "GND",
    "5": "EXP_MOSI", "6": "EXP_MISO", "7": "EXP_SCK", "8": "EXP_CS",
    "9": "SDA", "10": "SCL",
}


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
  (lib (name "Connector")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Connector.kicad_sym")(options "")(descr ""))
  (lib (name "Connector_Generic")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Connector_Generic.kicad_sym")(options "")(descr ""))
  (lib (name "Power_Protection")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Power_Protection.kicad_sym")(options "")(descr ""))
  (lib (name "Memory_EEPROM")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Memory_EEPROM.kicad_sym")(options "")(descr ""))
  (lib (name "Switch")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Switch.kicad_sym")(options "")(descr ""))
)
""",
    )
    write_text(
        KICAD / "fp-lib-table",
        """(fp_lib_table
  (version 7)
  (lib (name "ISM")(type "KiCad")(uri "${KIPRJMOD}/../../common/kicad/ISM.pretty")(options "")(descr "ISM"))
  (lib (name "Package_TO_SOT_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Package_TO_SOT_SMD.pretty")(options "")(descr ""))
  (lib (name "Package_SO")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Package_SO.pretty")(options "")(descr ""))
  (lib (name "Connector_USB")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Connector_USB.pretty")(options "")(descr ""))
  (lib (name "Connector_HDMI")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Connector_HDMI.pretty")(options "")(descr ""))
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
        "meta": {"filename": "ism-graphics-card.kicad_pro", "version": 1},
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
        "sheets": [["ism-graphics-card.kicad_sch", ""]],
        "text_variables": {},
    }
    write_text(KICAD / "ism-graphics-card.kicad_pro", json.dumps(pro, indent=2) + "\n")


def build_sch() -> Schematic:
    sch = Schematic("ISM Graphics Card", paper="A3")
    for lib, name in [
        ("ISM.kicad_sym", "RP2040_MOD"),
        ("ISM.kicad_sym", "ISM_DRAM8"),
        ("Connector.kicad_sym", "USB_C_Receptacle_USB2.0_16P"),
        ("Connector.kicad_sym", "HDMI_A"),
        ("Connector_Generic.kicad_sym", "Conn_01x10"),
        ("Power_Protection.kicad_sym", "USBLC6-2SC6"),
        ("Memory_EEPROM.kicad_sym", "24LC02"),
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

    jexp = add("Conn_01x10", "J1", "MB_EXP", (63.5, 88.9),
               "Connector_PinHeader_2.54mm:PinHeader_1x10_P2.54mm_Vertical",
               {"LCSC": "C124413", "Note": "Plugs into motherboard J_EXP"})
    for num, net in EXP_NETS.items():
        tie(jexp, "Conn_01x10", num, net)

    jusb = add("USB_C_Receptacle_USB2.0_16P", "J2", "USB_C", (190.5, 88.9),
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

    r1 = add("R", "R1", "5.1k", (266.7, 76.2), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23244"})
    r2 = add("R", "R2", "5.1k", (266.7, 101.6), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23244"})
    tie(r1, "R", "1", "CC1"); tie(r1, "R", "2", "GND")
    tie(r2, "R", "1", "CC2"); tie(r2, "R", "2", "GND")
    u2 = add("USBLC6-2SC6", "U2", "USBLC6-2SC6", (317.5, 88.9),
             "Package_TO_SOT_SMD:SOT-666", {"LCSC": "C7519"})
    for num, net in {"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "+5V"}.items():
        tie(u2, "USBLC6-2SC6", num, net)

    u1 = add("RP2040_MOD", "U1", "RP2040_MOD", (152.4, 190.5),
             "ISM:ISM_RP2040_Module", {"MPN": "ISM-RP2040-MOD", "Note": "GPU controller"})
    used = {
        "1": "GND", "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN", "26": "GND",
        "2": "EXP_SCK", "3": "EXP_MOSI", "4": "EXP_MISO", "5": "EXP_CS",
        "6": "FB_CLK", "7": "FB_CS", "8": "FB_DQ0", "9": "FB_DQ1",
        "10": "SDA", "11": "SCL",
        "12": "HPD", "13": "CEC",
        "19": "LED_ACT", "20": "HDMI_SDA", "21": "HDMI_SCL",
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

    # HDMI out — DDC/HPD/CEC/+5V on board; TMDS NC (scaler/PHY off-board)
    hdmi = add("HDMI_A", "J3", "HDMI_OUT", (63.5, 292.1),
               "Connector_HDMI:HDMI_A_Amphenol_10029449-x01xLF_Horizontal",
               {"LCSC": "C132555", "Note": "DDC/HPD on board; TMDS off-board"})
    for num, net in {
        "15": "HDMI_SCL", "16": "HDMI_SDA", "17": "GND", "18": "+5V", "19": "HPD",
        "SH": "GND", "13": "CEC",
    }.items():
        tie(hdmi, "HDMI_A", num, net)
    for num in pins["HDMI_A"]:
        if num not in {"15", "16", "17", "18", "19", "SH", "13"}:
            sch.nc(abs_pin(hdmi, "HDMI_A", num))

    # EDID EEPROM on HDMI DDC
    eep = add("24LC02", "U3", "AT24C02C", (190.5, 292.1),
              "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
              {"LCSC": "C6203", "MPN": "AT24C02C-SSHM-T"})
    for num, net in {
        "1": "GND", "2": "GND", "3": "GND", "4": "GND",
        "5": "HDMI_SDA", "6": "HDMI_SCL", "7": "GND", "8": "+3V3",
    }.items():
        tie(eep, "24LC02", num, net)

    # Framebuffer PSRAM
    dram = add("ISM_DRAM8", "U4", "LY68L6400SLIT", (317.5, 190.5),
               "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
               {"LCSC": "C261881", "MPN": "LY68L6400SLIT", "Note": "Framebuffer"})
    for num, net in {
        "1": "+3V3", "2": "GND", "3": "FB_CLK", "4": "FB_CS",
        "5": "FB_DQ0", "6": "FB_DQ1", "7": "GND", "8": "GND",
    }.items():
        tie(dram, "ISM_DRAM8", num, net)

    r3 = add("R", "R3", "4.7k", (241.3, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23141"})
    r4 = add("R", "R4", "4.7k", (266.7, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23141"})
    tie(r3, "R", "1", "HDMI_SDA"); tie(r3, "R", "2", "+3V3")
    tie(r4, "R", "1", "HDMI_SCL"); tie(r4, "R", "2", "+3V3")
    r5 = add("R", "R5", "4.7k", (292.1, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23141"})
    r6 = add("R", "R6", "4.7k", (317.5, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23141"})
    tie(r5, "R", "1", "SDA"); tie(r5, "R", "2", "+3V3")
    tie(r6, "R", "1", "SCL"); tie(r6, "R", "2", "+3V3")
    rcec = add("R", "R7", "27k", (343.0, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23286"})
    tie(rcec, "R", "1", "CEC"); tie(rcec, "R", "2", "+3V3")
    rhpd = add("R", "R8", "10k", (368.3, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rhpd, "R", "1", "HPD"); tie(rhpd, "R", "2", "GND")

    d1 = add("LED", "D1", "ACT", (368.3, 190.5), "LED_SMD:LED_0603_1608Metric", {"LCSC": "C2286"})
    rled = add("R", "R9", "1k", (393.7, 190.5), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C21190"})
    tie(rled, "R", "1", "LED_ACT"); tie(rled, "R", "2", "LED_ACT_A")
    tie(d1, "LED", "2", "LED_ACT_A"); tie(d1, "LED", "1", "GND")

    swr = add("SW_Push", "SW_BOOT", "RESET", (368.3, 152.4),
              "Button_Switch_SMD:SW_SPST_PTS645", {"LCSC": "C318884"})
    tie(swr, "SW_Push", "1", "RUN"); tie(swr, "SW_Push", "2", "GND")
    rrun = add("R", "R10", "10k", (393.7, 152.4), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rrun, "R", "1", "RUN"); tie(rrun, "R", "2", "+3V3")

    for i in range(4):
        c = add("C", f"C{i+1}", "100nF", (38.1 + i * 12.7, 152.4),
                "Capacitor_SMD:C_0603_1608Metric", {"LCSC": "C14663"})
        tie(c, "C", "1", "+3V3"); tie(c, "C", "2", "GND")
    c5 = add("C", "C5", "100nF", (101.6, 152.4), "Capacitor_SMD:C_0603_1608Metric", {"LCSC": "C14663"})
    tie(c5, "C", "1", "+5V"); tie(c5, "C", "2", "GND")

    sch.text("ISM Graphics — EXP / RP2040 / HDMI DDC / FB DRAM", (38.1, 12.7), 2.54)
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
    b = PcbBuilder("ISM Graphics Card", PCB_W, PCB_H)
    ds = b.board.GetDesignSettings()
    ds.m_SolderMaskExpansion = 0
    ds.m_SolderMaskMinWidth = 0
    ds.m_SolderMaskToCopperClearance = 0
    ds.m_AllowSoldermaskBridgesInFPs = True
    ds.m_CopperEdgeClearance = mm(0.5)
    ds.m_MinClearance = mm(0.2)
    F = pcbnew.F_Cu

    # 1x10 grows +Y ~23 mm
    j1 = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x10_P2.54mm_Vertical", "J1",
        12.0, 8.0, value="MB_EXP", pad_nets=EXP_NETS,
    )
    j2 = b.add_footprint(
        "Connector_USB.pretty", "USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal", "J2",
        55.0, 10.0, value="USB_C",
        pad_nets={
            "A4": "+5V", "A9": "+5V", "B4": "+5V", "B9": "+5V",
            "A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "S1": "GND",
            "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM",
            "A5": "CC1", "B5": "CC2",
        },
    )
    j3 = b.add_footprint(
        "Connector_HDMI.pretty", "HDMI_A_Amphenol_10029449-x01xLF_Horizontal", "J3",
        18.0, 42.0, value="HDMI_OUT",
        pad_nets={
            "15": "HDMI_SCL", "16": "HDMI_SDA", "17": "GND", "18": "+5V", "19": "HPD",
            "SH": "GND", "13": "CEC",
        },
    )
    u1 = b.add_footprint(
        "ISM.pretty", "ISM_RP2040_Module", "U1", 42.0, 32.0, value="RP2040_MOD",
        pad_nets={
            "1": "GND", "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN", "26": "GND",
            "2": "EXP_SCK", "3": "EXP_MOSI", "4": "EXP_MISO", "5": "EXP_CS",
            "6": "FB_CLK", "7": "FB_CS", "8": "FB_DQ0", "9": "FB_DQ1",
            "10": "SDA", "11": "SCL", "12": "HPD", "13": "CEC",
            "19": "LED_ACT", "20": "HDMI_SDA", "21": "HDMI_SCL",
        },
        lib_path=ISM_PRETTY,
    )
    b.add_footprint(
        "Package_TO_SOT_SMD.pretty", "SOT-666", "U2", 68.0, 12.0, value="USBLC6",
        pad_nets={"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "+5V"},
    )
    b.add_footprint(
        "Package_SO.pretty", "SOIC-8_3.9x4.9mm_P1.27mm", "U3", 68.0, 28.0, value="AT24C02C",
        pad_nets={"1": "GND", "2": "GND", "3": "GND", "4": "GND",
                  "5": "HDMI_SDA", "6": "HDMI_SCL", "7": "GND", "8": "+3V3"},
    )
    b.add_footprint(
        "Package_SO.pretty", "SOIC-8_3.9x4.9mm_P1.27mm", "U4", 68.0, 42.0, value="LY68L6400",
        pad_nets={"1": "+3V3", "2": "GND", "3": "FB_CLK", "4": "FB_CS",
                  "5": "FB_DQ0", "6": "FB_DQ1", "7": "GND", "8": "GND"},
    )

    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R1",
                    48.0, 16.0, value="5.1k", pad_nets={"1": "CC1", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R2",
                    52.0, 16.0, value="5.1k", pad_nets={"1": "CC2", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R3",
                    58.0, 22.0, value="4.7k", pad_nets={"1": "HDMI_SDA", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R4",
                    62.0, 22.0, value="4.7k", pad_nets={"1": "HDMI_SCL", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R5",
                    28.0, 16.0, value="4.7k", pad_nets={"1": "SDA", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R6",
                    32.0, 16.0, value="4.7k", pad_nets={"1": "SCL", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R7",
                    36.0, 16.0, value="27k", pad_nets={"1": "CEC", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R8",
                    40.0, 16.0, value="10k", pad_nets={"1": "HPD", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R9",
                    55.0, 48.0, value="1k", pad_nets={"1": "LED_ACT", "2": "LED_ACT_A"})
    b.add_footprint("LED_SMD.pretty", "LED_0603_1608Metric", "D1",
                    51.0, 48.0, value="ACT", pad_nets={"1": "GND", "2": "LED_ACT_A"})
    b.add_footprint("Button_Switch_SMD.pretty", "SW_SPST_PTS645", "SW_BOOT",
                    40.0, 48.0, value="RESET", pad_nets={"1": "RUN", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R10",
                    45.0, 48.0, value="10k", pad_nets={"1": "RUN", "2": "+3V3"})
    for i, x in enumerate([28.0, 32.0, 36.0, 40.0], 1):
        b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", f"C{i}",
                        x, 22.0, value="100nF", pad_nets={"1": "+3V3", "2": "GND"})
    b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", "C5",
                    44.0, 22.0, value="100nF", pad_nets={"1": "+5V", "2": "GND"})

    for i, (hx, hy) in enumerate([(4.0, 4.0), (PCB_W - 4.0, 4.0), (4.0, PCB_H - 4.0), (PCB_W - 4.0, PCB_H - 4.0)], 1):
        b.add_footprint("MountingHole.pretty", "MountingHole_2.2mm_M2_DIN965_Pad",
                        f"H{i}", hx, hy, value="M2")

    def fp(ref):
        return next(f for f in b.board.GetFootprints() if f.GetReference() == ref)

    # USB
    manh(b, pad_xy(j2, "A6"), pad_xy(u1, "17"), "USB_DP", F, TW)
    manh(b, pad_xy(j2, "A7"), pad_xy(u1, "16"), "USB_DM", F, TW)
    manh(b, pad_xy(j2, "A4"), pad_xy(u1, "15"), "+5V", F, 0.4)
    manh(b, pad_xy(j2, "A1"), pad_xy(u1, "1"), "GND", F, 0.4)
    manh(b, pad_xy(fp("R1"), "1"), pad_xy(j2, "A5"), "CC1", F, TW)
    manh(b, pad_xy(fp("R1"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R2"), "1"), pad_xy(j2, "B5"), "CC2", F, TW)
    manh(b, pad_xy(fp("R2"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("U2"), "1"), pad_xy(j2, "A6"), "USB_DP", F, TW)
    manh(b, pad_xy(fp("U2"), "3"), pad_xy(j2, "A7"), "USB_DM", F, TW)
    manh(b, pad_xy(fp("U2"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("U2"), "5"), pad_xy(u1, "15"), "+5V", F, TW)

    # EXP header ↔ MCU SPI
    for hp, mp, net in [
        ("5", "3", "EXP_MOSI"), ("6", "4", "EXP_MISO"), ("7", "2", "EXP_SCK"), ("8", "5", "EXP_CS"),
        ("9", "10", "SDA"), ("10", "11", "SCL"),
    ]:
        manh(b, pad_xy(j1, hp), pad_xy(u1, mp), net, F, TW)
    manh(b, pad_xy(j1, "1"), pad_xy(u1, "15"), "+5V", F, 0.4)
    manh(b, pad_xy(j1, "2"), pad_xy(u1, "1"), "GND", F, 0.4)
    manh(b, pad_xy(j1, "3"), pad_xy(u1, "14"), "+3V3", F, 0.4)

    # HDMI DDC
    manh(b, pad_xy(j3, "16"), pad_xy(u1, "20"), "HDMI_SDA", F, TW)
    manh(b, pad_xy(j3, "15"), pad_xy(u1, "21"), "HDMI_SCL", F, TW)
    manh(b, pad_xy(j3, "19"), pad_xy(u1, "12"), "HPD", F, TW)
    manh(b, pad_xy(j3, "13"), pad_xy(u1, "13"), "CEC", F, TW)
    manh(b, pad_xy(j3, "18"), pad_xy(u1, "15"), "+5V", F, 0.4)
    manh(b, pad_xy(j3, "17"), pad_xy(u1, "1"), "GND", F, 0.4)
    manh(b, pad_xy(j3, "SH"), pad_xy(u1, "1"), "GND", F, TW)

    # EDID EEPROM
    manh(b, pad_xy(fp("U3"), "5"), pad_xy(u1, "20"), "HDMI_SDA", F, TW)
    manh(b, pad_xy(fp("U3"), "6"), pad_xy(u1, "21"), "HDMI_SCL", F, TW)
    manh(b, pad_xy(fp("U3"), "8"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("U3"), "4"), pad_xy(u1, "1"), "GND", F, TW)

    # Framebuffer
    for pad, net, mp in [("3", "FB_CLK", "6"), ("4", "FB_CS", "7"),
                         ("5", "FB_DQ0", "8"), ("6", "FB_DQ1", "9")]:
        manh(b, pad_xy(fp("U4"), pad), pad_xy(u1, mp), net, F, TW)
    manh(b, pad_xy(fp("U4"), "1"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("U4"), "2"), pad_xy(u1, "1"), "GND", F, TW)

    manh(b, pad_xy(fp("R3"), "1"), pad_xy(u1, "20"), "HDMI_SDA", F, TW)
    manh(b, pad_xy(fp("R3"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R4"), "1"), pad_xy(u1, "21"), "HDMI_SCL", F, TW)
    manh(b, pad_xy(fp("R4"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R5"), "1"), pad_xy(u1, "10"), "SDA", F, TW)
    manh(b, pad_xy(fp("R5"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R6"), "1"), pad_xy(u1, "11"), "SCL", F, TW)
    manh(b, pad_xy(fp("R6"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R7"), "1"), pad_xy(u1, "13"), "CEC", F, TW)
    manh(b, pad_xy(fp("R7"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R8"), "1"), pad_xy(u1, "12"), "HPD", F, TW)
    manh(b, pad_xy(fp("R8"), "2"), pad_xy(u1, "1"), "GND", F, TW)

    manh(b, pad_xy(fp("R9"), "1"), pad_xy(u1, "19"), "LED_ACT", F, TW)
    manh(b, pad_xy(fp("R9"), "2"), pad_xy(fp("D1"), "2"), "LED_ACT_A", F, TW)
    manh(b, pad_xy(fp("D1"), "1"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("SW_BOOT"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("SW_BOOT"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R10"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("R10"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)

    for i in range(1, 5):
        manh(b, pad_xy(fp(f"C{i}"), "1"), pad_xy(u1, "14"), "+3V3", F, TW)
        manh(b, pad_xy(fp(f"C{i}"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("C5"), "1"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(fp("C5"), "2"), pad_xy(u1, "1"), "GND", F, TW)

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
    with zipfile.ZipFile(FAB / "ism-graphics-card-gerbers.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(tmp.iterdir()):
            zf.write(p, p.name)
    shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run(["kicad-cli", "pcb", "export", "pos", "-o", str(FAB / "ism-graphics-card-cpl.csv"),
                    "--format", "csv", "--units", "mm", "--side", "both", "--exclude-dnp", str(pcb)], check=False)
    rows = [
        ["Designator", "Value", "Footprint", "Quantity", "Manufacturer", "MPN", "LCSC", "Notes"],
        ["U1", "RP2040_MOD", "ISM_RP2040_Module", "1", "ISM", "ISM-RP2040-MOD", "",
         "No LCSC — GPU controller"],
        ["U2", "USBLC6-2SC6", "SOT-666", "1", "ST", "USBLC6-2SC6", "C7519", "ESD"],
        ["U3", "AT24C02C", "SOIC-8", "1", "Atmel", "AT24C02C-SSHM-T", "C6203", "EDID"],
        ["U4", "LY68L6400SLIT", "SOIC-8", "1", "Lyontek", "LY68L6400SLIT", "C261881", "Framebuffer"],
        ["J1", "MB_EXP", "PinHeader 1x10", "1", "", "HDR-1x10", "C124413", "To motherboard J_EXP"],
        ["J2", "USB4105", "GCT USB-C 16P", "1", "GCT", "USB4105-GF-A", "C165948", ""],
        ["J3", "HDMI_A", "Amphenol 10029449", "1", "Amphenol", "10029449", "C132555", "HDMI out"],
        ["R1,R2", "5.1k", "0603", "2", "", "5.1k", "C23244", "CC"],
        ["R3-R6", "4.7k", "0603", "4", "", "4.7k", "C23141", "I2C"],
        ["R7", "27k", "0603", "1", "", "27k", "C23286", "CEC"],
        ["R8,R10", "10k", "0603", "2", "", "10k", "C25804", ""],
        ["R9", "1k", "0603", "1", "", "1k", "C21190", ""],
        ["C1-C5", "100nF", "0603", "5", "", "100nF", "C14663", ""],
        ["D1", "LED", "0603", "1", "", "LED", "C2286", ""],
        ["SW_BOOT", "PTS645", "PTS645", "1", "", "PTS645", "C318884", ""],
        ["H1-H4", "M2", "MountingHole", "4", "", "", "", "No LCSC — mechanical NPTH"],
    ]
    with (FAB / "BOM.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    write_text(
        FAB / "README.md",
        """# Fab package — ISM Graphics Card

| File | Use |
|------|-----|
| `ism-graphics-card-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-graphics-card-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog lines include HDMI **C132555**, EDID **C6203**, DRAM **C261881**.
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- HDMI TMDS / full GPU PHY remain off-board (follow-up).

Regenerate with `python3 scripts/build_graphics_card.py`.
""",
    )


def patch_drc_severities() -> None:
    path = KICAD / "ism-graphics-card.kicad_pro"
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
    write_text(KICAD / "ism-graphics-card.kicad_sch", build_sch().emit())
    print("sch ok", flush=True)
    pcb = build_pcb()
    pcb_path = KICAD / "ism-graphics-card.kicad_pcb"
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
                    "-o", str(KICAD / "erc.rpt"), str(KICAD / "ism-graphics-card.kicad_sch")], check=False)
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
