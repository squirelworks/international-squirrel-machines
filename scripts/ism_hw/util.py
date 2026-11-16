"""Shared helpers for ISM KiCad / fab generation."""

from __future__ import annotations

import hashlib
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
KICAD_SYM = Path("/usr/share/kicad/symbols")
KICAD_FP = Path("/usr/share/kicad/footprints")


def new_uuid(seed: str | None = None) -> str:
    if seed is None:
        return str(uuid.uuid4())
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()
    return str(uuid.UUID(digest[:32]))


def extract_symbol(lib_path: Path, symbol_name: str) -> str:
    """Return one top-level symbol block from a .kicad_sym library, renumbered for embedding."""
    text = lib_path.read_text(encoding="utf-8")
    needle = f'(symbol "{symbol_name}"'
    start = text.find(needle)
    if start < 0:
        # try extends-only symbols by resolving parent later
        raise KeyError(f"{symbol_name} not in {lib_path}")
    # walk to matching close at column of opening paren depth from start
    i = start
    depth = 0
    while i < len(text):
        ch = text[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                block = text[start : i + 1]
                break
        i += 1
    else:
        raise ValueError(f"Unclosed symbol {symbol_name}")
    # Prefix lib id as Device-style embed: keep name; KiCad embeds use bare name in lib_symbols
    return block


def _extract_raw_symbol(lib_path: Path, symbol_name: str) -> str:
    text = lib_path.read_text(encoding="utf-8")
    needle = f'(symbol "{symbol_name}"'
    start = text.find(needle)
    if start < 0:
        raise KeyError(f"{symbol_name} not in {lib_path}")
    i = start
    depth = 0
    while i < len(text):
        ch = text[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
        i += 1
    raise ValueError(f"Unclosed symbol {symbol_name}")


def extract_symbol_with_extends(lib_path: Path, symbol_name: str) -> list[str]:
    """Extract a symbol flattened for schematic embedding.

    KiCad rejects embedded lib_symbols that use (extends ...). If the requested
    symbol extends a parent, copy the parent's full definition and rename it to
    the requested symbol name (and unit child prefixes).
    """
    import re

    block = _extract_raw_symbol(lib_path, symbol_name)
    m = re.search(r'\(extends "([^"]+)"\)', block)
    if not m:
        return [block]
    parent_name = m.group(1)
    # Walk to non-extends root
    root_name = parent_name
    while True:
        root_block = _extract_raw_symbol(lib_path, root_name)
        m2 = re.search(r'\(extends "([^"]+)"\)', root_block)
        if not m2:
            break
        root_name = m2.group(1)
    root_block = _extract_raw_symbol(lib_path, root_name)
    # Rename root -> symbol_name
    flat = root_block.replace(f'(symbol "{root_name}"', f'(symbol "{symbol_name}"', 1)
    flat = flat.replace(f'(symbol "{root_name}_', f'(symbol "{symbol_name}_')
    # Prefer the derived Value property text from the extends stub when present
    vm = re.search(r'\(property "Value" "([^"]+)"', block)
    if vm:
        flat = re.sub(
            r'\(property "Value" "[^"]*"',
            f'(property "Value" "{vm.group(1)}"',
            flat,
            count=1,
        )
    return [flat]


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
