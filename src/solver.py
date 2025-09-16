
from __future__ import annotations
import csv, json, argparse
from pathlib import Path
from typing import Dict, Tuple, List
from graph import Graph, astar
from kmeans import kmeans
from routing import greedy_route_cover

def read_points(path: Path):
    points = {}
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            points[int(row["id"])] = (float(row["x"]), float(row["y"]))
    return points

def read_edges(path: Path):
    edges = []
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            edges.append((int(row["source"]), int(row["target"]), float(row["distance"])))
    return edges

def build_graph(edges):
    g = Graph()
    for u,v,w in edges:
        g.add_edge(u,v,w)
    return g

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", default=str(Path(__file__).resolve().parent.parent / "data"))
    ap.add_argument("--outputs_dir", default=str(Path(__file__).resolve().parent.parent / "outputs"))
    ap.add_argument("--origin", type=int, default=0)
    ap.add_argument("--deliveries", type=str, default="deliveries.csv")
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    outputs_dir = Path(args.outputs_dir); outputs_dir.mkdir(parents=True, exist_ok=True)

    points = read_points(data_dir / "points.csv")
    edges = read_edges(data_dir / "edges.csv")
    graph = build_graph(edges)

    deliveries = []
    with (data_dir / args.deliveries).open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            deliveries.append(int(row["node_id"]))

    delivery_points = [points[n] for n in deliveries]
    cents, labels = kmeans(delivery_points, k=args.k)

    clusters = {i: [] for i in range(args.k)}
    for node, lbl in zip(deliveries, labels):
        clusters[lbl].append(node)

    coords = points
    cluster_solutions = {}
    grand_total = 0.0
    for cid, stops in clusters.items():
        if not stops: continue
        total_cost, path_nodes, visit_order = greedy_route_cover(graph, coords, origin=args.origin, stops=stops)
        cluster_solutions[cid] = {
            "stops": stops,
            "visit_order": visit_order,
            "path_nodes": path_nodes,
            "total_cost": round(total_cost, 3),
        }
        grand_total += total_cost

    result = {"origin": args.origin, "k": args.k, "total_cost_all_clusters": round(grand_total,3), "cluster_solutions": cluster_solutions}
    (outputs_dir / "solution.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
