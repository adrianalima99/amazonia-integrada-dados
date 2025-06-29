import matplotlib.pyplot as plt
import seaborn as sns

# Aplicar tema moderno do seaborn
sns.set_theme(style="whitegrid")

# Gráficos de dispersão para investigar relações entre variáveis climáticas
# Justificativa: Responde perguntas como "A produção agrícola diminui com a queda da umidade do solo?"
def plot_dispersao(df_clima, output_path='graficos/disp_clima.png'):
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("Gráficos de Dispersão - Variáveis Climáticas", fontsize=16, fontweight='bold', y=1.05)

    # 1. Chuvas previstas x Chuvas reais
    axs[0].scatter(df_clima['chuvas_previstas_mm'], df_clima['chuvas_reais_mm'], alpha=0.7, s=60, edgecolor='k', color=sns.color_palette("viridis", 3)[0])
    axs[0].set_xlabel('Chuvas Previstas (mm)', fontsize=12)
    axs[0].set_ylabel('Chuvas Reais (mm)', fontsize=12)
    axs[0].set_title('Previstas x Reais', fontsize=13)
    axs[0].grid(True, linestyle='--', alpha=0.5)

    # 2. Chuvas previstas x Temperatura média
    axs[1].scatter(df_clima['chuvas_previstas_mm'], df_clima['temperatura_media_C'], alpha=0.7, s=60, edgecolor='k', color=sns.color_palette("viridis", 3)[1])
    axs[1].set_xlabel('Chuvas Previstas (mm)', fontsize=12)
    axs[1].set_ylabel('Temperatura Média (°C)', fontsize=12)
    axs[1].set_title('Previstas x Temperatura', fontsize=13)
    axs[1].grid(True, linestyle='--', alpha=0.5)

    # 3. Chuvas reais x Temperatura média
    axs[2].scatter(df_clima['chuvas_reais_mm'], df_clima['temperatura_media_C'], alpha=0.7, s=60, edgecolor='k', color=sns.color_palette("viridis", 3)[2])
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
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(
        corr,
        annot=True,
        cmap='YlGnBu',
        fmt=".2f",
        linewidths=0.5,
        cbar_kws={"shrink": .8},
        square=True,
        annot_kws={"size": 11}
    )
    plt.title("Matriz de Correlação entre Variáveis", fontsize=16, fontweight='bold', pad=20)
    plt.xticks(fontsize=11, rotation=45, ha='right')
    plt.yticks(fontsize=11, rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=150)
    plt.close()
