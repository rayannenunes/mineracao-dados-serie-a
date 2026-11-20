from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# =====================================
# Caminhos
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DOC_DIR = BASE_DIR / "doc"

DATASET_ML_PATH = DATA_DIR / "dataset_ml.csv"

DATASET_CLUSTERS_PATH = DATA_DIR / "dataset_clusters.csv"

PERFIL_CLUSTERS_PATH = DATA_DIR / "clustering_perfil_clusters.csv"

CLUSTER_X_POSICAO_PATH = DATA_DIR / "clustering_cluster_x_posicao.csv"

GRAFICO_COTOVELO_SILHOUETTE_PATH = DOC_DIR / "clustering_cotovelo_silhouette.png"


# =====================================
# Configuração
# =====================================
# Colunas padronizadas geradas na Fase 1 (scripts/preparar_ml.py).

FEATURES_Z = [
    "partidas_z",
    "gols_por_partida_z",
    "assistencias_por_partida_z",
    "cartoes_por_partida_z",
]

# Colunas na escala original, usadas só para interpretar o perfil de
# cada grupo (o K-Means roda sobre as colunas padronizadas acima).

FEATURES_ORIGINAIS = [
    "partidas",
    "gols_por_partida",
    "assistencias_por_partida",
    "cartoes_por_partida",
]

K_MIN = 2

K_MAX = 8

RANDOM_STATE = 42


# =====================================
# Cotovelo (inertia) e silhouette para k = 2..8
# =====================================

def calcular_inertia_e_silhouette(X):

    valores_k = list(range(K_MIN, K_MAX + 1))

    inertias = []

    silhouettes = []

    for k in valores_k:

        modelo = KMeans(n_clusters=k, n_init=10, random_state=RANDOM_STATE)

        labels = modelo.fit_predict(X)

        inertias.append(modelo.inertia_)

        silhouettes.append(silhouette_score(X, labels))

    return valores_k, inertias, silhouettes


def plotar_cotovelo_e_silhouette(valores_k, inertias, silhouettes):

    DOC_DIR.mkdir(exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    ax1.plot(valores_k, inertias, marker="o")
    ax1.set_title("Método do cotovelo")
    ax1.set_xlabel("número de grupos (k)")
    ax1.set_ylabel("inertia")
    ax1.grid(alpha=0.3)

    ax2.plot(valores_k, silhouettes, marker="o", color="darkorange")
    ax2.set_title("Silhouette médio por k")
    ax2.set_xlabel("número de grupos (k)")
    ax2.set_ylabel("silhouette score")
    ax2.grid(alpha=0.3)

    fig.tight_layout()

    fig.savefig(GRAFICO_COTOVELO_SILHOUETTE_PATH, dpi=150)

    plt.close(fig)


# =====================================
# Main
# =====================================

def main():

    print("=" * 80)
    print("CLUSTERING (K-MEANS)")
    print("=" * 80)

    df = pd.read_csv(DATASET_ML_PATH)

    print(f"\nRegistros carregados: {len(df)}")

    X = df[FEATURES_Z]

    # =====================================
    # Cotovelo e silhouette
    # =====================================

    valores_k, inertias, silhouettes = calcular_inertia_e_silhouette(X)

    print("\n" + "=" * 80)
    print("INERTIA E SILHOUETTE POR K")
    print("=" * 80)

    resumo_k = pd.DataFrame(
        {
            "k": valores_k,
            "inertia": [round(v, 1) for v in inertias],
            "silhouette": [round(v, 3) for v in silhouettes],
        }
    )

    print(resumo_k.to_string(index=False))

    plotar_cotovelo_e_silhouette(valores_k, inertias, silhouettes)

    print(f"\nGráfico salvo em:\n{GRAFICO_COTOVELO_SILHOUETTE_PATH}")

    # =====================================
    # Escolha de k
    # =====================================
    # Critério: maior silhouette entre os valores de k testados. Em caso de
    # empate técnico (diferença pequena), o cotovelo do gráfico desempata.
 
    k_escolhido = valores_k[silhouettes.index(max(silhouettes))]

    print(f"\nk escolhido pelo maior silhouette: {k_escolhido}")

    # =====================================
    # Modelo final
    # =====================================

    modelo_final = KMeans(
        n_clusters=k_escolhido,
        n_init=10,
        random_state=RANDOM_STATE,
    )

    df["cluster"] = modelo_final.fit_predict(X)

    silhouette_final = silhouette_score(X, df["cluster"])

    print(f"Silhouette do modelo final (k={k_escolhido}): {silhouette_final:.3f}")

    # =====================================
    # Perfil de cada cluster
    # =====================================

    print("\n" + "=" * 80)
    print("PERFIL DE CADA CLUSTER (médias na escala original)")
    print("=" * 80)

    perfil = (
        df.groupby("cluster")[FEATURES_ORIGINAIS]
        .mean()
        .round(3)
    )

    perfil["qtd_jogadores"] = df.groupby("cluster").size()

    print(perfil)

    perfil.to_csv(PERFIL_CLUSTERS_PATH, encoding="utf-8-sig")

    print(f"\nPerfil salvo em:\n{PERFIL_CLUSTERS_PATH}")

    # =====================================
    # Cluster x posição macro
    # =====================================

    print("\n" + "=" * 80)
    print("CLUSTER x POSIÇÃO MACRO (% de cada cluster em cada posição)")
    print("=" * 80)

    cluster_x_posicao = pd.crosstab(
        df["cluster"],
        df["posicao_macro"],
        normalize="index",
    ).round(3) * 100

    print(cluster_x_posicao)

    cluster_x_posicao.to_csv(CLUSTER_X_POSICAO_PATH, encoding="utf-8-sig")

    print(f"\nCruzamento salvo em:\n{CLUSTER_X_POSICAO_PATH}")

    # =====================================
    # Cluster x temporada
    # =====================================

    print("\n" + "=" * 80)
    print("CLUSTER x TEMPORADA (quantidade de jogadores)")
    print("=" * 80)

    print(pd.crosstab(df["cluster"], df["temporada"]))

    # =====================================
    # Salvar dataset com o cluster
    # =====================================

    df.to_csv(DATASET_CLUSTERS_PATH, index=False, encoding="utf-8-sig")

    print(f"\nBase com os clusters salva em:\n{DATASET_CLUSTERS_PATH}")

    print("\nClustering concluído com sucesso.")


if __name__ == "__main__":
    main()