"""Minimal KiCad 8 schematic builder (S-expression)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from .util import extract_symbol_with_extends, new_uuid, KICAD_SYM


@dataclass
class PinUuid:
    num: str
    uuid: str


@dataclass
class SchSymbol:
    lib_id: str  # e.g. "Device:R" -> embedded as Device_R or keep "Device:R"
    embed_name: str
    ref: str
    value: str
    at: tuple[float, float]
    rotation: int = 0
    footprint: str = ""
    fields: dict[str, str] = field(default_factory=dict)
    pin_numbers: list[str] = field(default_factory=list)
    unit: int = 1
    in_bom: bool = True
    on_board: bool = True
    dnp: bool = False
    uuid: str = ""

    def __post_init__(self) -> None:
        if not self.uuid:
            self.uuid = new_uuid(f"sym:{self.ref}")


@dataclass
class Wire:
    a: tuple[float, float]
    b: tuple[float, float]
    uuid: str = ""

    def __post_init__(self) -> None:
        if not self.uuid:
            self.uuid = new_uuid(f"wire:{self.a}:{self.b}")


@dataclass
class Label:
    text: str
    at: tuple[float, float]
    rotation: int = 0
    shape: str = "input"  # input/output/bidirectional/passive/etc for global? local uses label
    kind: str = "label"  # label | global_label | hierarchical_label
    uuid: str = ""

    def __post_init__(self) -> None:
        if not self.uuid:
            self.uuid = new_uuid(f"lbl:{self.kind}:{self.text}:{self.at}")


@dataclass
class NoConnect:
    at: tuple[float, float]
    uuid: str = ""

    def __post_init__(self) -> None:
        if not self.uuid:
            self.uuid = new_uuid(f"nc:{self.at}")


@dataclass
class Junction:
    at: tuple[float, float]
    uuid: str = ""

    def __post_init__(self) -> None:
        if not self.uuid:
            self.uuid = new_uuid(f"j:{self.at}")


class Schematic:
    def __init__(self, title: str, paper: str = "A2") -> None:
        self.title = title
        self.paper = paper
        self.symbols: list[SchSymbol] = []
        self.wires: list[Wire] = []
        self.labels: list[Label] = []
        self.noconnects: list[NoConnect] = []
        self.junctions: list[Junction] = []
        self.lib_blocks: dict[str, str] = {}  # embed_name -> sexpr
        self.texts: list[tuple[str, tuple[float, float], float]] = []

    def add_lib_symbol(self, lib_file: str, symbol_name: str, embed_name: str | None = None) -> str:
        from .libload import load_symbol

        embed = embed_name or symbol_name
        if embed in self.lib_blocks:
            return embed
        blocks = load_symbol(lib_file, symbol_name)
        # rewrite top symbol name to embed if needed; keep extends chain names as-is
        for block in blocks:
            # detect name
            import re

            m = re.match(r'\(symbol "([^"]+)"', block)
            assert m
            name = m.group(1)
            if name == symbol_name and embed != symbol_name:
                block = block.replace(f'(symbol "{symbol_name}"', f'(symbol "{embed}"', 1)
                # also rewrite child unit symbol prefixes
                block = block.replace(f'(symbol "{symbol_name}_', f'(symbol "{embed}_')
                name = embed
            if name not in self.lib_blocks:
                self.lib_blocks[name] = block
        return embed

    def add_symbol(self, sym: SchSymbol) -> SchSymbol:
        self.symbols.append(sym)
        return sym

    def wire(self, a: tuple[float, float], b: tuple[float, float]) -> None:
        self.wires.append(Wire(a, b))

    def label(self, text: str, at: tuple[float, float], rotation: int = 0, kind: str = "label") -> None:
        self.labels.append(Label(text=text, at=at, rotation=rotation, kind=kind))

    def nc(self, at: tuple[float, float]) -> None:
        self.noconnects.append(NoConnect(at=at))

    def junction(self, at: tuple[float, float]) -> None:
        self.junctions.append(Junction(at=at))

    def text(self, content: str, at: tuple[float, float], size: float = 1.27) -> None:
        self.texts.append((content, at, size))

    def emit(self) -> str:
        parts: list[str] = []
        parts.append("(kicad_sch")
        parts.append("  (version 20231120)")
        parts.append('  (generator "ism_hw")')
        parts.append('  (generator_version "8.0")')
        parts.append(f'  (uuid "{new_uuid("sheet:"+self.title)}")')
        parts.append(f'  (paper "{self.paper}")')
        parts.append("  (title_block")
        parts.append(f'    (title "{self.title}")')
        parts.append('    (date "2026-11-16")')
        parts.append('    (rev "0.1")')
        parts.append('    (company "International Squirrel Machines")')
        parts.append('    (comment 1 "Original ISM design - stock KiCad libs credited in README")')
        parts.append("  )")
        parts.append("  (lib_symbols")
        for name in sorted(self.lib_blocks):
            block = self.lib_blocks[name]
            indented = "\n".join("    " + line if line else line for line in block.splitlines())
            parts.append(indented)
        parts.append("  )")

        for w in self.wires:
            (x1, y1), (x2, y2) = w.a, w.b
            parts.append("  (wire (pts (xy %.3f %.3f) (xy %.3f %.3f))" % (x1, y1, x2, y2))
            parts.append('    (stroke (width 0) (type default))')
            parts.append(f'    (uuid "{w.uuid}")')
            parts.append("  )")

        for j in self.junctions:
            parts.append(f'  (junction (at {j.at[0]:.3f} {j.at[1]:.3f}) (diameter 0) (color 0 0 0 0)')
            parts.append(f'    (uuid "{j.uuid}")')
            parts.append("  )")

        for nc in self.noconnects:
            parts.append(f'  (no_connect (at {nc.at[0]:.3f} {nc.at[1]:.3f}) (uuid "{nc.uuid}"))')

        for lb in self.labels:
            if lb.kind == "global_label":
                parts.append(f'  (global_label "{lb.text}"')
                parts.append(f"    (shape {lb.shape})")
                parts.append(f"    (at {lb.at[0]:.3f} {lb.at[1]:.3f} {lb.rotation})")
                parts.append("    (effects (font (size 1.27 1.27)) (justify left))")
                parts.append(f'    (uuid "{lb.uuid}")')
                parts.append("  )")
            else:
                parts.append(f'  (label "{lb.text}"')
                parts.append(f"    (at {lb.at[0]:.3f} {lb.at[1]:.3f} {lb.rotation})")
                parts.append("    (effects (font (size 1.27 1.27)) (justify left bottom))")
                parts.append(f'    (uuid "{lb.uuid}")')
                parts.append("  )")

        for content, at, size in self.texts:
            escaped = content.replace("\\", "\\\\").replace('"', '\\"')
            parts.append(f'  (text "{escaped}"')
            parts.append(f"    (at {at[0]:.3f} {at[1]:.3f} 0)")
            parts.append(f"    (effects (font (size {size} {size})))")
            parts.append(f'    (uuid "{new_uuid("text:"+content[:20])}")')
            parts.append("  )")

        for sym in self.symbols:
            in_bom = "yes" if sym.in_bom else "no"
            on_board = "yes" if sym.on_board else "no"
            dnp = "yes" if sym.dnp else "no"
            parts.append(
                f'  (symbol (lib_id "{sym.embed_name}") (at {sym.at[0]:.3f} {sym.at[1]:.3f} {sym.rotation}) '
                f"(unit {sym.unit}) (exclude_from_sim no) (in_bom {in_bom}) (on_board {on_board}) (dnp {dnp}) "
                f"(fields_autoplaced yes)"
            )
            parts.append(f'    (uuid "{sym.uuid}")')
            parts.append(
                f'    (property "Reference" "{sym.ref}" (at {sym.at[0]:.3f} {sym.at[1]-2.54:.3f} 0) '
                f"(effects (font (size 1.27 1.27))))"
            )
            parts.append(
                f'    (property "Value" "{sym.value}" (at {sym.at[0]:.3f} {sym.at[1]+2.54:.3f} 0) '
                f"(effects (font (size 1.27 1.27))))"
            )
            fp = sym.footprint
            parts.append(
                f'    (property "Footprint" "{fp}" (at {sym.at[0]:.3f} {sym.at[1]:.3f} 0) '
                f"(effects (font (size 1.27 1.27)) hide))"
            )
            parts.append(
                f'    (property "Datasheet" "" (at {sym.at[0]:.3f} {sym.at[1]:.3f} 0) '
                f"(effects (font (size 1.27 1.27)) hide))"
            )
            for k, v in sym.fields.items():
                parts.append(
                    f'    (property "{k}" "{v}" (at {sym.at[0]:.3f} {sym.at[1]:.3f} 0) '
                    f"(effects (font (size 1.27 1.27)) hide))"
                )
            for pn in sym.pin_numbers:
                parts.append(f'    (pin "{pn}" (uuid "{new_uuid(f"pin:{sym.ref}:{pn}")}"))')
            parts.append("  )")

        parts.append(
            f'  (sheet_instances\n    (path "/" (page "1"))\n  )'
        )
        parts.append(")")
        return "\n".join(parts) + "\n"


def power_symbol_names() -> dict[str, str]:
    """Map logical power name -> symbol in power.kicad_sym."""
    return {
        "GND": "GND",
        "+3V3": "+3V3",
        "+5V": "+5V",
        "PWR_FLAG": "PWR_FLAG",
    }
