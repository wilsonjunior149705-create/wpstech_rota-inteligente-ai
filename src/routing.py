
from __future__ import annotations
from typing import Dict, List, Tuple, Iterable, Set
from graph import Graph, astar

def greedy_route_cover(graph: Graph, coords: Dict[int, Tuple[float,float]], origin: int, stops: Iterable[int]):
    remaining: Set[int] = set(stops)
    path_nodes: List[int] = [origin]
    total_cost = 0.0
    current = origin
    visit_order: List[int] = []
    while remaining:
        best = None; best_cost = float('inf'); best_path=[]
        for s in remaining:
            c, p = astar(graph, current, s, coords)
            if c < best_cost:
                best_cost = c; best = s; best_path = p
        if best is None: break
        total_cost += best_cost
        if best_path and best_path[0]==current:
            path_nodes.extend(best_path[1:])
        else:
            path_nodes.extend(best_path)
        visit_order.append(best); current = best; remaining.remove(best)
    return total_cost, path_nodes, visit_order
