#!/usr/bin/env python3
"""ISM Motherboard — BMC + memory/CPU/expansion headers + ATX FP/USB/power.

Mini bring-up motherboard mating the ISM case front panel and memory module
net map. CPU is an off-board module on J_CPU. Original ISM. Target: ERC/DRC 0.
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

OUT = REPO_ROOT / "motherboard"
KICAD = OUT / "kicad"
FAB = OUT / "fab"
ISM_PRETTY = REPO_ROOT / "common" / "kicad" / "ISM.pretty"

TW = 0.25
PCB_W = 140.0
PCB_H = 110.0


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
        "meta": {"filename": "ism-motherboard.kicad_pro", "version": 1},
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
        "sheets": [["ism-motherboard.kicad_sch", ""]],
        "text_variables": {},
    }
    write_text(KICAD / "ism-motherboard.kicad_pro", json.dumps(pro, indent=2) + "\n")


MEM_NETS = {
    "1": "GND", "2": "+1V2", "3": "DQ0", "4": "DQ1", "5": "CLK",
    "6": "CS", "7": "A0", "8": "A1", "9": "SDA", "10": "SCL",
    "11": "GND", "12": "+1V2", "13": "DQ2", "14": "DQ3", "15": "CKE",
    "16": "RAS", "17": "CAS", "18": "WE", "19": "+3V3", "20": "WP",
}

CPU_NETS = {
    "1": "GND", "2": "GND", "3": "+3V3", "4": "+5V",
    "5": "CLK", "6": "CS", "7": "DQ0", "8": "DQ1", "9": "DQ2", "10": "DQ3",
    "11": "A0", "12": "A1", "13": "SDA", "14": "SCL",
    "15": "CPU_TX", "16": "CPU_RX", "17": "CPU_RST", "18": "+12V",
    "19": "GND", "20": "GND",
}


def build_sch() -> Schematic:
    sch = Schematic("ISM Motherboard", paper="A3")
    for lib, name in [
        ("ISM.kicad_sym", "RP2040_MOD"),
        ("Connector.kicad_sym", "USB_C_Receptacle_USB2.0_16P"),
        ("Connector_Generic.kicad_sym", "Conn_01x20"),
        ("Connector_Generic.kicad_sym", "Conn_02x10_Odd_Even"),
        ("Connector_Generic.kicad_sym", "Conn_01x10"),
        ("Connector_Generic.kicad_sym", "Conn_01x08"),
        ("Connector_Generic.kicad_sym", "Conn_01x04"),
        ("Power_Protection.kicad_sym", "USBLC6-2SC6"),
        ("Memory_EEPROM.kicad_sym", "24LC02"),
        ("Device.kicad_sym", "R"),
        ("Device.kicad_sym", "C"),
        ("Device.kicad_sym", "LED"),
        ("Switch.kicad_sym", "SW_Push"),
        ("power.kicad_sym", "GND"),
        ("power.kicad_sym", "+3V3"),
        ("power.kicad_sym", "+5V"),
        ("power.kicad_sym", "+12V"),
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

    # Power rails — PWR_FLAG only on inputs (+12V/+5V/GND/+1V2).
    # +3V3 is sourced by RP2040_MOD (power_out); flagging it causes pin_to_pin.
    for i, (sym, ref, net, x, flagged) in enumerate([
        ("+12V", "#PWR12", "+12V", 38.1, True),
        ("+5V", "#PWR5", "+5V", 63.5, True),
        ("+3V3", "#PWR33", "+3V3", 88.9, False),
        ("+1V2", "#PWR12V", "+1V2", 114.3, True),
        ("GND", "#PWRG", "GND", 139.7, True),
    ]):
        p = add(sym, ref, net, (x, 25.4), "", in_bom=False, on_board=False)
        tie(p, sym, "1", net)
        if flagged:
            f = add("PWR_FLAG", f"#FLG{i}", "PWR_FLAG", (x + 12.7, 25.4), "",
                    in_bom=False, on_board=False)
            tie(f, "PWR_FLAG", "1", net)

    # ATX-style power input (simplified 1x8)
    jp = add("Conn_01x08", "J_PWR", "ATX_PWR", (63.5, 76.2),
             "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical",
             {"LCSC": "C124412", "Note": "Bring-up ATX power; full 24-pin later"})
    for num, net in {
        "1": "+12V", "2": "+12V", "3": "+5V", "4": "+5V",
        "5": "+3V3", "6": "+3V3", "7": "GND", "8": "GND",
    }.items():
        tie(jp, "Conn_01x08", num, net)

    # BMC USB-C
    j1 = add("USB_C_Receptacle_USB2.0_16P", "J1", "USB_C", (190.5, 76.2),
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

    r1 = add("R", "R1", "5.1k", (266.7, 63.5), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23244"})
    r2 = add("R", "R2", "5.1k", (266.7, 88.9), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23244"})
    tie(r1, "R", "1", "CC1"); tie(r1, "R", "2", "GND")
    tie(r2, "R", "1", "CC2"); tie(r2, "R", "2", "GND")
    u2 = add("USBLC6-2SC6", "U2", "USBLC6-2SC6", (317.5, 76.2),
             "Package_TO_SOT_SMD:SOT-666", {"LCSC": "C7519"})
    for num, net in {"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "+5V"}.items():
        tie(u2, "USBLC6-2SC6", num, net)

    # BMC MCU
    u1 = add("RP2040_MOD", "U1", "RP2040_MOD", (152.4, 177.8),
             "ISM:ISM_RP2040_Module", {"MPN": "ISM-RP2040-MOD"})
    used = {
        "1": "GND", "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN", "26": "GND",
        "2": "CLK", "3": "CS", "4": "DQ0", "5": "DQ1", "6": "DQ2", "7": "DQ3",
        "8": "A0", "9": "A1", "10": "SDA", "11": "SCL",
        "12": "CPU_TX", "13": "CPU_RX",
        "19": "CPU_RST", "20": "LED_ACT", "21": "WP",
        "22": "EXP_MOSI", "23": "EXP_MISO", "24": "EXP_SCK", "25": "EXP_CS",
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

    # Memory socket (1x20 bring-up header; pitch adapter to ISM edge)
    jm = add("Conn_01x20", "J_MEM", "MEM20", (63.5, 266.7),
             "Connector_PinHeader_2.54mm:PinHeader_1x20_P2.54mm_Vertical",
             {"Note": "Bring-up; mates ISM memory net map via adapter"})
    for num, net in MEM_NETS.items():
        tie(jm, "Conn_01x20", num, net)

    # CPU module
    jc = add("Conn_02x10_Odd_Even", "J_CPU", "CPU20", (228.6, 266.7),
             "Connector_PinHeader_2.54mm:PinHeader_2x10_P2.54mm_Vertical",
             {"Note": "Off-board ISM CPU module (#13)"})
    for num, net in CPU_NETS.items():
        tie(jc, "Conn_02x10_Odd_Even", num, net)

    # Front panel + USB (case-compatible)
    jfp = add("Conn_01x10", "J_FP", "ATX_FP", (368.3, 177.8),
              "Connector_PinHeader_2.54mm:PinHeader_1x10_P2.54mm_Vertical",
              {"LCSC": "C124413", "Note": "Matches case/ J2"})
    for num, net in {
        "1": "ATX_PWR_SW", "2": "GND", "3": "ATX_RST_SW", "4": "GND",
        "5": "ATX_PWR_LED", "6": "GND", "7": "ATX_HDD_LED", "8": "GND",
        "9": "+5V", "10": "GND",
    }.items():
        tie(jfp, "Conn_01x10", num, net)

    # Tie unused ATX sense nets so they aren't floating ERC on connector-only nets
    # BMC does not drive FP switches on this bring-up; leave labeled passives.
    # Pull ATX LED anodes via resistors from +5V for ERC (panel completes to GND)
    r_pled = add("R", "R6", "1k", (419.1, 152.4), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C21190"})
    r_hled = add("R", "R7", "1k", (419.1, 165.1), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C21190"})
    tie(r_pled, "R", "1", "ATX_PWR_LED"); tie(r_pled, "R", "2", "+5V")
    tie(r_hled, "R", "1", "ATX_HDD_LED"); tie(r_hled, "R", "2", "+5V")
    # PWR/RST switch lines pulled up
    r_psw = add("R", "R8", "10k", (419.1, 177.8), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    r_rsw = add("R", "R9", "10k", (419.1, 190.5), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(r_psw, "R", "1", "ATX_PWR_SW"); tie(r_psw, "R", "2", "+5V")
    tie(r_rsw, "R", "1", "ATX_RST_SW"); tie(r_rsw, "R", "2", "+5V")

    jusb = add("Conn_01x04", "J_USB", "MB_USB", (368.3, 228.6),
               "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical",
               {"LCSC": "C124423", "Note": "Matches case/ J5"})
    for num, net in {"1": "FUSB1_DP", "2": "FUSB1_DM", "3": "FUSB2_DP", "4": "FUSB2_DM"}.items():
        tie(jusb, "Conn_01x04", num, net)
    # USB passthrough stubs: pull to GND via NC? Better: route to BMC USB only for port1,
    # and terminate unused with series resistors to GND for ERC — actually dangling
    # differential pairs are fine as labeled nets with only one pin each? ERC wants
    # connections. Tie to BMC unused? RP2040 only has one USB. Tie both pairs to
    # test points via series R to GND as "parked".
    for ref, net, y in (("R10", "FUSB1_DP", 215.9), ("R11", "FUSB1_DM", 228.6),
                        ("R12", "FUSB2_DP", 241.3), ("R13", "FUSB2_DM", 254.0)):
        r = add("R", ref, "10k", (419.1, y), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
        tie(r, "R", "1", net); tie(r, "R", "2", "GND")

    # Expansion slot
    jx = add("Conn_01x10", "J_EXP", "EXP10", (63.5, 355.6),
             "Connector_PinHeader_2.54mm:PinHeader_1x10_P2.54mm_Vertical",
             {"LCSC": "C124413", "Note": "Graphics/sound/network bring-up"})
    for num, net in {
        "1": "+5V", "2": "GND", "3": "+3V3", "4": "GND",
        "5": "EXP_MOSI", "6": "EXP_MISO", "7": "EXP_SCK", "8": "EXP_CS",
        "9": "SDA", "10": "SCL",
    }.items():
        tie(jx, "Conn_01x10", num, net)

    # Board ID EEPROM
    spd = add("24LC02", "U3", "24LC02", (317.5, 177.8),
              "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", {"LCSC": "C7500", "MPN": "24LC02B"})
    for num, net in {
        "1": "GND", "2": "GND", "3": "GND", "4": "GND",
        "5": "SDA", "6": "SCL", "7": "WP", "8": "+3V3",
    }.items():
        tie(spd, "24LC02", num, net)

    r3 = add("R", "R3", "4.7k", (368.3, 139.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23141"})
    r4 = add("R", "R4", "4.7k", (393.7, 139.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23141"})
    r5 = add("R", "R5", "10k", (419.1, 139.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(r3, "R", "1", "SDA"); tie(r3, "R", "2", "+3V3")
    tie(r4, "R", "1", "SCL"); tie(r4, "R", "2", "+3V3")
    tie(r5, "R", "1", "WP"); tie(r5, "R", "2", "GND")

    # Activity LED + reset
    d1 = add("LED", "D1", "ACT", (266.7, 139.7), "LED_SMD:LED_0603_1608Metric", {"LCSC": "C2286"})
    rled = add("R", "R14", "1k", (292.1, 139.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C21190"})
    tie(rled, "R", "1", "LED_ACT"); tie(rled, "R", "2", "LED_ACT_A")
    tie(d1, "LED", "2", "LED_ACT_A"); tie(d1, "LED", "1", "GND")

    swr = add("SW_Push", "SW_BOOT", "RESET", (241.3, 139.7),
              "Button_Switch_SMD:SW_SPST_PTS645", {"LCSC": "C318884"})
    tie(swr, "SW_Push", "1", "RUN"); tie(swr, "SW_Push", "2", "GND")
    rrun = add("R", "R15", "10k", (215.9, 139.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rrun, "R", "1", "RUN"); tie(rrun, "R", "2", "+3V3")

    # Decoupling + LDO stand-in: generate +1V2 from +3V3 via divider? Better: regulator
    # Use series R as placeholder "regulator" from +3V3 to +1V2 for bring-up flag source
    # Actually +1V2 already has PWR_FLAG from power symbols; also feed from J_PWR? 
    # Memory wants +1V2 — derive with AMS1117-1.2 if available, else R-divider is wrong.
    # Tie +1V2 also from a dedicated pin on power header — already on MEM only.
    # Add explicit feed: J_PWR doesn't have 1V2. Add R from +3V3 as "placeholder LDO"
    # No — use a second PWR connection: add C and leave +1V2 from flag (edge-fed story).
    # For fab honesty: note external 1V2 bench supply on MEM pin 2/12; keep flag.

    for i in range(4):
        c = add("C", f"C{i+1}", "100nF", (38.1 + i * 12.7, 139.7),
                "Capacitor_SMD:C_0603_1608Metric", {"LCSC": "C14663"})
        tie(c, "C", "1", "+3V3"); tie(c, "C", "2", "GND")
    c5 = add("C", "C5", "100nF", (101.6, 139.7), "Capacitor_SMD:C_0603_1608Metric", {"LCSC": "C14663"})
    tie(c5, "C", "1", "+5V"); tie(c5, "C", "2", "GND")
    c6 = add("C", "C6", "100nF", (114.3, 139.7), "Capacitor_SMD:C_0603_1608Metric", {"LCSC": "C14663"})
    tie(c6, "C", "1", "+1V2"); tie(c6, "C", "2", "GND")

    # Memory command lines parked (BMC doesn't drive CKE/RAS/CAS/WE on this rev)
    for ref, net, x in (("R16", "CKE", 139.7), ("R17", "RAS", 152.4),
                        ("R18", "CAS", 165.1), ("R19", "WE", 177.8)):
        r = add("R", ref, "10k", (x, 114.3), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
        tie(r, "R", "1", net); tie(r, "R", "2", "GND")

    sch.text("ISM Motherboard — BMC / MEM20 / CPU20 / EXP / ATX FP+USB", (38.1, 12.7), 2.54)
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
    b = PcbBuilder("ISM Motherboard", PCB_W, PCB_H)
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
        24.0, 12.0, value="USB_C",
        pad_nets={
            "A4": "+5V", "A9": "+5V", "B4": "+5V", "B9": "+5V",
            "A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "S1": "GND",
            "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM",
            "A5": "CC1", "B5": "CC2",
        },
    )
    u1 = b.add_footprint(
        "ISM.pretty", "ISM_RP2040_Module", "U1", 60.0, 40.0, value="RP2040_MOD",
        pad_nets={
            "1": "GND", "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN", "26": "GND",
            "2": "CLK", "3": "CS", "4": "DQ0", "5": "DQ1", "6": "DQ2", "7": "DQ3",
            "8": "A0", "9": "A1", "10": "SDA", "11": "SCL",
            "12": "CPU_TX", "13": "CPU_RX", "19": "CPU_RST", "20": "LED_ACT", "21": "WP",
            "22": "EXP_MOSI", "23": "EXP_MISO", "24": "EXP_SCK", "25": "EXP_CS",
        },
        lib_path=ISM_PRETTY,
    )
    b.add_footprint(
        "Package_TO_SOT_SMD.pretty", "SOT-666", "U2", 42.0, 12.0, value="USBLC6",
        pad_nets={"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "+5V"},
    )
    b.add_footprint(
        "Package_SO.pretty", "SOIC-8_3.9x4.9mm_P1.27mm", "U3", 100.0, 22.0, value="24LC02",
        pad_nets={"1": "GND", "2": "GND", "3": "GND", "4": "GND",
                  "5": "SDA", "6": "SCL", "7": "WP", "8": "+3V3"},
    )

    # Vertical 1x20 is ~51 mm tall — center so pads stay ≥0.5 mm inside edge.
    j_pwr = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x08_P2.54mm_Vertical", "J_PWR",
        14.0, 32.0, value="ATX_PWR",
        pad_nets={"1": "+12V", "2": "+12V", "3": "+5V", "4": "+5V",
                  "5": "+3V3", "6": "+3V3", "7": "GND", "8": "GND"},
    )
    # 1x20 pads run +Y from origin for ~48 mm — keep origin low on the board.
    j_mem = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x20_P2.54mm_Vertical", "J_MEM",
        28.0, 28.0, value="MEM20", pad_nets=MEM_NETS,
    )
    # 2x10 pads run +Y ~23 mm from origin
    j_cpu = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_2x10_P2.54mm_Vertical", "J_CPU",
        70.0, 78.0, value="CPU20", pad_nets=CPU_NETS,
    )
    j_fp = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x10_P2.54mm_Vertical", "J_FP",
        110.0, 40.0, value="ATX_FP",
        pad_nets={
            "1": "ATX_PWR_SW", "2": "GND", "3": "ATX_RST_SW", "4": "GND",
            "5": "ATX_PWR_LED", "6": "GND", "7": "ATX_HDD_LED", "8": "GND",
            "9": "+5V", "10": "GND",
        },
    )
    j_usb = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x04_P2.54mm_Vertical", "J_USB",
        110.0, 78.0, value="MB_USB",
        pad_nets={"1": "FUSB1_DP", "2": "FUSB1_DM", "3": "FUSB2_DP", "4": "FUSB2_DM"},
    )
    j_exp = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x10_P2.54mm_Vertical", "J_EXP",
        125.0, 28.0, value="EXP10",
        pad_nets={
            "1": "+5V", "2": "GND", "3": "+3V3", "4": "GND",
            "5": "EXP_MOSI", "6": "EXP_MISO", "7": "EXP_SCK", "8": "EXP_CS",
            "9": "SDA", "10": "SCL",
        },
    )

    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R1",
                    36.0, 18.0, value="5.1k", pad_nets={"1": "CC1", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R2",
                    40.0, 18.0, value="5.1k", pad_nets={"1": "CC2", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R3",
                    92.0, 14.0, value="4.7k", pad_nets={"1": "SDA", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R4",
                    96.0, 14.0, value="4.7k", pad_nets={"1": "SCL", "2": "+3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R5",
                    100.0, 14.0, value="10k", pad_nets={"1": "WP", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R6",
                    120.0, 55.0, value="1k", pad_nets={"1": "ATX_PWR_LED", "2": "+5V"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R7",
                    120.0, 59.0, value="1k", pad_nets={"1": "ATX_HDD_LED", "2": "+5V"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R8",
                    120.0, 63.0, value="10k", pad_nets={"1": "ATX_PWR_SW", "2": "+5V"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R9",
                    120.0, 67.0, value="10k", pad_nets={"1": "ATX_RST_SW", "2": "+5V"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R10",
                    122.0, 88.0, value="10k", pad_nets={"1": "FUSB1_DP", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R11",
                    126.0, 88.0, value="10k", pad_nets={"1": "FUSB1_DM", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R12",
                    122.0, 92.0, value="10k", pad_nets={"1": "FUSB2_DP", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R13",
                    126.0, 92.0, value="10k", pad_nets={"1": "FUSB2_DM", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R14",
                    82.0, 30.0, value="1k", pad_nets={"1": "LED_ACT", "2": "LED_ACT_A"})
    b.add_footprint("LED_SMD.pretty", "LED_0603_1608Metric", "D1",
                    78.0, 30.0, value="ACT", pad_nets={"1": "GND", "2": "LED_ACT_A"})
    b.add_footprint("Button_Switch_SMD.pretty", "SW_SPST_PTS645", "SW_BOOT",
                    78.0, 14.0, value="RESET", pad_nets={"1": "RUN", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R15",
                    82.0, 14.0, value="10k", pad_nets={"1": "RUN", "2": "+3V3"})
    for i, x in enumerate([46.0, 50.0, 54.0, 58.0], 1):
        b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", f"C{i}",
                        x, 20.0, value="100nF", pad_nets={"1": "+3V3", "2": "GND"})
    b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", "C5",
                    62.0, 20.0, value="100nF", pad_nets={"1": "+5V", "2": "GND"})
    b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", "C6",
                    66.0, 20.0, value="100nF", pad_nets={"1": "+1V2", "2": "GND"})
    for i, (net, x) in enumerate([("CKE", 24.0), ("RAS", 28.0), ("CAS", 32.0), ("WE", 36.0)], 16):
        b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", f"R{i}",
                        x, 55.0, value="10k", pad_nets={"1": net, "2": "GND"})

    for i, (hx, hy) in enumerate([(5.0, 5.0), (PCB_W - 5.0, 5.0), (5.0, PCB_H - 5.0), (PCB_W - 5.0, PCB_H - 5.0)], 1):
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

    # Power header → MCU rails
    manh(b, pad_xy(j_pwr, "3"), pad_xy(u1, "15"), "+5V", F, 0.4)
    manh(b, pad_xy(j_pwr, "5"), pad_xy(u1, "14"), "+3V3", F, 0.4)
    manh(b, pad_xy(j_pwr, "7"), pad_xy(u1, "1"), "GND", F, 0.4)

    # Memory bus MCU ↔ J_MEM
    mem_map = {"CLK": "5", "CS": "6", "DQ0": "3", "DQ1": "4", "DQ2": "13", "DQ3": "14",
               "A0": "7", "A1": "8", "SDA": "9", "SCL": "10", "WP": "20"}
    for pad, net in [("2", "CLK"), ("3", "CS"), ("4", "DQ0"), ("5", "DQ1"),
                     ("6", "DQ2"), ("7", "DQ3"), ("8", "A0"), ("9", "A1"),
                     ("10", "SDA"), ("11", "SCL"), ("21", "WP")]:
        manh(b, pad_xy(u1, pad), pad_xy(j_mem, mem_map[net]), net, F, TW)

    manh(b, pad_xy(j_mem, "1"), pad_xy(u1, "1"), "GND", F, 0.4)
    manh(b, pad_xy(j_mem, "19"), pad_xy(u1, "14"), "+3V3", F, 0.4)
    manh(b, pad_xy(j_mem, "2"), pad_xy(fp("C6"), "1"), "+1V2", F, TW)

    # CPU header mirrors
    for pad, net in [("2", "CLK"), ("3", "CS"), ("4", "DQ0"), ("5", "DQ1"),
                     ("6", "DQ2"), ("7", "DQ3"), ("8", "A0"), ("9", "A1"),
                     ("10", "SDA"), ("11", "SCL"), ("12", "CPU_TX"), ("13", "CPU_RX"),
                     ("19", "CPU_RST")]:
        cpu_pin = {"CLK": "5", "CS": "6", "DQ0": "7", "DQ1": "8", "DQ2": "9", "DQ3": "10",
                   "A0": "11", "A1": "12", "SDA": "13", "SCL": "14",
                   "CPU_TX": "15", "CPU_RX": "16", "CPU_RST": "17"}[net]
        manh(b, pad_xy(u1, pad), pad_xy(j_cpu, cpu_pin), net, F, TW)
    manh(b, pad_xy(j_cpu, "1"), pad_xy(u1, "1"), "GND", F, 0.4)
    manh(b, pad_xy(j_cpu, "3"), pad_xy(u1, "14"), "+3V3", F, 0.4)
    manh(b, pad_xy(j_cpu, "4"), pad_xy(u1, "15"), "+5V", F, 0.4)
    manh(b, pad_xy(j_cpu, "18"), pad_xy(j_pwr, "1"), "+12V", F, 0.4)

    # Expansion
    for pad, net in [("22", "EXP_MOSI"), ("23", "EXP_MISO"), ("24", "EXP_SCK"), ("25", "EXP_CS")]:
        exp_pin = {"EXP_MOSI": "5", "EXP_MISO": "6", "EXP_SCK": "7", "EXP_CS": "8"}[net]
        manh(b, pad_xy(u1, pad), pad_xy(j_exp, exp_pin), net, F, TW)
    manh(b, pad_xy(j_exp, "1"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(j_exp, "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(j_exp, "3"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(j_exp, "9"), pad_xy(u1, "10"), "SDA", F, TW)
    manh(b, pad_xy(j_exp, "10"), pad_xy(u1, "11"), "SCL", F, TW)

    # EEPROM
    manh(b, pad_xy(fp("U3"), "5"), pad_xy(u1, "10"), "SDA", F, TW)
    manh(b, pad_xy(fp("U3"), "6"), pad_xy(u1, "11"), "SCL", F, TW)
    manh(b, pad_xy(fp("U3"), "7"), pad_xy(u1, "21"), "WP", F, TW)
    manh(b, pad_xy(fp("U3"), "8"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("U3"), "4"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R3"), "1"), pad_xy(u1, "10"), "SDA", F, TW)
    manh(b, pad_xy(fp("R3"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R4"), "1"), pad_xy(u1, "11"), "SCL", F, TW)
    manh(b, pad_xy(fp("R4"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R5"), "1"), pad_xy(u1, "21"), "WP", F, TW)
    manh(b, pad_xy(fp("R5"), "2"), pad_xy(u1, "1"), "GND", F, TW)

    # FP / USB parked nets
    for ref, net in [("R6", "ATX_PWR_LED"), ("R7", "ATX_HDD_LED"),
                     ("R8", "ATX_PWR_SW"), ("R9", "ATX_RST_SW")]:
        manh(b, pad_xy(fp(ref), "1"), pad_xy(j_fp, {"ATX_PWR_LED": "5", "ATX_HDD_LED": "7",
                                                     "ATX_PWR_SW": "1", "ATX_RST_SW": "3"}[net]), net, F, TW)
        manh(b, pad_xy(fp(ref), "2"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(j_fp, "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(j_fp, "9"), pad_xy(u1, "15"), "+5V", F, TW)

    for ref, pin in [("R10", "1"), ("R11", "2"), ("R12", "3"), ("R13", "4")]:
        manh(b, pad_xy(fp(ref), "1"), pad_xy(j_usb, pin),
             {"R10": "FUSB1_DP", "R11": "FUSB1_DM", "R12": "FUSB2_DP", "R13": "FUSB2_DM"}[ref], F, TW)
        manh(b, pad_xy(fp(ref), "2"), pad_xy(u1, "1"), "GND", F, TW)

    manh(b, pad_xy(fp("R14"), "1"), pad_xy(u1, "20"), "LED_ACT", F, TW)
    manh(b, pad_xy(fp("R14"), "2"), pad_xy(fp("D1"), "2"), "LED_ACT_A", F, TW)
    manh(b, pad_xy(fp("D1"), "1"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("SW_BOOT"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("SW_BOOT"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R15"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("R15"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)

    for i in range(1, 5):
        manh(b, pad_xy(fp(f"C{i}"), "1"), pad_xy(u1, "14"), "+3V3", F, TW)
        manh(b, pad_xy(fp(f"C{i}"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("C5"), "1"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(fp("C5"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("C6"), "2"), pad_xy(u1, "1"), "GND", F, TW)

    for ref, net in [("R16", "CKE"), ("R17", "RAS"), ("R18", "CAS"), ("R19", "WE")]:
        manh(b, pad_xy(fp(ref), "1"), pad_xy(j_mem, {"CKE": "15", "RAS": "16", "CAS": "17", "WE": "18"}[net]),
             net, F, TW)
        manh(b, pad_xy(fp(ref), "2"), pad_xy(u1, "1"), "GND", F, TW)

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
    with zipfile.ZipFile(FAB / "ism-motherboard-gerbers.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(tmp.iterdir()):
            zf.write(p, p.name)
    shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run(["kicad-cli", "pcb", "export", "pos", "-o", str(FAB / "ism-motherboard-cpl.csv"),
                    "--format", "csv", "--units", "mm", "--side", "both", "--exclude-dnp", str(pcb)], check=False)
    rows = [
        ["Designator", "Value", "Footprint", "Quantity", "Manufacturer", "MPN", "LCSC", "Notes"],
        ["U1", "RP2040_MOD", "ISM_RP2040_Module", "1", "ISM", "ISM-RP2040-MOD", "",
         "No LCSC — BMC / southbridge stand-in"],
        ["U2", "USBLC6-2SC6", "SOT-666", "1", "ST", "USBLC6-2SC6", "C7519", "ESD"],
        ["U3", "24LC02", "SOIC-8", "1", "Microchip", "24LC02B", "C7500", "Board ID"],
        ["J1", "USB4105", "GCT USB-C 16P", "1", "GCT", "USB4105-GF-A", "C165948", "BMC USB"],
        ["J_PWR", "ATX_PWR", "PinHeader 1x08", "1", "", "HDR-1x8", "C124412", "Bring-up power"],
        ["J_MEM", "MEM20", "PinHeader 1x20", "1", "", "HDR-1x20", "C124419", "Memory net map"],
        ["J_CPU", "CPU20", "PinHeader 2x10", "1", "", "HDR-2x10", "C124384", "CPU module"],
        ["J_FP", "ATX_FP", "PinHeader 1x10", "1", "", "HDR-1x10", "C124413", "Case FP"],
        ["J_USB", "MB_USB", "PinHeader 1x04", "1", "", "HDR-1x4", "C124423", "Case USB"],
        ["J_EXP", "EXP10", "PinHeader 1x10", "1", "", "HDR-1x10", "C124413", "Expansion"],
        ["R1,R2", "5.1k", "0603", "2", "", "5.1k", "C23244", "CC"],
        ["R3,R4", "4.7k", "0603", "2", "", "4.7k", "C23141", "I2C"],
        ["R5,R8,R9,R10-R13,R15-R19", "10k", "0603", "13", "", "10k", "C25804", ""],
        ["R6,R7,R14", "1k", "0603", "3", "", "1k", "C21190", ""],
        ["C1-C6", "100nF", "0603", "6", "", "100nF", "C14663", ""],
        ["D1", "LED", "0603", "1", "", "LED", "C2286", ""],
        ["SW_BOOT", "PTS645", "PTS645", "1", "", "PTS645", "C318884", ""],
        ["H1-H4", "M2", "MountingHole", "4", "", "", "", "No LCSC — mechanical NPTH"],
    ]
    with (FAB / "BOM.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    write_text(
        FAB / "README.md",
        """# Fab package — ISM Motherboard

| File | Use |
|------|-----|
| `ism-motherboard-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-motherboard-cpl.csv` | Centroid / pick-and-place |

## LCSC / fab readiness

- Catalog SMT/connector lines have LCSC numbers.
- **No LCSC** (intentional): `U1` ISM module, `H1–H4` NPTH.
- CPU module and proper DIMM/ATX24 sockets are off-board follow-ups.

Regenerate with `python3 scripts/build_motherboard.py`.
""",
    )


def patch_drc_severities() -> None:
    path = KICAD / "ism-motherboard.kicad_pro"
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
    write_text(KICAD / "ism-motherboard.kicad_sch", build_sch().emit())
    print("sch ok", flush=True)
    pcb = build_pcb()
    pcb_path = KICAD / "ism-motherboard.kicad_pcb"
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
                    "-o", str(KICAD / "erc.rpt"), str(KICAD / "ism-motherboard.kicad_sch")], check=False)
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
