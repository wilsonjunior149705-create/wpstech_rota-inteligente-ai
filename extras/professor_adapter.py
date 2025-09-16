
from __future__ import annotations
import argparse, csv
from pathlib import Path
from typing import Optional

# Este adaptador usa networkx e matplotlib localmente (na sua máquina).
# Instale-os se necessário:
#   pip install networkx matplotlib pandas

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

EXPECTED_COLS = ["Origem","Destino","Rua","Distancia_km","Tempo_min","Condicao"]

def load_professor_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in EXPECTED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV faltando colunas: {missing}.")
    return df

def make_graph(df: pd.DataFrame) -> nx.DiGraph:
    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(
            row["Origem"],
            row["Destino"],
            rua=row["Rua"],
            distancia=float(row["Distancia_km"]),
            tempo=float(row["Tempo_min"]),
            condicao=row["Condicao"],
        )
    return G

def save_plot(G: nx.DiGraph, path_nodes: Optional[list], out_path: Path):
    pos = nx.spring_layout(G, seed=42, weight='distancia')
    plt.figure(figsize=(12,9))
    nx.draw_networkx_nodes(G, pos, node_size=300)
    nx.draw_networkx_labels(G, pos, font_size=8)
    widths = []
    edges = list(G.edges())
    highlight = set(zip(path_nodes, path_nodes[1:])) if path_nodes else set()
    for (u,v) in edges:
        widths.append(3.0 if (u,v) in highlight else 1.0)
    nx.draw_networkx_edges(G, pos, width=widths, arrows=True, arrowsize=15)
    plt.title("Rede de Trânsito (caminho destacado)")
    plt.axis("off")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close()

def convert_to_project(df: pd.DataFrame, out_dir: Path):
    """Gera pontos/arestas compatíveis com o projeto:
    - points_prof.csv: ids e coordenadas (spring_layout)
    - edges_prof.csv: arestas com distância
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    G = make_graph(df)
    pos = nx.spring_layout(G, seed=42, weight='distancia')

    nodes = list(G.nodes())
    id_map = {name: idx for idx, name in enumerate(nodes)}

    xs = [pos[n][0] for n in nodes]
    ys = [pos[n][1] for n in nodes]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    def scale(v, lo, hi):
        return 50.0 if (hi - lo) < 1e-12 else ( (v - lo) / (hi - lo) ) * 100.0

    with (out_dir/"points_prof.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["id","x","y","name"])
        for name, idx in id_map.items():
            x = scale(pos[name][0], minx, maxx)
            y = scale(pos[name][1], miny, maxy)
            w.writerow([idx, round(x,3), round(y,3), name])

    with (out_dir/"edges_prof.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["source","target","distance","rua","tempo_min","condicao","orig_name","dest_name"])
        for u,v,data in G.edges(data=True):
            w.writerow([id_map[u], id_map[v], data.get("distancia",1.0), data.get("rua",""), data.get("tempo",0.0), data.get("condicao",""), u, v])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(Path(__file__).resolve().parents[1] / "data" / "rede_transito_brasil.csv"))
    ap.add_argument("--metric", choices=["distancia","tempo"], default="distancia")
    ap.add_argument("--origin")
    ap.add_argument("--dest")
    ap.add_argument("--outputs_dir", default=str(Path(__file__).resolve().parents[1] / "outputs"))
    ap.add_argument("--convert_only", action="store_true")
    args = ap.parse_args()

    df = load_professor_csv(Path(args.csv))
    G = make_graph(df)

    # Sempre converter p/ arquivos do projeto
    convert_to_project(df, Path(args.outputs_dir))

    if args.convert_only:
        print("Conversão concluída em", args.outputs_dir)
        return

    if not args.origin or not args.dest:
        print("Forneça --origin e --dest (ex.: --origin 'São Paulo' --dest 'Rio de Janeiro').")
        print("Primeiras cidades disponíveis:", list(list(G.nodes())[:15]))
        return

    path = nx.shortest_path(G, source=args.origin, target=args.dest, weight=args.metric)
    cost = nx.shortest_path_length(G, source=args.origin, target=args.dest, weight=args.metric)
    print(f"Caminho ({args.metric}) de {args.origin} para {args.dest}:")
    print(" -> ".join(path))
    print(f"Custo total: {cost:.2f}")
    save_plot(G, path_nodes=path, out_path=Path(args.outputs_dir)/f"caminho_{args.metric}.png")

if __name__ == "__main__":
    main()
