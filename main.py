import os
from src.limpeza_dados import carregar_bases, limpar_bases, normalizar_dados
from src.analise_exploratoria import (
    estatisticas_descritivas, 
    correlacoes, 
    verificar_duplicatas_e_outliers,
    analisar_correlacao_producao_doencas,
    normalizar_e_analisar
)
from src.visualizacoes import plot_dispersao, heatmap_correlacao, plot_correlacao_producao_doencas

# Garantir que a pasta de gráficos exista
os.makedirs("graficos", exist_ok=True)

print("=== ANÁLISE AMAZÔNIA INTEGRADA - DADOS MELHORADOS ===\n")

# Carregar e limpar os dados
print("1. Carregando e limpando dados...")
clima, socio = carregar_bases()
clima_original, socio_original = clima.copy(), socio.copy()

# Verificar duplicatas e outliers ANTES da limpeza
verificar_duplicatas_e_outliers(clima_original, socio_original)

# Aplicar limpeza
clima, socio = limpar_bases(clima, socio)

print(f"\n2. Dados após limpeza:")
print(f"   - Registros climáticos: {len(clima)} (era {len(clima_original)})")
print(f"   - Registros socioeconômicos: {len(socio)} (era {len(socio_original)})")

# Estatísticas descritivas
print("\n3. Estatísticas Descritivas: Dados Climáticos")
print(estatisticas_descritivas(clima), end="\n\n")

print("4. Estatísticas Descritivas: Dados Socioeconômicos")
print(estatisticas_descritivas(socio), end="\n\n")

# Análise de correlação específica
df_merged = clima.merge(socio, on='data')
analisar_correlacao_producao_doencas(df_merged)

# Análise com dados normalizados
corr_norm = normalizar_e_analisar(df_merged)

# Correlação geral
print("\n5. Matriz de Correlação (Dados Limpos)")
print(correlacoes(clima, socio), end="\n\n")

# Gerar gráficos melhorados
print("6. Gerando gráficos melhorados...")
plot_dispersao(clima)
heatmap_correlacao(df_merged)
plot_correlacao_producao_doencas(df_merged)

print("\n✅ Análise concluída!")
print("📊 Gráficos salvos em /graficos:")
print("   - disp_clima.png (com linhas de tendência)")
print("   - heatmap.png (correlações destacadas)")
print("   - corr_producao_doencas.png (análise específica)")
print("\n💡 Principais melhorias implementadas:")
print("   - Remoção de outliers extremos")
print("   - Verificação de duplicatas")
print("   - Análise com dados normalizados")
print("   - Gráficos com linhas de tendência")
print("   - Heatmap com correlações destacadas")
