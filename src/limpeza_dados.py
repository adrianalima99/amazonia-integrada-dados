import pandas as pd

def carregar_bases():
    clima = pd.read_csv('data/base_climatica.csv')
    socio = pd.read_csv('data/base_socioeconomica.csv')
    return clima, socio

def limpar_bases(clima, socio):
    clima['data'] = pd.to_datetime(clima['data'], errors='coerce')
    socio['data'] = pd.to_datetime(socio['data'], errors='coerce')

    clima.drop_duplicates(inplace=True)
    socio.drop_duplicates(inplace=True)

    clima['variacao_climatica'] = clima['variacao_climatica'].str.strip().str.lower().replace({'nao': 'não'})
    socio['acesso_agua_potavel'] = socio['acesso_agua_potavel'].str.strip().str.lower().replace({'nao': 'não'})

    clima = clima[clima['chuvas_reais_mm'] < 300].copy()

    clima.ffill(inplace=True)
    socio.ffill(inplace=True)

    return clima, socio
