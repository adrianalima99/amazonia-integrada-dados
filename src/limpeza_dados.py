import pandas as pd
import numpy as np

# Carrega as bases de dados climática e socioeconômica
# Justificativa: Separar carregamento facilita reuso e modularidade

def carregar_bases():
    clima = pd.read_csv('data/base_climatica.csv')
    socio = pd.read_csv('data/base_socioeconomica.csv')
    return clima, socio

# Limpeza e padronização das bases
# Justificativa: Garante consistência, remove duplicatas e trata outliers/contexto local

def limpar_bases(clima, socio):
    # Padroniza datas para formato único
    clima['data'] = pd.to_datetime(clima['data'], errors='coerce')
    socio['data'] = pd.to_datetime(socio['data'], errors='coerce')

    # Remove duplicatas
    clima.drop_duplicates(inplace=True)
    socio.drop_duplicates(inplace=True)

    # Padroniza termos categóricos (ex: "nao" para "não")
    clima['variacao_climatica'] = clima['variacao_climatica'].str.strip().str.lower().replace({'nao': 'não'})
    socio['acesso_agua_potavel'] = socio['acesso_agua_potavel'].str.strip().str.lower().replace({'nao': 'não'})

    # Remove outliers extremos de chuvas reais (acima de 300 mm)
    # Justificativa: Valores acima desse limite são improváveis para a região e podem ser erro de digitação
    clima = clima[clima['chuvas_reais_mm'] < 300].copy()
    
    # Remove outliers extremos de produção (acima de 100 tons) e doenças (acima de 50)
    # Justificativa: Valores extremos como 1000 tons e 200 doenças são claramente erros de digitação
    socio = socio[socio['volume_producao_tons'] < 100].copy()
    socio = socio[socio['incidencia_doencas'] < 50].copy()
    
    # Remove valores negativos que não fazem sentido
    clima = clima[clima['chuvas_reais_mm'] >= 0].copy()
    socio = socio[socio['volume_producao_tons'] >= 0].copy()
    socio = socio[socio['incidencia_doencas'] >= 0].copy()

    # Preenche valores ausentes com forward fill
    # Justificativa: Mantém continuidade temporal, importante para séries diárias
    clima.ffill(inplace=True)
    socio.ffill(inplace=True)

    return clima, socio

def normalizar_dados(df):
    """
    Normaliza dados numéricos para evitar distorções em correlações
    devido a escalas muito diferentes
    """
    df_norm = df.copy()
    
    # Identifica colunas numéricas
    colunas_numericas = df_norm.select_dtypes(include=[np.number]).columns
    
    # Aplica normalização z-score
    for col in colunas_numericas:
        if df_norm[col].std() > 0:  # Evita divisão por zero
            df_norm[col] = (df_norm[col] - df_norm[col].mean()) / df_norm[col].std()
    
    return df_norm
