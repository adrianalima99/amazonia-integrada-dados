import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Aplicar tema moderno do seaborn
sns.set_theme(style="whitegrid")

# Gráficos de dispersão para investigar relações entre variáveis climáticas
# Justificativa: Responde perguntas como "A produção agrícola diminui com a queda da umidade do solo?"
def plot_dispersao(df_clima, output_path='graficos/disp_clima.png'):
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("Gráficos de Dispersão - Variáveis Climáticas", fontsize=16, fontweight='bold', y=1.05)

    # 1. Chuvas previstas x Chuvas reais
    x = df_clima['chuvas_previstas_mm'].dropna()
    y = df_clima['chuvas_reais_mm'].dropna()
    
    # Garantir que x e y tenham o mesmo tamanho
    min_len = min(len(x), len(y))
    x = x.iloc[:min_len]
    y = y.iloc[:min_len]
    
    axs[0].scatter(x, y, alpha=0.7, s=60, edgecolor='k', color=sns.color_palette("viridis", 3)[0])
    
    # Adicionar linha de tendência
    if len(x) > 1:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        line = slope * x + intercept
        axs[0].plot(x, line, color='red', linestyle='--', alpha=0.8, linewidth=2)
        axs[0].text(0.05, 0.95, f'R² = {r_value**2:.3f}', transform=axs[0].transAxes, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    axs[0].set_xlabel('Chuvas Previstas (mm)', fontsize=12)
    axs[0].set_ylabel('Chuvas Reais (mm)', fontsize=12)
    axs[0].set_title('Previstas x Reais', fontsize=13)
    axs[0].grid(True, linestyle='--', alpha=0.5)

    # 2. Chuvas previstas x Temperatura média
    x = df_clima['chuvas_previstas_mm'].dropna()
    y = df_clima['temperatura_media_C'].dropna()
    
    min_len = min(len(x), len(y))
    x = x.iloc[:min_len]
    y = y.iloc[:min_len]
    
    axs[1].scatter(x, y, alpha=0.7, s=60, edgecolor='k', color=sns.color_palette("viridis", 3)[1])
    
    # Adicionar linha de tendência
    if len(x) > 1:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        line = slope * x + intercept
        axs[1].plot(x, line, color='red', linestyle='--', alpha=0.8, linewidth=2)
        axs[1].text(0.05, 0.95, f'R² = {r_value**2:.3f}', transform=axs[1].transAxes, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    axs[1].set_xlabel('Chuvas Previstas (mm)', fontsize=12)
    axs[1].set_ylabel('Temperatura Média (°C)', fontsize=12)
    axs[1].set_title('Previstas x Temperatura', fontsize=13)
    axs[1].grid(True, linestyle='--', alpha=0.5)

    # 3. Chuvas reais x Temperatura média
    x = df_clima['chuvas_reais_mm'].dropna()
    y = df_clima['temperatura_media_C'].dropna()
    
    min_len = min(len(x), len(y))
    x = x.iloc[:min_len]
    y = y.iloc[:min_len]
    
    axs[2].scatter(x, y, alpha=0.7, s=60, edgecolor='k', color=sns.color_palette("viridis", 3)[2])
    
    # Adicionar linha de tendência
    if len(x) > 1:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        line = slope * x + intercept
        axs[2].plot(x, line, color='red', linestyle='--', alpha=0.8, linewidth=2)
        axs[2].text(0.05, 0.95, f'R² = {r_value**2:.3f}', transform=axs[2].transAxes, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    axs[2].set_xlabel('Chuvas Reais (mm)', fontsize=12)
    axs[2].set_ylabel('Temperatura Média (°C)', fontsize=12)
    axs[2].set_title('Reais x Temperatura', fontsize=13)
    axs[2].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(output_path, bbox_inches='tight', dpi=150)
    plt.close()

# Heatmap de correlação para revelar padrões e clusters entre variáveis
# Justificativa: Ajuda a responder perguntas sobre relações entre clima, produção e saúde

def heatmap_correlacao(df, output_path='graficos/heatmap.png'):
    corr = df.corr(numeric_only=True)
    
    # Criar máscara para destacar correlações fortes
    mask = np.abs(corr) > 0.8
    
    plt.figure(figsize=(12, 10))
    
    # Usar paleta de cores mais contrastante
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    
    ax = sns.heatmap(
        corr,
        annot=True,
        cmap=cmap,
        fmt=".2f",
        linewidths=0.5,
        cbar_kws={"shrink": .8},
        square=True,
        annot_kws={"size": 10},
        mask=~mask,  # Destacar apenas correlações fortes
        center=0,
        vmin=-1, vmax=1
    )
    
    # Adicionar título explicativo
    plt.title("Relação entre Variáveis Climáticas e Socioeconômicas\n(Correlações > 0.8 destacadas)", 
              fontsize=16, fontweight='bold', pad=20)
    
    plt.xticks(fontsize=11, rotation=45, ha='right')
    plt.yticks(fontsize=11, rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=150)
    plt.close()

def plot_correlacao_producao_doencas(df, output_path='graficos/corr_producao_doencas.png'):
    """
    Gráfico específico para analisar a correlação entre produção e doenças
    """
    plt.figure(figsize=(10, 6))
    
    x = df['volume_producao_tons'].dropna()
    y = df['incidencia_doencas'].dropna()
    
    min_len = min(len(x), len(y))
    x = x.iloc[:min_len]
    y = y.iloc[:min_len]
    
    plt.scatter(x, y, alpha=0.7, s=80, edgecolor='k', color='steelblue')
    
    # Adicionar linha de tendência
    if len(x) > 1:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        line = slope * x + intercept
        plt.plot(x, line, color='red', linestyle='--', alpha=0.8, linewidth=2)
        
        # Adicionar estatísticas
        plt.text(0.05, 0.95, f'Correlação: {r_value:.3f}\nP-valor: {p_value:.3f}', 
                transform=plt.gca().transAxes, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    plt.xlabel('Volume de Produção (tons)', fontsize=12)
    plt.ylabel('Incidência de Doenças', fontsize=12)
    plt.title('Correlação: Produção x Doenças\n(Análise de Possíveis Vieses)', fontsize=14, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=150)
    plt.close()
