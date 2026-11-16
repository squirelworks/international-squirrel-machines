"""Simple clearance-aware Manhattan router for ISM PCBs."""

from __future__ import annotations

import heapq
import math
from dataclasses import dataclass

import pcbnew

from .pcb_builder import mm


@dataclass
class Obstacle:
    x: float
    y: float
    r: float


class GridRouter:
    def __init__(self, board: pcbnew.BOARD, pitch: float = 0.5, clearance: float = 0.35) -> None:
        self.board = board
        self.pitch = pitch
        self.clearance = clearance
        self.obstacles: list[Obstacle] = []
        self._collect_obstacles()

    def _collect_obstacles(self) -> None:
        for fp in self.board.GetFootprints():
            for pad in fp.Pads():
                pos = pad.GetPosition()
                x = pcbnew.ToMM(pos.x)
                y = pcbnew.ToMM(pos.y)
                # approximate radius from pad size / drill
                size = pad.GetSize()
                drill = pad.GetDrillSize()
                pr = max(pcbnew.ToMM(size.x), pcbnew.ToMM(size.y), pcbnew.ToMM(drill.x), pcbnew.ToMM(drill.y)) / 2.0
                self.obstacles.append(Obstacle(x, y, pr + self.clearance))

    def _blocked(self, x: float, y: float) -> bool:
        for ob in self.obstacles:
            if (x - ob.x) ** 2 + (y - ob.y) ** 2 <= ob.r ** 2:
                return True
        return False

    def _q(self, v: float) -> int:
        return int(round(v / self.pitch))

    def _from_q(self, i: int) -> float:
        return i * self.pitch

    def _set_net(self, item, net: str) -> None:
        ni = self.board.FindNet(net)
        if ni is not None:
            item.SetNet(ni)

    def track(self, x1: float, y1: float, x2: float, y2: float, net: str, layer, width: float = 0.25) -> None:
        tr = pcbnew.PCB_TRACK(self.board)
        tr.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1)))
        tr.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
        tr.SetWidth(mm(width))
        tr.SetLayer(layer)
        self._set_net(tr, net)
        self.board.Add(tr)

    def route_l(self, x1: float, y1: float, x2: float, y2: float, net: str, layer, width: float = 0.25, horizontal_first: bool = True) -> None:
        """Force an L-shaped Manhattan route (no obstacle search)."""
        if abs(x1 - x2) < 1e-6 or abs(y1 - y2) < 1e-6:
            self.track(x1, y1, x2, y2, net, layer, width)
            return
        if horizontal_first:
            self.track(x1, y1, x2, y1, net, layer, width)
            self.track(x2, y1, x2, y2, net, layer, width)
        else:
            self.track(x1, y1, x1, y2, net, layer, width)
            self.track(x1, y2, x2, y2, net, layer, width)

    def route(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        net: str,
        layer,
        width: float = 0.25,
        bbox: tuple[float, float, float, float] | None = None,
    ) -> bool:
        """A* Manhattan route; falls back to L-shape if search fails."""
        # Ignore obstacles near endpoints so pad centers are routable.
        def blocked(x: float, y: float) -> bool:
            if (x - x1) ** 2 + (y - y1) ** 2 <= 4.0 or (x - x2) ** 2 + (y - y2) ** 2 <= 4.0:
                return False
            return self._blocked(x, y)

        if bbox is None:
            bb = self.board.GetBoardEdgesBoundingBox()
            bbox = (
                pcbnew.ToMM(bb.GetLeft()) + 1,
                pcbnew.ToMM(bb.GetTop()) + 1,
                pcbnew.ToMM(bb.GetRight()) - 1,
                pcbnew.ToMM(bb.GetBottom()) - 1,
            )
        minx, miny, maxx, maxy = bbox
        sx, sy = self._q(x1), self._q(y1)
        gx, gy = self._q(x2), self._q(y2)
        xmin, xmax = self._q(minx), self._q(maxx)
        ymin, ymax = self._q(miny), self._q(maxy)

        def h(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        start = (sx, sy)
        goal = (gx, gy)
        open_h: list[tuple[int, tuple[int, int]]] = [(h(start, goal), start)]
        came: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        gscore = {start: 0}
        found = False
        steps = 0
        while open_h and steps < 200000:
            steps += 1
            _, cur = heapq.heappop(open_h)
            if cur == goal:
                found = True
                break
            cx, cy = cur
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nxt = (cx + dx, cy + dy)
                if nxt[0] < xmin or nxt[0] > xmax or nxt[1] < ymin or nxt[1] > ymax:
                    continue
                wx, wy = self._from_q(nxt[0]), self._from_q(nxt[1])
                if nxt != goal and nxt != start and blocked(wx, wy):
                    continue
                ng = gscore[cur] + 1
                if ng < gscore.get(nxt, 1_000_000):
                    gscore[nxt] = ng
                    came[nxt] = cur
                    heapq.heappush(open_h, (ng + h(nxt, goal), nxt))

        if not found:
            return False

        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = came[cur]
        path.reverse()

        def commit(a, b):
            ax, ay = self._from_q(a[0]), self._from_q(a[1])
            bx, by = self._from_q(b[0]), self._from_q(b[1])
            self.track(ax, ay, bx, by, net, layer, width)
            self._add_track_obstacles(ax, ay, bx, by, width)

        if len(path) == 1:
            return True
        # Ensure exact endpoint snaps to real pad centers
        self.track(x1, y1, self._from_q(path[0][0]), self._from_q(path[0][1]), net, layer, width)
        self._add_track_obstacles(x1, y1, self._from_q(path[0][0]), self._from_q(path[0][1]), width)
        run_start = path[0]
        prev = path[0]
        direction = None
        for p in path[1:]:
            d = (p[0] - prev[0], p[1] - prev[1])
            if direction is None:
                direction = d
            elif d != direction:
                commit(run_start, prev)
                run_start = prev
                direction = d
            prev = p
        commit(run_start, prev)
        self.track(self._from_q(path[-1][0]), self._from_q(path[-1][1]), x2, y2, net, layer, width)
        self._add_track_obstacles(self._from_q(path[-1][0]), self._from_q(path[-1][1]), x2, y2, width)
        return True

    def _add_track_obstacles(self, x1: float, y1: float, x2: float, y2: float, width: float) -> None:
        """Sample obstacle discs along a committed track so later nets avoid it."""
        r = width / 2.0 + self.clearance
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist < 1e-9:
            self.obstacles.append(Obstacle(x1, y1, r))
            return
        n = max(1, int(dist / (self.pitch * 0.5)))
        for i in range(n + 1):
            t = i / n
            self.obstacles.append(Obstacle(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, r))

    def via(self, x: float, y: float, net: str, top_layer=None, bottom_layer=None) -> None:
        via = pcbnew.PCB_VIA(self.board)
        via.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        via.SetWidth(mm(0.6))
        via.SetDrill(mm(0.3))
        if top_layer is not None and bottom_layer is not None:
            via.SetViaType(pcbnew.VIATYPE_BLIND_BURIED)
            via.SetLayerPair(top_layer, bottom_layer)
        ni = self.board.FindNet(net)
        if ni is not None:
            via.SetNet(ni)
        self.board.Add(via)
        self.obstacles.append(Obstacle(x, y, 0.3 + self.clearance))
