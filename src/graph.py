
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import heapq, math

@dataclass
class Graph:
    adj: Dict[int, List[Tuple[int, float]]] = field(default_factory=dict)

    def add_edge(self, u: int, v: int, w: float) -> None:
        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, []).append((u, w))

    def neighbors(self, u: int) -> List[Tuple[int, float]]:
        return self.adj.get(u, [])

def euclidean(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0]-b[0], a[1]-b[1])

def astar(graph: Graph, start: int, goal: int, coords: Dict[int, Tuple[float,float]]):
    if start == goal:
        return 0.0, [start]
    open_set = [(0.0, start)]
    g = {start: 0.0}
    parent = {}
    def h(n): return euclidean(coords[n], coords[goal])
    while open_set:
        _, u = heapq.heappop(open_set)
        if u == goal:
            path = [u]
            while u in parent:
                u = parent[u]
                path.append(u)
            path.reverse()
            return g[path[-1]], path
        for v,w in graph.neighbors(u):
            ng = g[u] + w
            if ng < g.get(v, float('inf')):
                parent[v] = u
                g[v] = ng
                f = ng + h(v)
                heapq.heappush(open_set, (f, v))
    return float('inf'), []

def dijkstra_all(graph: Graph, source: int):
    dist = {source: 0.0}
    pq = [(0.0, source)]
    vis = set()
    while pq:
        d,u = heapq.heappop(pq)
        if u in vis: continue
        vis.add(u)
        for v,w in graph.neighbors(u):
            nd = d + w
            if nd < dist.get(v, float('inf')):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist
