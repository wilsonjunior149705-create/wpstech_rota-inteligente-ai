# ============================
# 📥 0. Criar dataset na memória
# ============================
import pandas as pd
import random

# ... (código para gerar o DataFrame df) ...

print("✅ Dataset criado na memória com sucesso!")
print("Total de registros:", len(df))
print("\nExemplo de dados:\n", df.head())

# Adicione esta linha para salvar o arquivo
df.to_csv("rede_transito_brasil.csv", index=False)
print("✅ Arquivo 'rede_transito_brasil.csv' salvo com sucesso!")