# ============================
# 📂 1. Importar bibliotecas
# ============================
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import random

# ============================
# 📥 2. Carregar dataset
# ============================
df = pd.read_csv("rede_transito_brasil.csv")

print("✅ Arquivo carregado com sucesso!")
print("Total de registros:", len(df))
print("\nExemplo de dados:\n", df.head())

# ============================
# 📊 3. Estatísticas básicas
# ============================
print("\n📊 Estatísticas das distâncias (km):")
print(df["Distancia_km"].describe())

print("\n⏱️ Estatísticas dos tempos (min):")
print(df["Tempo_min"].describe())

print("\n🚦 Condições das ruas:")
print(df["Condicao"].value_counts())

print("\n🏙️ Top 5 cidades de origem mais usadas:")
print(df["Origem"].value_counts().head())

print("\n🎯 Top 5 cidades de destino mais usadas:")
print(df["Destino"].value_counts().head())

# ============================
# 🌐 4. Criar grafo
# ============================
G = nx.DiGraph()

for _, row in df.iterrows():
    G.add_edge(
        row["Origem"],
        row["Destino"],
        rua=row["Rua"],
        distancia=row["Distancia_km"],
        tempo=row["Tempo_min"],
        condicao=row["Condicao"]
    )

print("\n🔗 Grafo criado com", G.number_of_nodes(), "cidades e", G.number_of_edges(), "ruas.")

# ============================
# 🎨 5. Definir cores por condição
# ============================
cores = {
    "Boa": "green",
    "Moderada": "orange",
    "Ruim": "red",
    "Obras": "gray"  # adicionar outras condições do dataset se necessário
}

# ============================
# 6. Calcular caminho mais curto (distância) entre duas cidades aleatórias
# ============================
if G.number_of_nodes() >= 2:
    origem, destino = random.sample(list(G.nodes()), 2)  # garante que são diferentes
    try:
        caminho = nx.shortest_path(G, source=origem, target=destino, weight="distancia")
        distancia_total = nx.shortest_path_length(G, source=origem, target=destino, weight="distancia")
        print(f"\n🚗 Caminho mais curto entre {origem} e {destino}: {caminho}")
        print(f"Distância total: {distancia_total:.2f} km")
    except nx.NetworkXNoPath:
        print(f"\n❌ Não há caminho entre {origem} e {destino}.")

# ============================
# 🗺️ 7. Visualizar grafo com cores corretas e caminho mais curto
# ============================
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42)

# Nós e labels
nx.draw_networkx_nodes(G, pos, node_size=600, node_color="skyblue", edgecolors="black")
nx.draw_networkx_labels(G, pos, font_size=8)

# Criar conjunto de arestas do caminho mais curto
arestas_caminho = set()
if caminho:
    for i in range(len(caminho) - 1):
        arestas_caminho.add((caminho[i], caminho[i+1]))
        arestas_caminho.add((caminho[i+1], caminho[i]))  # grafos não direcionados

# Definir cores das arestas
edge_colors = []
for u, v in G.edges():
    if (u, v) in arestas_caminho:
        edge_colors.append("red")  # caminho mais curto
    else:
        edge_colors.append(cores.get(G[u][v]["condicao"], "black"))  # cor por condição

#nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2)
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2, arrows=True, arrowsize=20)


# Criar legenda usando Line2D
legend_handles = []
for cond, cor in cores.items():
    # só adicionar à legenda se a condição estiver presente nas arestas
    if any(G[u][v]["condicao"] == cond for u, v in G.edges()):
        legend_handles.append(mlines.Line2D([], [], color=cor, linewidth=2, label=cond))
if caminho:
    legend_handles.append(mlines.Line2D([], [], color="red", linewidth=2, label="Caminho mais curto"))

plt.legend(handles=legend_handles, title="Condição da rua")
plt.title("🌐 Rede de Trânsito Simulada no Brasil (Caminho mais curto em vermelho)", fontsize=14)
plt.axis("off")
plt.show()

# ============================
# 📈 8. Métricas da rede
# ============================
print("\n📈 Métricas da Rede:")
print("Número de cidades (nós):", G.number_of_nodes())
print("Número de ruas (arestas):", G.number_of_edges())
print("Grau médio:", sum(dict(G.degree()).values())/G.number_of_nodes())
print("Densidade da rede:", nx.density(G))
