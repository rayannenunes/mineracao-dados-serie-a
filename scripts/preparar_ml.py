from pathlib import Path

import pandas as pd
from sklearn.preprocessing import StandardScaler


# =====================================
# Caminhos
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATASET_PATH = DATA_DIR / "dataset_final_limpo.csv"

DATASET_ML_PATH = DATA_DIR / "dataset_ml.csv"


# =====================================
# Posição macro
# =====================================

MAPA_POSICAO_MACRO = {
    "Goalkeeper": "Goleiro",
    "Centre-Back": "Defesa",
    "Right-Back": "Defesa",
    "Left-Back": "Defesa",
    "Defensive Midfield": "Meio-campo",
    "Central Midfield": "Meio-campo",
    "Attacking Midfield": "Meio-campo",
    "Right Midfield": "Meio-campo",
    "Centre-Forward": "Ataque",
    "Second Striker": "Ataque",
    "Right Winger": "Ataque",
    "Left Winger": "Ataque",
}


def mapear_posicao_macro(posicao):
    return MAPA_POSICAO_MACRO.get(posicao, "Outra")


# =====================================
# Features do clustering
# =====================================

FEATURES_CLUSTERING = [
    "partidas",
    "gols_por_partida",
    "assistencias_por_partida",
    "cartoes_por_partida",
]


# =====================================
# Main
# =====================================

def main():

    print("=" * 80)
    print("PREPARAÇÃO PARA O CLUSTERING (K-MEANS)")
    print("=" * 80)

    df = pd.read_csv(DATASET_PATH)

    print(f"\nRegistros carregados: {len(df)}")

    # =====================================
    # Posição macro
    # =====================================

    df["posicao_macro"] = df["posicao"].apply(mapear_posicao_macro)

    print("\nRegistros por posição macro:")
    print(df["posicao_macro"].value_counts())

    # =====================================
    # Taxas por partida
    # =====================================

    df["gols_por_partida"] = (df["gols"] / df["partidas"]).round(3)

    df["assistencias_por_partida"] = (
        df["assistencias"] / df["partidas"]
    ).round(3)

    # =====================================
    # Estatísticas descritivas das features do clustering
    # =====================================

    print("\n" + "=" * 80)
    print("ESTATÍSTICAS DESCRITIVAS (features do clustering, antes de padronizar)")
    print("=" * 80)

    print(df[FEATURES_CLUSTERING].describe().round(3))

    # =====================================
    # Padronização (StandardScaler)
    # =====================================
   
    scaler = StandardScaler()

    colunas_padronizadas = [f"{coluna}_z" for coluna in FEATURES_CLUSTERING]

    df[colunas_padronizadas] = scaler.fit_transform(df[FEATURES_CLUSTERING])

    print("\n" + "=" * 80)
    print("ESTATÍSTICAS DAS FEATURES PADRONIZADAS (média ~0, desvio ~1)")
    print("=" * 80)

    print(df[colunas_padronizadas].describe().round(3))

    # =====================================
    # Salvar
    # =====================================

    df.to_csv(DATASET_ML_PATH, index=False, encoding="utf-8-sig")

    print(f"\nBase para o clustering salva em:\n{DATASET_ML_PATH}")

    print(f"\nColunas adicionadas: posicao_macro, {', '.join(FEATURES_CLUSTERING[1:])}, "
          f"{', '.join(colunas_padronizadas)}")

    print(
        "\nPróximo passo (Fase 2): rodar o K-Means sobre as colunas "
        f"{colunas_padronizadas}."
    )


if __name__ == "__main__":
    main()