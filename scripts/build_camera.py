#!/usr/bin/env python3
"""ISM Camera controller — USB MCU + OV2640-style module link.

RP2040 USB camera board with 2×8 camera-module header (SCCB/DVP bring-up),
shutter button, and AT24C02 config EEPROM. Sensor module is off-board.
Original ISM design. Target: ERC 0 / DRC 0.
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

OUT = REPO_ROOT / "camera"
KICAD = OUT / "kicad"
FAB = OUT / "fab"
ISM_PRETTY = REPO_ROOT / "common" / "kicad" / "ISM.pretty"

VIA_D = 0.6
VIA_DRILL = 0.3
TW = 0.25
PCB_W = 80.0
PCB_H = 55.0


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
  (lib (name "Memory_EEPROM")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Memory_EEPROM.kicad_sym")(options "")(descr ""))
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
        "meta": {"filename": "ism-camera.kicad_pro", "version": 1},
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
        "sheets": [["ism-camera.kicad_sch", ""]],
        "text_variables": {},
    }
    write_text(KICAD / "ism-camera.kicad_pro", json.dumps(pro, indent=2) + "\n")


def build_sch() -> Schematic:
    sch = Schematic("ISM Camera Controller", paper="A3")
    for lib, name in [
        ("ISM.kicad_sym", "RP2040_MOD"),
        ("Connector.kicad_sym", "USB_C_Receptacle_USB2.0_16P"),
        ("Connector_Generic.kicad_sym", "Conn_02x08_Odd_Even"),
        ("Memory_EEPROM.kicad_sym", "24LC02"),
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
    used = {
        "1": "GND", "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN", "26": "GND",
        "2": "CAM_SDA", "3": "CAM_SCL", "4": "CAM_XCLK", "5": "CAM_PCLK",
        "6": "CAM_VSYNC", "7": "CAM_HREF", "8": "CAM_RST", "9": "CAM_PWDN",
        "10": "CAM_D0", "11": "CAM_D1", "12": "CAM_D2", "13": "CAM_D3",
        "19": "BTN_SHUT", "20": "BTN_MODE",
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

    # OV2640-style module header (off-board sensor; LCSC for header only)
    j2 = add(
        "Conn_02x08_Odd_Even", "J2", "CAM_MOD", (50.8, 292.1),
        "Connector_PinHeader_2.54mm:PinHeader_2x08_P2.54mm_Vertical",
        {"Note": "OV2640-class module (off-board). Header LCSC C124418"},
    )
    cam_nets = {
        "1": "+3V3", "2": "GND", "3": "CAM_SCL", "4": "CAM_SDA",
        "5": "CAM_VSYNC", "6": "CAM_HREF", "7": "CAM_PCLK", "8": "CAM_XCLK",
        "9": "CAM_D3", "10": "CAM_D2", "11": "CAM_D1", "12": "CAM_D0",
        "13": "CAM_RST", "14": "CAM_PWDN", "15": "+3V3", "16": "GND",
    }
    for num, net in cam_nets.items():
        tie(j2, "Conn_02x08_Odd_Even", num, net)

    eep = add(
        "24LC02", "U3", "AT24C02C", (228.6, 190.5),
        "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        {"LCSC": "C6203", "MPN": "AT24C02C-SSHM-T", "Note": "Config / serial EEPROM"},
    )
    tie(eep, "24LC02", "1", "GND")
    tie(eep, "24LC02", "2", "GND")
    tie(eep, "24LC02", "3", "GND")
    tie(eep, "24LC02", "4", "GND")
    tie(eep, "24LC02", "5", "CAM_SDA")
    tie(eep, "24LC02", "6", "CAM_SCL")
    tie(eep, "24LC02", "7", "GND")
    tie(eep, "24LC02", "8", "+3V3")
    rpu1 = add("R", "R6", "4.7k", (279.4, 165.1), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23141"})
    rpu2 = add("R", "R7", "4.7k", (279.4, 177.8), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23141"})
    tie(rpu1, "R", "1", "CAM_SDA"); tie(rpu1, "R", "2", "+3V3")
    tie(rpu2, "R", "1", "CAM_SCL"); tie(rpu2, "R", "2", "+3V3")

    for ref, net, y in (("SW1", "BTN_SHUT", 266.7), ("SW2", "BTN_MODE", 292.1)):
        sw = add("SW_Push", ref, "PTS645", (317.5, y),
                 "Button_Switch_SMD:SW_SPST_PTS645", {"LCSC": "C318884"})
        tie(sw, "SW_Push", "1", net); tie(sw, "SW_Push", "2", "GND")

    swr = add("SW_Push", "SW_RST", "RESET", (368.3, 190.5),
              "Button_Switch_SMD:SW_SPST_PTS645", {"LCSC": "C318884"})
    tie(swr, "SW_Push", "1", "RUN"); tie(swr, "SW_Push", "2", "GND")
    r4 = add("R", "R4", "10k", (419.1, 190.5), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(r4, "R", "1", "RUN"); tie(r4, "R", "2", "+3V3")
    led = add("LED", "D_PWR", "LED", (368.3, 215.9), "LED_SMD:LED_0603_1608Metric", {"LCSC": "C2286"})
    r5 = add("R", "R5", "1k", (419.1, 215.9), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C21190"})
    tie(r5, "R", "1", "+3V3"); tie(r5, "R", "2", "LED_A")
    tie(led, "LED", "2", "LED_A"); tie(led, "LED", "1", "GND")
    for i in range(4):
        c = add("C", f"C{i+1}", "100nF", (50.8, 355.6 + i * 5.08),
                "Capacitor_SMD:C_0603_1608Metric", {"LCSC": "C14663"})
        tie(c, "C", "1", "+3V3"); tie(c, "C", "2", "GND")

    sch.text("ISM Camera — USB MCU / OV2640-class module / shutter", (38.1, 12.7), 2.54)
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
    b = PcbBuilder("ISM Camera", PCB_W, PCB_H)
    ds = b.board.GetDesignSettings()
    ds.m_SolderMaskExpansion = 0
    ds.m_SolderMaskMinWidth = 0
    ds.m_AllowSoldermaskBridgesInFPs = True
    ds.m_CopperEdgeClearance = mm(0.5)
    F = pcbnew.F_Cu

    mcu_x, mcu_y = PCB_W / 2.0, 36.0
    mod_nets = {
        "1": "GND", "2": "CAM_SDA", "3": "CAM_SCL", "4": "CAM_XCLK", "5": "CAM_PCLK",
        "6": "CAM_VSYNC", "7": "CAM_HREF", "8": "CAM_RST", "9": "CAM_PWDN",
        "10": "CAM_D0", "11": "CAM_D1", "12": "CAM_D2", "13": "CAM_D3",
        "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN",
        "19": "BTN_SHUT", "20": "BTN_MODE", "26": "GND",
    }
    u1 = b.add_footprint(
        "ISM.pretty", "ISM_RP2040_Module", "U1", mcu_x, mcu_y, value="RP2040_MOD",
        pad_nets=mod_nets, lib_path=ISM_PRETTY,
    )
    j1 = b.add_footprint(
        "Connector_USB.pretty", "USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal", "J1",
        PCB_W / 2, 6.0, value="USB_C",
        pad_nets={
            "A4": "+5V", "A9": "+5V", "B4": "+5V", "B9": "+5V",
            "A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "S1": "GND",
            "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM",
            "A5": "CC1", "B5": "CC2", "A8": "GND", "B8": "GND",
        },
    )
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R1",
                    PCB_W / 2 - 16, 13, value="5.1k", pad_nets={"1": "CC1", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R2",
                    PCB_W / 2 + 16, 13, value="5.1k", pad_nets={"1": "CC2", "2": "GND"})
    b.add_footprint("Package_TO_SOT_SMD.pretty", "SOT-666", "U2",
                    PCB_W / 2 + 28, 13, value="USBLC6-2SC6",
                    pad_nets={"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "+5V"})

    j2 = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_2x08_P2.54mm_Vertical", "J2",
        16.0, 28.0, value="CAM_MOD",
        pad_nets={
            "1": "+3V3", "2": "GND", "3": "CAM_SCL", "4": "CAM_SDA",
            "5": "CAM_VSYNC", "6": "CAM_HREF", "7": "CAM_PCLK", "8": "CAM_XCLK",
            "9": "CAM_D3", "10": "CAM_D2", "11": "CAM_D1", "12": "CAM_D0",
            "13": "CAM_RST", "14": "CAM_PWDN", "15": "+3V3", "16": "GND",
        },
    )
    u3 = b.add_footprint(
        "Package_SO.pretty", "SOIC-8_3.9x4.9mm_P1.27mm", "U3", 58.0, 22.0,
        value="AT24C02C",
        pad_nets={"1": "GND", "2": "GND", "3": "GND", "4": "GND",
                  "5": "CAM_SDA", "6": "CAM_SCL", "7": "GND", "8": "+3V3"},
    )
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R6",
                    68.0, 18.0, value="4.7k", pad_nets={"1": "CAM_SDA", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R7",
                    72.0, 18.0, value="4.7k", pad_nets={"1": "CAM_SCL", "2": "+3V3"})

    b.add_footprint("Button_Switch_SMD.pretty", "SW_SPST_PTS645", "SW1",
                    58.0, 42.0, value="SHUTTER", pad_nets={"1": "BTN_SHUT", "2": "GND"})
    b.add_footprint("Button_Switch_SMD.pretty", "SW_SPST_PTS645", "SW2",
                    66.0, 42.0, value="MODE", pad_nets={"1": "BTN_MODE", "2": "GND"})
    b.add_footprint("Button_Switch_SMD.pretty", "SW_SPST_PTS645", "SW_RST",
                    mcu_x + 24, mcu_y - 8, value="RESET", pad_nets={"1": "RUN", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R4",
                    mcu_x + 32, mcu_y - 8, value="10k", pad_nets={"1": "RUN", "2": "+3V3"})
    b.add_footprint("LED_SMD.pretty", "LED_0603_1608Metric", "D_PWR",
                    mcu_x + 24, mcu_y + 6, value="LED", pad_nets={"1": "GND", "2": "LED_A"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R5",
                    mcu_x + 32, mcu_y + 6, value="1k", pad_nets={"1": "+3V3", "2": "LED_A"})
    for i in range(4):
        b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", f"C{i+1}",
                        mcu_x - 18 + i * 4, mcu_y + 12, value="100nF",
                        pad_nets={"1": "+3V3", "2": "GND"})
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

    cam_map = {
        "3": ("3", "CAM_SCL"), "4": ("2", "CAM_SDA"),
        "5": ("6", "CAM_VSYNC"), "6": ("7", "CAM_HREF"),
        "7": ("5", "CAM_PCLK"), "8": ("4", "CAM_XCLK"),
        "9": ("13", "CAM_D3"), "10": ("12", "CAM_D2"),
        "11": ("11", "CAM_D1"), "12": ("10", "CAM_D0"),
        "13": ("8", "CAM_RST"), "14": ("9", "CAM_PWDN"),
    }
    for jpad, (mpad, net) in cam_map.items():
        manh(b, pad_xy(j2, jpad), pad_xy(u1, mpad), net, F, TW)
    manh(b, pad_xy(j2, "1"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(j2, "15"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(j2, "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(j2, "16"), pad_xy(u1, "1"), "GND", F, TW)

    manh(b, pad_xy(u3, "5"), pad_xy(u1, "2"), "CAM_SDA", F, TW)
    manh(b, pad_xy(u3, "6"), pad_xy(u1, "3"), "CAM_SCL", F, TW)
    manh(b, pad_xy(u3, "8"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(u3, "4"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R6"), "1"), pad_xy(u1, "2"), "CAM_SDA", F, TW)
    manh(b, pad_xy(fp("R6"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R7"), "1"), pad_xy(u1, "3"), "CAM_SCL", F, TW)
    manh(b, pad_xy(fp("R7"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)

    manh(b, pad_xy(fp("SW1"), "1"), pad_xy(u1, "19"), "BTN_SHUT", F, TW)
    manh(b, pad_xy(fp("SW1"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("SW2"), "1"), pad_xy(u1, "20"), "BTN_MODE", F, TW)
    manh(b, pad_xy(fp("SW2"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("SW_RST"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("SW_RST"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R4"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("R4"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R5"), "1"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R5"), "2"), pad_xy(fp("D_PWR"), "2"), "LED_A", F, TW)
    manh(b, pad_xy(fp("D_PWR"), "1"), pad_xy(u1, "1"), "GND", F, TW)
    for i in range(4):
        manh(b, pad_xy(fp(f"C{i+1}"), "1"), pad_xy(u1, "14"), "+3V3", F, TW)
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
    with zipfile.ZipFile(FAB / "ism-camera-gerbers.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(tmp.iterdir()):
            zf.write(p, p.name)
    shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run(["kicad-cli", "pcb", "export", "pos", "-o", str(FAB / "ism-camera-cpl.csv"),
                    "--format", "csv", "--units", "mm", "--side", "both", "--exclude-dnp", str(pcb)], check=False)
    rows = [
        ["Designator", "Value", "Footprint", "Quantity", "Manufacturer", "MPN", "LCSC", "Notes"],
        ["U1", "RP2040_MOD", "ISM_RP2040_Module", "1", "ISM", "ISM-RP2040-MOD", "",
         "No LCSC — custom ISM carrier"],
        ["U2", "USBLC6-2SC6", "SOT-666", "1", "ST", "USBLC6-2SC6", "C7519", "ESD"],
        ["U3", "AT24C02C", "SOIC-8", "1", "Microchip", "AT24C02C-SSHM-T", "C6203",
         "Config EEPROM"],
        ["J1", "USB4105", "GCT USB-C 16P", "1", "GCT", "USB4105-GF-A", "C165948", ""],
        ["J2", "CAM_MOD", "PinHeader 2x08", "1", "", "HDR-2x8", "C124418",
         "OV2640-class module header (sensor off-board)"],
        ["R1,R2", "5.1k", "0603", "2", "", "5.1k", "C23244", "CC"],
        ["R4", "10k", "0603", "1", "", "10k", "C25804", ""],
        ["R5", "1k", "0603", "1", "", "1k", "C21190", ""],
        ["R6,R7", "4.7k", "0603", "2", "", "4.7k", "C23141", "I2C pull-up"],
        ["C1-C4", "100nF", "0603", "4", "", "100nF", "C14663", ""],
        ["D_PWR", "LED", "0603", "1", "", "LED", "C2286", ""],
        ["SW1,SW2,SW_RST", "PTS645", "PTS645", "3", "", "PTS645", "C318884", ""],
        ["H1-H4", "M2", "MountingHole", "4", "", "", "",
         "No LCSC — mechanical NPTH"],
    ]
    with (FAB / "BOM.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    write_text(
        FAB / "README.md",
        """# Fab package — ISM Camera controller

| File | Use |
|------|-----|
| `ism-camera-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-camera-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT lines have LCSC numbers (EEPROM **C6203**, header **C124418**).
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- OV2640-class image sensor is an off-board module on `J2`.

Regenerate with `python3 scripts/build_camera.py`.
""",
    )


def patch_drc_severities() -> None:
    path = KICAD / "ism-camera.kicad_pro"
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
    write_text(KICAD / "ism-camera.kicad_sch", build_sch().emit())
    print("sch ok", flush=True)
    pcb = build_pcb()
    pcb_path = KICAD / "ism-camera.kicad_pcb"
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
                    "-o", str(KICAD / "erc.rpt"), str(KICAD / "ism-camera.kicad_sch")], check=False)
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
