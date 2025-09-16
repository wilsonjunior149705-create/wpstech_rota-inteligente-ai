# Como Executar — Resumo

## Requisitos
- Python 3.10+
- `pip install -r requirements.txt`

## Passos
```bash
python src/solver.py --origin 21 --k 3
python src/visualize_graph.py
```
Saídas:
- `outputs/solution.json`
- `docs/grafo_e_rotas.png`

## Extras (CSV)
```bash
python extras/professor_adapter.py --convert_only
python extras/professor_adapter.py --metric distancia --origin "CIDADE A" --dest "CIDADE B"
```
