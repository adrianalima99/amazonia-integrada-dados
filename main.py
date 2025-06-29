import os
from src.limpeza_dados import carregar_bases, limpar_bases
from src.analise_exploratoria import estatisticas_descritivas, correlacoes
from src.visualizacoes import plot_dispersao, heatmap_correlacao

# Garantir que a pasta de gráficos exista
os.makedirs("graficos", exist_ok=True)

# Carregar e limpar os dados
clima, socio = carregar_bases()
clima, socio = limpar_bases(clima, socio)

# Estatísticas descritivas
print("=== Estatísticas Descritivas: Dados Climáticos ===")
print(estatisticas_descritivas(clima), end="\n\n")

print("=== Estatísticas Descritivas: Dados Socioeconômicos ===")
print(estatisticas_descritivas(socio), end="\n\n")

# Correlação
df_merged = clima.merge(socio, on='data')
print("=== Correlação ===")
print(correlacoes(clima, socio), end="\n\n")

# Gerar gráficos
plot_dispersao(clima)
heatmap_correlacao(df_merged)

print("Gráficos salvos em /graficos")
