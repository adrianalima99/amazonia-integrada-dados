def estatisticas_descritivas(df):
    return df.describe()

def correlacoes(clima, socio):
    combinado = clima.merge(socio, on='data')
    return combinado.corr(numeric_only=True)
