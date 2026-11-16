"""KiCad 8 PCB builder via pcbnew."""

from __future__ import annotations

from pathlib import Path

import pcbnew

from .util import KICAD_FP, new_uuid


def mm(x: float) -> int:
    return int(pcbnew.FromMM(x))


class PcbBuilder:
    def __init__(self, title: str, width_mm: float, height_mm: float) -> None:
        self.board = pcbnew.BOARD()
        self.board.SetCopperLayerCount(4)
        self.board.GetDesignSettings().SetCopperLayerCount(4)
        self.board.GetDesignSettings().m_CopperEdgeClearance = mm(0.5)
        self.board.GetDesignSettings().m_MinClearance = mm(0.2)
        self.board.GetDesignSettings().m_TrackMinWidth = mm(0.2)
        self.board.GetDesignSettings().m_ViasMinSize = mm(0.6)
        self.board.GetDesignSettings().m_ViasMinDrill = mm(0.3)
        self.board.GetDesignSettings().m_HoleClearance = mm(0.15)
        self.title = title
        self.width_mm = width_mm
        self.height_mm = height_mm
        self._nets: dict[str, pcbnew.NETINFO_ITEM] = {}
        self._ensure_net("")  # net 0
        self._add_edge_cuts(width_mm, height_mm)
        self._add_title(title)

    def _ensure_net(self, name: str) -> pcbnew.NETINFO_ITEM:
        if name in self._nets:
            return self._nets[name]
        net = pcbnew.NETINFO_ITEM(self.board, name)
        self.board.Add(net)
        self._nets[name] = net
        return net

    def _add_edge_cuts(self, w: float, h: float, margin: float = 0.0) -> None:
        def seg(x1, y1, x2, y2):
            s = pcbnew.PCB_SHAPE(self.board)
            s.SetShape(pcbnew.SHAPE_T_SEGMENT)
            s.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1)))
            s.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
            s.SetLayer(pcbnew.Edge_Cuts)
            s.SetWidth(mm(0.15))
            self.board.Add(s)

        x0, y0 = margin, margin
        x1, y1 = w - margin, h - margin
        seg(x0, y0, x1, y0)
        seg(x1, y0, x1, y1)
        seg(x1, y1, x0, y1)
        seg(x0, y1, x0, y0)

    def _add_title(self, title: str) -> None:
        t = pcbnew.PCB_TEXT(self.board)
        t.SetText(title)
        t.SetLayer(pcbnew.F_SilkS)
        t.SetPosition(pcbnew.VECTOR2I(mm(5), mm(3)))
        t.SetTextSize(pcbnew.VECTOR2I(mm(1.5), mm(1.5)))
        t.SetTextThickness(mm(0.2))
        self.board.Add(t)

    def add_footprint(
        self,
        pretty: str,
        name: str,
        ref: str,
        x_mm: float,
        y_mm: float,
        rotation_deg: float = 0.0,
        value: str = "",
        pad_nets: dict[str, str] | None = None,
        bottom: bool = False,
        lib_path: Path | None = None,
    ) -> pcbnew.FOOTPRINT:
        lib = str(lib_path) if lib_path is not None else str(KICAD_FP / pretty)
        fp = pcbnew.FootprintLoad(lib, name)
        if fp is None:
            raise FileNotFoundError(f"{lib}:{name}")
        fp.SetReference(ref)
        if value:
            fp.SetValue(value)
        fp.SetPosition(pcbnew.VECTOR2I(mm(x_mm), mm(y_mm)))
        if rotation_deg:
            fp.SetOrientation(pcbnew.EDA_ANGLE(rotation_deg, pcbnew.DEGREES_T))
        if bottom:
            # aFlipLeftRight=True is the safe KiCad 8 path in headless pcbnew
            fp.Flip(fp.GetPosition(), True)
        self.board.Add(fp)
        if pad_nets:
            for pad in fp.Pads():
                key = pad.GetNumber()
                if key in pad_nets:
                    net = self._ensure_net(pad_nets[key])
                    pad.SetNet(net)
        return fp

    def add_track(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        net_name: str,
        width: float = 0.25,
        layer=None,
    ) -> None:
        if layer is None:
            layer = pcbnew.F_Cu
        track = pcbnew.PCB_TRACK(self.board)
        track.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1)))
        track.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
        track.SetWidth(mm(width))
        track.SetLayer(layer)
        track.SetNet(self._ensure_net(net_name))
        self.board.Add(track)

    def add_via(self, x: float, y: float, net_name: str, diameter: float = 0.6, drill: float = 0.3) -> None:
        via = pcbnew.PCB_VIA(self.board)
        via.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        via.SetWidth(mm(diameter))
        via.SetDrill(mm(drill))
        via.SetNet(self._ensure_net(net_name))
        self.board.Add(via)

    def add_mounting_hole(self, x: float, y: float, drill: float = 2.2) -> None:
        # Use MountingHole footprint if available
        try:
            self.add_footprint(
                "MountingHole.pretty",
                "MountingHole_2.2mm_M2",
                f"H{int(x)}{int(y)}",
                x,
                y,
                value="Mount",
            )
        except FileNotFoundError:
            # raw NPTH pad footprint fallback via circle edge? skip
            pass

    def add_filled_zone(self, net_name: str, layer, outline: list[tuple[float, float]], clearance: float = 0.2) -> None:
        zone = pcbnew.ZONE(self.board)
        zone.SetNet(self._ensure_net(net_name))
        zone.SetLayer(layer)
        zone.SetLocalClearance(mm(clearance))
        zone.SetMinThickness(mm(0.25))
        zone.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        zone.Outline().NewOutline()
        for x, y in outline:
            zone.Outline().Append(mm(x), mm(y))
        self.board.Add(zone)

    def pour_gnd_rect(self) -> None:
        w, h = self.width_mm, self.height_mm
        outline = [(1, 1), (w - 1, 1), (w - 1, h - 1), (1, h - 1)]
        for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
            self.add_filled_zone("GND", layer, outline)

    def refill_zones(self) -> None:
        filler = pcbnew.ZONE_FILLER(self.board)
        filler.Fill(self.board.Zones())

    def save(self, path: Path | str) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        pcbnew.SaveBoard(str(path), self.board)
