"""Load symbols from KiCad system libs or ISM project libs."""

from __future__ import annotations

from pathlib import Path

from .util import REPO_ROOT, extract_symbol_with_extends, KICAD_SYM


ISM_SYM = REPO_ROOT / "common" / "kicad" / "ISM.kicad_sym"


def load_symbol(lib_file: str, symbol_name: str) -> list[str]:
    if lib_file == "ISM.kicad_sym":
        return extract_symbol_with_extends(ISM_SYM, symbol_name)
    return extract_symbol_with_extends(KICAD_SYM / lib_file, symbol_name)
