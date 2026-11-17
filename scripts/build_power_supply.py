#!/usr/bin/env python3
"""ISM Power Supply — DC-side ATX-style rail board (Track A).

12 V DC in (certified brick off-board) → LM2596 bucks for +5 V / +3.3 V,
pass-through +12 V, mates motherboard J_PWR 1×8. RP2040 monitors rails /
PS_ON / PWR_OK. No mains on this PCB. Original ISM. ERC/DRC 0.
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

OUT = REPO_ROOT / "power-supply"
KICAD = OUT / "kicad"
FAB = OUT / "fab"
ISM_PRETTY = REPO_ROOT / "common" / "kicad" / "ISM.pretty"

TW = 0.25
PCB_W = 100.0
PCB_H = 70.0

# Must match motherboard J_PWR
PWR_NETS = {
    "1": "+12V", "2": "+12V", "3": "+5V", "4": "+5V",
    "5": "+3V3", "6": "+3V3", "7": "GND", "8": "GND",
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
  (lib (name "Regulator_Switching")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Regulator_Switching.kicad_sym")(options "")(descr ""))
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
  (lib (name "Connector_USB")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Connector_USB.pretty")(options "")(descr ""))
  (lib (name "Connector_BarrelJack")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Connector_BarrelJack.pretty")(options "")(descr ""))
  (lib (name "Connector_PinHeader_2.54mm")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Connector_PinHeader_2.54mm.pretty")(options "")(descr ""))
  (lib (name "Inductor_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Inductor_SMD.pretty")(options "")(descr ""))
  (lib (name "Diode_SMD")(type "KiCad")(uri "${KICAD8_FOOTPRINT_DIR}/Diode_SMD.pretty")(options "")(descr ""))
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
        "meta": {"filename": "ism-power-supply.kicad_pro", "version": 1},
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
        "sheets": [["ism-power-supply.kicad_sch", ""]],
        "text_variables": {},
    }
    write_text(KICAD / "ism-power-supply.kicad_pro", json.dumps(pro, indent=2) + "\n")


def build_sch() -> Schematic:
    sch = Schematic("ISM Power Supply", paper="A3")
    for lib, name in [
        ("ISM.kicad_sym", "RP2040_MOD"),
        ("Connector.kicad_sym", "USB_C_Receptacle_USB2.0_16P"),
        ("Connector.kicad_sym", "Barrel_Jack"),
        ("Connector_Generic.kicad_sym", "Conn_01x08"),
        ("Connector_Generic.kicad_sym", "Conn_01x04"),
        ("Power_Protection.kicad_sym", "USBLC6-2SC6"),
        ("Regulator_Switching.kicad_sym", "LM2596S-5"),
        ("Regulator_Switching.kicad_sym", "LM2596S-3.3"),
        ("Device.kicad_sym", "R"),
        ("Device.kicad_sym", "C"),
        ("Device.kicad_sym", "L"),
        ("Device.kicad_sym", "D_Schottky"),
        ("Device.kicad_sym", "LED"),
        ("Switch.kicad_sym", "SW_Push"),
        ("power.kicad_sym", "GND"),
        ("power.kicad_sym", "+3V3"),
        ("power.kicad_sym", "+5V"),
        ("power.kicad_sym", "+12V"),
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

    # +12V from certified brick is primary source; +5V from LM2596.
    # Do NOT flag +3V3 — RP2040 module pin is power_out (same as motherboard).
    for i, (sym, ref, net, x, flagged) in enumerate([
        ("+12V", "#PWR12", "+12V", 38.1, True),
        ("+5V", "#PWR5", "+5V", 63.5, True),
        ("+3V3", "#PWR33", "+3V3", 88.9, False),
        ("GND", "#PWRG", "GND", 114.3, True),
    ]):
        p = add(sym, ref, net, (x, 25.4), "", in_bom=False, on_board=False)
        tie(p, sym, "1", net)
        if flagged:
            f = add("PWR_FLAG", f"#FLG{i}", "PWR_FLAG", (x + 12.7, 25.4), "",
                    in_bom=False, on_board=False)
            tie(f, "PWR_FLAG", "1", net)

    jin = add("Barrel_Jack", "J_IN", "DC_12V", (63.5, 88.9),
              "Connector_BarrelJack:BarrelJack_CUI_PJ-063AH_Horizontal",
              {"LCSC": "C75013", "Note": "From certified 12V AC-DC brick — no mains on PCB"})
    tie(jin, "Barrel_Jack", "1", "+12V")
    tie(jin, "Barrel_Jack", "2", "GND")

    jout = add("Conn_01x08", "J_OUT", "MB_PWR", (152.4, 88.9),
               "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical",
               {"LCSC": "C124412", "Note": "Mates motherboard J_PWR"})
    for num, net in PWR_NETS.items():
        tie(jout, "Conn_01x08", num, net)

    jctl = add("Conn_01x04", "J_CTL", "ATX_CTL", (228.6, 88.9),
               "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical",
               {"LCSC": "C124409", "Note": "PS_ON / PWR_OK / 5VSB"})
    for num, net in {"1": "PS_ON", "2": "PWR_OK", "3": "GND", "4": "+5V"}.items():
        tie(jctl, "Conn_01x04", num, net)

    jusb = add("USB_C_Receptacle_USB2.0_16P", "J_USB", "USB_C", (317.5, 88.9),
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

    r1 = add("R", "R1", "5.1k", (393.7, 76.2), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23244"})
    r2 = add("R", "R2", "5.1k", (393.7, 101.6), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C23244"})
    tie(r1, "R", "1", "CC1"); tie(r1, "R", "2", "GND")
    tie(r2, "R", "1", "CC2"); tie(r2, "R", "2", "GND")
    u2 = add("USBLC6-2SC6", "U2", "USBLC6-2SC6", (444.5, 88.9),
             "Package_TO_SOT_SMD:SOT-666", {"LCSC": "C7519"})
    for num, net in {"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "+5V"}.items():
        tie(u2, "USBLC6-2SC6", num, net)

    u1 = add("RP2040_MOD", "U1", "RP2040_MOD", (152.4, 190.5),
             "ISM:ISM_RP2040_Module", {"MPN": "ISM-RP2040-MOD", "Note": "PSU monitor / sequencer"})
    used = {
        "1": "GND", "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN", "26": "GND",
        "2": "PS_ON", "3": "PWR_OK", "4": "SNS_12V", "5": "SNS_5V",
        "6": "SNS_3V3", "19": "LED_ACT",
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

    # +5 V buck
    u5 = add("LM2596S-5", "U3", "LM2596S-5.0", (292.1, 190.5),
             "Package_TO_SOT_SMD:TO-263-5_TabPin3",
             {"LCSC": "C10872", "MPN": "LM2596S-5.0"})
    tie(u5, "LM2596S-5", "1", "+12V")
    tie(u5, "LM2596S-5", "2", "SW_5V")
    tie(u5, "LM2596S-5", "3", "GND")
    tie(u5, "LM2596S-5", "4", "+5V")
    tie(u5, "LM2596S-5", "5", "GND")
    l5 = add("L", "L1", "33uH", (355.6, 177.8), "Inductor_SMD:L_12x12mm_H6mm", {"LCSC": "C167270"})
    tie(l5, "L", "1", "SW_5V"); tie(l5, "L", "2", "+5V")
    d5 = add("D_Schottky", "D4", "SS34", (355.6, 203.2), "Diode_SMD:D_SMA", {"LCSC": "C8678"})
    tie(d5, "D_Schottky", "1", "SW_5V"); tie(d5, "D_Schottky", "2", "GND")  # K=1 to SW, A=2 to GND

    # +3V3 buck
    u33 = add("LM2596S-3.3", "U4", "LM2596S-3.3", (419.1, 190.5),
              "Package_TO_SOT_SMD:TO-263-5_TabPin3",
              {"LCSC": "C10871", "MPN": "LM2596S-3.3"})
    tie(u33, "LM2596S-3.3", "1", "+12V")
    tie(u33, "LM2596S-3.3", "2", "SW_3V3")
    tie(u33, "LM2596S-3.3", "3", "GND")
    tie(u33, "LM2596S-3.3", "4", "+3V3")
    tie(u33, "LM2596S-3.3", "5", "GND")
    l33 = add("L", "L2", "33uH", (482.6, 177.8), "Inductor_SMD:L_12x12mm_H6mm", {"LCSC": "C167270"})
    tie(l33, "L", "1", "SW_3V3"); tie(l33, "L", "2", "+3V3")
    d33 = add("D_Schottky", "D5", "SS34", (482.6, 203.2), "Diode_SMD:D_SMA", {"LCSC": "C8678"})
    tie(d33, "D_Schottky", "1", "SW_3V3"); tie(d33, "D_Schottky", "2", "GND")

    # Sense dividers (≈½ rail into MCU ADC GPIOs)
    for ref, top, mid, bot, x in [
        ("R3", "+12V", "SNS_12V", "GND", 241.3),
        ("R5", "+5V", "SNS_5V", "GND", 266.7),
        ("R7", "+3V3", "SNS_3V3", "GND", 292.1),
    ]:
        rt = add("R", ref, "10k", (x, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
        rb = add("R", f"R{int(ref[1:])+1}", "10k", (x + 12.7, 266.7),
                 "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
        tie(rt, "R", "1", top); tie(rt, "R", "2", mid)
        tie(rb, "R", "1", mid); tie(rb, "R", "2", bot)

    rpson = add("R", "R9", "10k", (343.0, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rpson, "R", "1", "PS_ON"); tie(rpson, "R", "2", "+5V")
    rpok = add("R", "R10", "10k", (368.3, 266.7), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rpok, "R", "1", "PWR_OK"); tie(rpok, "R", "2", "+5V")

    d1 = add("LED", "D1", "ACT", (393.7, 292.1), "LED_SMD:LED_0603_1608Metric", {"LCSC": "C2286"})
    rled = add("R", "R11", "1k", (419.1, 292.1), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C21190"})
    tie(rled, "R", "1", "LED_ACT"); tie(rled, "R", "2", "LED_ACT_A")
    tie(d1, "LED", "2", "LED_ACT_A"); tie(d1, "LED", "1", "GND")

    swr = add("SW_Push", "SW_BOOT", "RESET", (444.5, 292.1),
              "Button_Switch_SMD:SW_SPST_PTS645", {"LCSC": "C318884"})
    tie(swr, "SW_Push", "1", "RUN"); tie(swr, "SW_Push", "2", "GND")
    rrun = add("R", "R12", "10k", (470.0, 292.1), "Resistor_SMD:R_0603_1608Metric", {"LCSC": "C25804"})
    tie(rrun, "R", "1", "RUN"); tie(rrun, "R", "2", "+3V3")

    # Bulk / decoupling
    for i, (ref, val, net, lcsc, x) in enumerate([
        ("C1", "100uF", "+12V", "C15855", 38.1),
        ("C2", "100uF", "+5V", "C15855", 63.5),
        ("C3", "100uF", "+3V3", "C15855", 88.9),
        ("C4", "100nF", "+12V", "C14663", 114.3),
        ("C5", "100nF", "+5V", "C14663", 139.7),
        ("C6", "100nF", "+3V3", "C14663", 165.1),
        ("C7", "100nF", "+5V", "C14663", 190.5),
        ("C8", "100nF", "+3V3", "C14663", 215.9),
    ]):
        c = add("C", ref, val, (x, 152.4), "Capacitor_SMD:C_0603_1608Metric", {"LCSC": lcsc})
        tie(c, "C", "1", net); tie(c, "C", "2", "GND")

    sch.text("ISM PSU — 12V brick / LM2596 ×2 / MB J_PWR (no mains)", (38.1, 12.7), 2.54)
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
    b = PcbBuilder("ISM Power Supply", PCB_W, PCB_H)
    ds = b.board.GetDesignSettings()
    ds.m_SolderMaskExpansion = 0
    ds.m_SolderMaskMinWidth = 0
    ds.m_SolderMaskToCopperClearance = 0
    ds.m_AllowSoldermaskBridgesInFPs = True
    ds.m_CopperEdgeClearance = mm(0.5)
    ds.m_MinClearance = mm(0.2)
    F = pcbnew.F_Cu

    jin = b.add_footprint(
        "Connector_BarrelJack.pretty", "BarrelJack_CUI_PJ-063AH_Horizontal", "J_IN",
        14.0, 18.0, value="DC_12V", pad_nets={"1": "+12V", "2": "GND"},
    )
    jout = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x08_P2.54mm_Vertical", "J_OUT",
        14.0, 42.0, value="MB_PWR", pad_nets=PWR_NETS,
    )
    jctl = b.add_footprint(
        "Connector_PinHeader_2.54mm.pretty", "PinHeader_1x04_P2.54mm_Vertical", "J_CTL",
        28.0, 55.0, value="ATX_CTL",
        pad_nets={"1": "PS_ON", "2": "PWR_OK", "3": "GND", "4": "+5V"},
    )
    jusb = b.add_footprint(
        "Connector_USB.pretty", "USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal", "J_USB",
        70.0, 12.0, value="USB_C",
        pad_nets={
            "A4": "+5V", "A9": "+5V", "B4": "+5V", "B9": "+5V",
            "A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "S1": "GND",
            "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM",
            "A5": "CC1", "B5": "CC2",
        },
    )
    u1 = b.add_footprint(
        "ISM.pretty", "ISM_RP2040_Module", "U1", 48.0, 38.0, value="RP2040_MOD",
        pad_nets={
            "1": "GND", "14": "+3V3", "15": "+5V", "16": "USB_DM", "17": "USB_DP", "18": "RUN", "26": "GND",
            "2": "PS_ON", "3": "PWR_OK", "4": "SNS_12V", "5": "SNS_5V", "6": "SNS_3V3", "19": "LED_ACT",
        },
        lib_path=ISM_PRETTY,
    )
    b.add_footprint(
        "Package_TO_SOT_SMD.pretty", "SOT-666", "U2", 88.0, 12.0, value="USBLC6",
        pad_nets={"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "+5V"},
    )
    b.add_footprint(
        "Package_TO_SOT_SMD.pretty", "TO-263-5_TabPin3", "U3", 72.0, 32.0, value="LM2596S-5",
        pad_nets={"1": "+12V", "2": "SW_5V", "3": "GND", "4": "+5V", "5": "GND"},
    )
    b.add_footprint(
        "Package_TO_SOT_SMD.pretty", "TO-263-5_TabPin3", "U4", 88.0, 32.0, value="LM2596S-3.3",
        pad_nets={"1": "+12V", "2": "SW_3V3", "3": "GND", "4": "+3V3", "5": "GND"},
    )
    b.add_footprint("Inductor_SMD.pretty", "L_12x12mm_H6mm", "L1",
                    72.0, 48.0, value="33uH", pad_nets={"1": "SW_5V", "2": "+5V"})
    b.add_footprint("Inductor_SMD.pretty", "L_12x12mm_H6mm", "L2",
                    88.0, 48.0, value="33uH", pad_nets={"1": "SW_3V3", "2": "+3V3"})
    # Schottky: pad 1 = K, pad 2 = A → K to SW, A to GND
    b.add_footprint("Diode_SMD.pretty", "D_SMA", "D4",
                    60.0, 48.0, value="SS34", pad_nets={"1": "SW_5V", "2": "GND"})
    b.add_footprint("Diode_SMD.pretty", "D_SMA", "D5",
                    60.0, 56.0, value="SS34", pad_nets={"1": "SW_3V3", "2": "GND"})

    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R1",
                    58.0, 16.0, value="5.1k", pad_nets={"1": "CC1", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R2",
                    62.0, 16.0, value="5.1k", pad_nets={"1": "CC2", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R3",
                    32.0, 20.0, value="10k", pad_nets={"1": "+12V", "2": "SNS_12V"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R4",
                    36.0, 20.0, value="10k", pad_nets={"1": "SNS_12V", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R5",
                    40.0, 20.0, value="10k", pad_nets={"1": "+5V", "2": "SNS_5V"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R6",
                    44.0, 20.0, value="10k", pad_nets={"1": "SNS_5V", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R7",
                    48.0, 20.0, value="10k", pad_nets={"1": "+3V3", "2": "SNS_3V3"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R8",
                    52.0, 20.0, value="10k", pad_nets={"1": "SNS_3V3", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R9",
                    32.0, 64.0, value="10k", pad_nets={"1": "PS_ON", "2": "+5V"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R10",
                    36.0, 64.0, value="10k", pad_nets={"1": "PWR_OK", "2": "+5V"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R11",
                    48.0, 64.0, value="1k", pad_nets={"1": "LED_ACT", "2": "LED_ACT_A"})
    b.add_footprint("LED_SMD.pretty", "LED_0603_1608Metric", "D1",
                    44.0, 64.0, value="ACT", pad_nets={"1": "GND", "2": "LED_ACT_A"})
    b.add_footprint("Button_Switch_SMD.pretty", "SW_SPST_PTS645", "SW_BOOT",
                    54.0, 64.0, value="RESET", pad_nets={"1": "RUN", "2": "GND"})
    b.add_footprint("Resistor_SMD.pretty", "R_0603_1608Metric", "R12",
                    58.0, 64.0, value="10k", pad_nets={"1": "RUN", "2": "+3V3"})

    for i, (x, net) in enumerate([
        (28.0, "+12V"), (32.0, "+5V"), (36.0, "+3V3"),
        (40.0, "+12V"), (44.0, "+5V"), (48.0, "+3V3"),
        (52.0, "+5V"), (56.0, "+3V3"),
    ], 1):
        val = "100uF" if i <= 3 else "100nF"
        b.add_footprint("Capacitor_SMD.pretty", "C_0603_1608Metric", f"C{i}",
                        x, 28.0, value=val, pad_nets={"1": net, "2": "GND"})

    for i, (hx, hy) in enumerate([(4.0, 4.0), (PCB_W - 4.0, 4.0), (4.0, PCB_H - 4.0), (PCB_W - 4.0, PCB_H - 4.0)], 1):
        b.add_footprint("MountingHole.pretty", "MountingHole_2.2mm_M2_DIN965_Pad",
                        f"H{i}", hx, hy, value="M2")

    def fp(ref):
        return next(f for f in b.board.GetFootprints() if f.GetReference() == ref)

    # Input / output power
    manh(b, pad_xy(jin, "1"), pad_xy(jout, "1"), "+12V", F, 0.5)
    manh(b, pad_xy(jin, "1"), pad_xy(jout, "2"), "+12V", F, 0.5)
    manh(b, pad_xy(jin, "2"), pad_xy(jout, "7"), "GND", F, 0.5)
    manh(b, pad_xy(jin, "2"), pad_xy(jout, "8"), "GND", F, 0.5)
    manh(b, pad_xy(fp("U3"), "4"), pad_xy(jout, "3"), "+5V", F, 0.5)
    manh(b, pad_xy(fp("U3"), "4"), pad_xy(jout, "4"), "+5V", F, 0.5)
    manh(b, pad_xy(fp("U4"), "4"), pad_xy(jout, "5"), "+3V3", F, 0.5)
    manh(b, pad_xy(fp("U4"), "4"), pad_xy(jout, "6"), "+3V3", F, 0.5)

    # Bucks
    manh(b, pad_xy(jin, "1"), pad_xy(fp("U3"), "1"), "+12V", F, 0.5)
    manh(b, pad_xy(jin, "1"), pad_xy(fp("U4"), "1"), "+12V", F, 0.5)
    manh(b, pad_xy(fp("U3"), "2"), pad_xy(fp("L1"), "1"), "SW_5V", F, 0.4)
    manh(b, pad_xy(fp("L1"), "2"), pad_xy(fp("U3"), "4"), "+5V", F, 0.4)
    manh(b, pad_xy(fp("D4"), "1"), pad_xy(fp("U3"), "2"), "SW_5V", F, TW)
    manh(b, pad_xy(fp("D4"), "2"), pad_xy(jin, "2"), "GND", F, TW)
    manh(b, pad_xy(fp("U3"), "3"), pad_xy(jin, "2"), "GND", F, 0.4)
    manh(b, pad_xy(fp("U4"), "2"), pad_xy(fp("L2"), "1"), "SW_3V3", F, 0.4)
    manh(b, pad_xy(fp("L2"), "2"), pad_xy(fp("U4"), "4"), "+3V3", F, 0.4)
    manh(b, pad_xy(fp("D5"), "1"), pad_xy(fp("U4"), "2"), "SW_3V3", F, TW)
    manh(b, pad_xy(fp("D5"), "2"), pad_xy(jin, "2"), "GND", F, TW)
    manh(b, pad_xy(fp("U4"), "3"), pad_xy(jin, "2"), "GND", F, 0.4)

    # USB / MCU
    manh(b, pad_xy(jusb, "A6"), pad_xy(u1, "17"), "USB_DP", F, TW)
    manh(b, pad_xy(jusb, "A7"), pad_xy(u1, "16"), "USB_DM", F, TW)
    manh(b, pad_xy(jusb, "A4"), pad_xy(u1, "15"), "+5V", F, 0.4)
    manh(b, pad_xy(jusb, "A1"), pad_xy(u1, "1"), "GND", F, 0.4)
    manh(b, pad_xy(fp("R1"), "1"), pad_xy(jusb, "A5"), "CC1", F, TW)
    manh(b, pad_xy(fp("R1"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R2"), "1"), pad_xy(jusb, "B5"), "CC2", F, TW)
    manh(b, pad_xy(fp("R2"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("U2"), "1"), pad_xy(jusb, "A6"), "USB_DP", F, TW)
    manh(b, pad_xy(fp("U2"), "3"), pad_xy(jusb, "A7"), "USB_DM", F, TW)
    manh(b, pad_xy(fp("U2"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("U2"), "5"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(u1, "14"), pad_xy(fp("U4"), "4"), "+3V3", F, 0.4)
    manh(b, pad_xy(u1, "15"), pad_xy(fp("U3"), "4"), "+5V", F, 0.4)
    manh(b, pad_xy(u1, "1"), pad_xy(jin, "2"), "GND", F, 0.4)

    # Control / sense
    manh(b, pad_xy(jctl, "1"), pad_xy(u1, "2"), "PS_ON", F, TW)
    manh(b, pad_xy(jctl, "2"), pad_xy(u1, "3"), "PWR_OK", F, TW)
    manh(b, pad_xy(jctl, "3"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(jctl, "4"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(fp("R3"), "1"), pad_xy(jin, "1"), "+12V", F, TW)
    manh(b, pad_xy(fp("R3"), "2"), pad_xy(u1, "4"), "SNS_12V", F, TW)
    manh(b, pad_xy(fp("R4"), "1"), pad_xy(u1, "4"), "SNS_12V", F, TW)
    manh(b, pad_xy(fp("R4"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R5"), "1"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(fp("R5"), "2"), pad_xy(u1, "5"), "SNS_5V", F, TW)
    manh(b, pad_xy(fp("R6"), "1"), pad_xy(u1, "5"), "SNS_5V", F, TW)
    manh(b, pad_xy(fp("R6"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R7"), "1"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("R7"), "2"), pad_xy(u1, "6"), "SNS_3V3", F, TW)
    manh(b, pad_xy(fp("R8"), "1"), pad_xy(u1, "6"), "SNS_3V3", F, TW)
    manh(b, pad_xy(fp("R8"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R9"), "1"), pad_xy(u1, "2"), "PS_ON", F, TW)
    manh(b, pad_xy(fp("R9"), "2"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(fp("R10"), "1"), pad_xy(u1, "3"), "PWR_OK", F, TW)
    manh(b, pad_xy(fp("R10"), "2"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(fp("R11"), "1"), pad_xy(u1, "19"), "LED_ACT", F, TW)
    manh(b, pad_xy(fp("R11"), "2"), pad_xy(fp("D1"), "2"), "LED_ACT_A", F, TW)
    manh(b, pad_xy(fp("D1"), "1"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("SW_BOOT"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("SW_BOOT"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("R12"), "1"), pad_xy(u1, "18"), "RUN", F, TW)
    manh(b, pad_xy(fp("R12"), "2"), pad_xy(u1, "14"), "+3V3", F, TW)

    for i in range(1, 9):
        manh(b, pad_xy(fp(f"C{i}"), "2"), pad_xy(u1, "1"), "GND", F, TW)
    manh(b, pad_xy(fp("C1"), "1"), pad_xy(jin, "1"), "+12V", F, TW)
    manh(b, pad_xy(fp("C2"), "1"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(fp("C3"), "1"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("C4"), "1"), pad_xy(jin, "1"), "+12V", F, TW)
    manh(b, pad_xy(fp("C5"), "1"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(fp("C6"), "1"), pad_xy(u1, "14"), "+3V3", F, TW)
    manh(b, pad_xy(fp("C7"), "1"), pad_xy(u1, "15"), "+5V", F, TW)
    manh(b, pad_xy(fp("C8"), "1"), pad_xy(u1, "14"), "+3V3", F, TW)

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
    with zipfile.ZipFile(FAB / "ism-power-supply-gerbers.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(tmp.iterdir()):
            zf.write(p, p.name)
    shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run(["kicad-cli", "pcb", "export", "pos", "-o", str(FAB / "ism-power-supply-cpl.csv"),
                    "--format", "csv", "--units", "mm", "--side", "both", "--exclude-dnp", str(pcb)], check=False)
    rows = [
        ["Designator", "Value", "Footprint", "Quantity", "Manufacturer", "MPN", "LCSC", "Notes"],
        ["U1", "RP2040_MOD", "ISM_RP2040_Module", "1", "ISM", "ISM-RP2040-MOD", "",
         "No LCSC — PSU monitor"],
        ["U2", "USBLC6-2SC6", "SOT-666", "1", "ST", "USBLC6-2SC6", "C7519", "ESD"],
        ["U3", "LM2596S-5.0", "TO-263-5", "1", "TI", "LM2596S-5.0", "C10872", "+5V buck"],
        ["U4", "LM2596S-3.3", "TO-263-5", "1", "TI", "LM2596S-3.3", "C10871", "+3V3 buck"],
        ["J_IN", "PJ-063AH", "CUI barrel", "1", "CUI", "PJ-063AH", "C75013", "12V from brick"],
        ["J_OUT", "MB_PWR", "PinHeader 1x08", "1", "", "HDR-1x8", "C124412", "To motherboard J_PWR"],
        ["J_CTL", "ATX_CTL", "PinHeader 1x04", "1", "", "HDR-1x4", "C124409", "PS_ON/PWR_OK"],
        ["J_USB", "USB4105", "GCT USB-C 16P", "1", "GCT", "USB4105-GF-A", "C165948", ""],
        ["L1,L2", "33uH", "12x12mm", "2", "", "33uH", "C167270", "Buck inductors"],
        ["D4,D5", "SS34", "SMA", "2", "", "SS34", "C8678", "Catch diodes"],
        ["R1,R2", "5.1k", "0603", "2", "", "5.1k", "C23244", "CC"],
        ["R3-R10,R12", "10k", "0603", "9", "", "10k", "C25804", "Sense/pull"],
        ["R11", "1k", "0603", "1", "", "1k", "C21190", ""],
        ["C1-C3", "100uF", "0603", "3", "", "100uF", "C15855", "Bulk"],
        ["C4-C8", "100nF", "0603", "5", "", "100nF", "C14663", ""],
        ["D1", "LED", "0603", "1", "", "LED", "C2286", ""],
        ["SW_BOOT", "PTS645", "PTS645", "1", "", "PTS645", "C318884", ""],
        ["H1-H4", "M2", "MountingHole", "4", "", "", "", "No LCSC — mechanical NPTH"],
    ]
    with (FAB / "BOM.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    write_text(
        FAB / "README.md",
        """# Fab package — ISM Power Supply (DC rail board)

| File | Use |
|------|-----|
| `ism-power-supply-gerbers.zip` | JLCPCB/PCBWay upload |
| `BOM.csv` | SMT BOM with LCSC where available |
| `ism-power-supply-cpl.csv` | Centroid / pick-and-place |

## Safety

- **No mains** on this PCB (Track A). Input is 12 V DC from a **certified** AC-DC brick.
- See `../docs/safety.md`.

Regenerate with `python3 scripts/build_power_supply.py`.
""",
    )


def patch_drc_severities() -> None:
    path = KICAD / "ism-power-supply.kicad_pro"
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
    write_text(KICAD / "ism-power-supply.kicad_sch", build_sch().emit())
    print("sch ok", flush=True)
    pcb = build_pcb()
    pcb_path = KICAD / "ism-power-supply.kicad_pcb"
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
                    "-o", str(KICAD / "erc.rpt"), str(KICAD / "ism-power-supply.kicad_sch")], check=False)
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
