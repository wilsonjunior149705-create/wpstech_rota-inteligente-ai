# Rota Inteligente  

**Aluno:** Wilson Pierre • **RA:** 149705  
**Disciplina:** Artificial Intelligence Fundamentals  
**Tema:** Otimização de rotas de delivery com grafos + A* + K-Means  

---

## 1. Problema
A empresa de delivery tem atrasos frequentes nos horários de pico.  
O desafio é planejar as rotas de forma mais inteligente para **reduzir tempo e distância percorrida** pelos entregadores.  

---

## 2. Objetivos
- Representar a cidade como um **grafo ponderado** (nós = locais de entrega; arestas = ruas com custo).  
- Calcular **rotas de menor custo** a partir de um depósito/origem para várias entregas.  
- Usar **K-Means** para agrupar entregas em zonas e facilitar a divisão entre motoristas.  
- Comparar resultados em termos de **distância** e **tempo**.  

---

## 3. Como a solução funciona
1. **Dados → Grafo:** os CSVs são transformados em um grafo com pesos positivos.  
2. **Agrupamento (K-Means):** entregas são divididas em *k* zonas com base nas coordenadas.  
3. **Roteirização intra-zona:** cada zona é resolvida com uma heurística simples (vizinho mais próximo), mas as rotas ponto-a-ponto usam **A\***.  
4. **Avaliação:** soma dos custos e visualização do grafo com as rotas calculadas.  

---

## 4. Algoritmos usados
- **Dijkstra:** referência (ótimo garantido).  
- **A\*:** busca mais rápida quando há coordenadas, usando distância euclidiana como heurística.  
- **K-Means:** divide o problema em partes menores, permitindo paralelismo (um entregador por zona).  

---

## 5. Resultados iniciais
Exemplo com malha 6×6 (36 nós) e 12 entregas, usando **k = 3** zonas:  

- **Custo total:** 24.02 (distância).  
- Quanto maior o *k*, menor a rota média, mas aumenta a quantidade de zonas/entregadores.  

---

## 6. Limitações e melhorias
**Limitações:**  
- A solução é heurística, não garante o ótimo global.  
- Não considera fatores como capacidade do veículo, janelas de tempo ou tráfego em tempo real.  

**Possíveis melhorias:**  
- Aplicar refinamentos (ex.: 2-opt/3-opt).  
- Incluir custo ajustado por condição da via.  
- Evoluir para modelos VRPTW/CVRP.  

---

## 7. Como rodar
```bash
python src/solver.py --origin 21 --k 3
python src/visualize_graph.py
