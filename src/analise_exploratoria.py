import pandas as pd
import numpy as np
from scipy import stats

def estatisticas_descritivas(df):
    return df.describe()

def correlacoes(clima, socio):
    combinado = clima.merge(socio, on='data')
    return combinado.corr(numeric_only=True)

def verificar_duplicatas_e_outliers(df_clima, df_socio):
    """
    Verifica duplicatas e outliers que podem causar correlações artificiais
    """
    print("=== VERIFICAÇÃO DE DUPLICATAS E OUTLIERS ===")
    
    # Verificar duplicatas
    duplicatas_clima = df_clima.duplicated().sum()
    duplicatas_socio = df_socio.duplicated().sum()
    
    print(f"Duplicatas em dados climáticos: {duplicatas_clima}")
    print(f"Duplicatas em dados socioeconômicos: {duplicatas_socio}")
    
    # Verificar outliers extremos
    print("\n=== OUTLIERS EXTREMOS IDENTIFICADOS ===")
    
    # Dados climáticos
    outliers_chuvas = df_clima[df_clima['chuvas_reais_mm'] > 300]
    if not outliers_chuvas.empty:
        print(f"Chuvas reais > 300mm: {len(outliers_chuvas)} registros")
        print(outliers_chuvas[['data', 'chuvas_reais_mm']].head())
    
    # Dados socioeconômicos
    outliers_producao = df_socio[df_socio['volume_producao_tons'] > 100]
    if not outliers_producao.empty:
        print(f"\nProdução > 100 tons: {len(outliers_producao)} registros")
        print(outliers_producao[['data', 'volume_producao_tons']].head())
    
    outliers_doencas = df_socio[df_socio['incidencia_doencas'] > 50]
    if not outliers_doencas.empty:
        print(f"\nDoenças > 50: {len(outliers_doencas)} registros")
        print(outliers_doencas[['data', 'incidencia_doencas']].head())

def analisar_correlacao_producao_doencas(df):
    """
    Análise específica da correlação entre produção e doenças
    """
    print("\n=== ANÁLISE CORRELAÇÃO PRODUÇÃO x DOENÇAS ===")
    
    # Dados limpos
    x = df['volume_producao_tons'].dropna()
    y = df['incidencia_doencas'].dropna()
    
    min_len = min(len(x), len(y))
    x = x.iloc[:min_len]
    y = y.iloc[:min_len]
    
    if len(x) > 1:
        # Correlação de Pearson
        corr_pearson, p_value = stats.pearsonr(x, y)
        
        # Correlação de Spearman (menos sensível a outliers)
        corr_spearman, p_value_spearman = stats.spearmanr(x, y)
        
        print(f"Correlação de Pearson: {corr_pearson:.3f} (p-valor: {p_value:.3f})")
        print(f"Correlação de Spearman: {corr_spearman:.3f} (p-valor: {p_value_spearman:.3f})")
        
        # Verificar se a correlação é estatisticamente significativa
        if p_value < 0.05:
            print("✓ Correlação estatisticamente significativa (p < 0.05)")
        else:
            print("✗ Correlação não estatisticamente significativa (p >= 0.05)")
        
        # Comparar correlações
        if abs(corr_pearson - corr_spearman) > 0.1:
            print("⚠️ Diferença grande entre Pearson e Spearman sugere influência de outliers")
        else:
            print("✓ Correlações consistentes entre métodos")
    
    return corr_pearson, corr_spearman

def normalizar_e_analisar(df):
    """
    Normaliza dados e analisa correlações para evitar distorções por escalas diferentes
    """
    print("\n=== ANÁLISE COM DADOS NORMALIZADOS ===")
    
    # Selecionar apenas colunas numéricas
    df_numeric = df.select_dtypes(include=[np.number])
    
    # Normalizar dados
    df_norm = (df_numeric - df_numeric.mean()) / df_numeric.std()
    
    # Calcular correlações normalizadas
    corr_norm = df_norm.corr()
    
    print("Correlações com dados normalizados:")
    print(corr_norm.round(3))
    
    return corr_norm
