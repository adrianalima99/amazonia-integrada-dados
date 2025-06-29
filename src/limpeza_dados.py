import pandas as pd

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

    # Remove outliers de chuvas reais (acima de 300 mm)
    # Justificativa: Valores acima desse limite são improváveis para a região e podem ser erro de digitação
    clima = clima[clima['chuvas_reais_mm'] < 300].copy()

    # Preenche valores ausentes com forward fill
    # Justificativa: Mantém continuidade temporal, importante para séries diárias
    clima.ffill(inplace=True)
    socio.ffill(inplace=True)

    return clima, socio
