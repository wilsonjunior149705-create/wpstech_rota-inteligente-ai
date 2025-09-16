
from __future__ import annotations
import csv, json
from pathlib import Path
import matplotlib.pyplot as plt

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

def main():
    base = Path(__file__).resolve().parent.parent
    data_dir = base / "data"
    outputs_dir = base / "outputs"
    docs_dir = base / "docs"; docs_dir.mkdir(exist_ok=True, parents=True)

    points = read_points(data_dir / "points.csv")
    edges = read_edges(data_dir / "edges.csv")

    plt.figure()
    for u,v,w in edges:
        x1,y1 = points[u]; x2,y2 = points[v]
        plt.plot([x1,x2],[y1,y2], linewidth=1)

    xs = [p[0] for p in points.values()]
    ys = [p[1] for p in points.values()]
    plt.scatter(xs, ys)
    for nid,(x,y) in points.items():
        plt.text(x, y, str(nid), fontsize=8)

    sol_path = outputs_dir / "solution.json"
    if sol_path.exists():
        sol = json.loads(sol_path.read_text())
        for cid, info in sol["cluster_solutions"].items():
            path_nodes = info["path_nodes"]
            for a,b in zip(path_nodes, path_nodes[1:]):
                x1,y1 = points[a]; x2,y2 = points[b]
                plt.plot([x1,x2],[y1,y2], linewidth=2)

    plt.title("Cidade como Grafo + Rotas")
    plt.xlabel("x"); plt.ylabel("y")
    fig_path = docs_dir / "grafo_e_rotas.png"
    plt.savefig(fig_path, dpi=160, bbox_inches="tight")
    print(f"Saved diagram to: {fig_path}")

if __name__ == "__main__":
    main()
