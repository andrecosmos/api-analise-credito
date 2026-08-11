import pandas as pd
import numpy as np

# Define uma semente para gerar sempre os mesmos dados
np.random.seed(42)

# Gera os dados simulados corrigindo a sintaxe do arredondamento
dados = {
    'ID_Cliente': range(1001, 1051),
    'Renda_Mensal': np.round(np.random.uniform(2500, 18000, size=50), 2),
    'Valor_Emprestimo': np.round(np.random.uniform(5000, 80000, size=50), 2),
    'Parcelas': np.random.choice([12, 24, 36, 48, 60], size=50),
    'Historico_Inadimplencia': np.random.choice([0, 1], size=50, p=[0.8, 0.2])
}

df = pd.DataFrame(dados)

# Salva a planilha de testes
df.to_excel('clientes_teste.xlsx', index=False)
print("Planilha 'clientes_teste.xlsx' gerada com sucesso!")
