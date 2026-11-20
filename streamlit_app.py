from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =====================================
# Configuração da página
# =====================================

st.set_page_config(
    page_title="Série A — Painel Analítico",
    page_icon="⚽",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "data" / "dataset_clusters.csv"

ORDEM_POSICAO = ["Goleiro", "Defesa", "Meio-campo", "Ataque"]

NOME_CLUSTER = {
    0: "Cluster 0 — perfil mais ofensivo",
    1: "Cluster 1 — perfil mais defensivo/disciplinar",
}


# =====================================
# Carregar dados
# =====================================

def classificar_nacionalidade(valor):

    if str(valor).strip().lower() == "brazil":
        return "Brasileiro"

    return "Estrangeiro"


@st.cache_data
def carregar_dados():

    df = pd.read_csv(DATASET_PATH)

    df["grupo_nacionalidade"] = df["nacionalidade"].apply(classificar_nacionalidade)

    df["cluster_nome"] = df["cluster"].map(NOME_CLUSTER)

    return df


df = carregar_dados()


# =====================================
# Filtros (barra lateral — afetam todos os gráficos)
# =====================================

st.sidebar.header("Filtros")

temporadas_disponiveis = sorted(df["temporada"].unique())

temporadas_sel = st.sidebar.multiselect(
    "Temporada",
    options=temporadas_disponiveis,
    default=temporadas_disponiveis,
)

posicoes_disponiveis = [p for p in ORDEM_POSICAO if p in df["posicao_macro"].unique()]

posicoes_sel = st.sidebar.multiselect(
    "Posição",
    options=posicoes_disponiveis,
    default=posicoes_disponiveis,
)

clubes_disponiveis = sorted(df["clube"].unique())

clubes_sel = st.sidebar.multiselect(
    "Clube",
    options=clubes_disponiveis,
    default=clubes_disponiveis,
)

st.sidebar.caption(
    "Esses três filtros valem para todos os gráficos da página. "
    "Alguns gráficos têm um filtro adicional próprio, logo acima deles."
)

df_filtrado = df[
    df["temporada"].isin(temporadas_sel)
    & df["posicao_macro"].isin(posicoes_sel)
    & df["clube"].isin(clubes_sel)
]

if df_filtrado.empty:
    st.warning("Nenhum registro para essa combinação de filtros. Ajuste a barra lateral.")
    st.stop()


# =====================================
# Cabeçalho
# =====================================

st.title("⚽ Campeonato Brasileiro Série A — Painel Analítico")

st.caption(
    "Fonte: Transfermarkt. Jogadores da Série A, temporadas 2023–2025. "
    "981 registros na base completa; os números abaixo refletem os filtros aplicados."
)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)

col_m1.metric("Registros filtrados", len(df_filtrado))
col_m2.metric("Jogadores únicos", df_filtrado["jogador"].nunique())
col_m3.metric("Clubes", df_filtrado["clube"].nunique())
col_m4.metric("Temporadas", df_filtrado["temporada"].nunique())

st.divider()


# =====================================
# V1 — Produção ofensiva por posição (Q1)
# =====================================

st.subheader("V1 · Produção ofensiva por posição")

st.caption(
    "Q1) Quais posições apresentam maior contribuição ofensiva, medida por gols "
    "e assistências, ao longo das temporadas?"
)

v1_dados = (
    df_filtrado.groupby("posicao_macro")[["gols_por_partida", "assistencias_por_partida"]]
    .mean()
    .reindex(posicoes_sel)
    .reset_index()
    .melt(id_vars="posicao_macro", var_name="métrica", value_name="média por partida")
)

v1_dados["métrica"] = v1_dados["métrica"].map(
    {"gols_por_partida": "Gols por partida", "assistencias_por_partida": "Assistências por partida"}
)

fig_v1 = px.bar(
    v1_dados,
    x="posicao_macro",
    y="média por partida",
    color="métrica",
    barmode="group",
    title="Gols e assistências médios por partida, por posição",
    labels={"posicao_macro": "Posição"},
    color_discrete_sequence=["#1f77b4", "#ff7f0e"],
)

st.plotly_chart(fig_v1, width="stretch")


# =====================================
# V2 — Perfil disciplinar por posição (Q2)
# =====================================

st.subheader("V2 · Perfil disciplinar por posição")

st.caption(
    "Q2) Como o perfil disciplinar, medido em cartões por partida, varia entre "
    "as posições?"
)

col_v2a, col_v2b = st.columns(2)

v2_cartoes = (
    df_filtrado.groupby("posicao_macro")["cartoes_por_partida"]
    .mean()
    .reindex(posicoes_sel)
    .reset_index()
)

fig_v2a = px.bar(
    v2_cartoes,
    x="posicao_macro",
    y="cartoes_por_partida",
    title="Cartões por partida (média)",
    labels={"posicao_macro": "Posição", "cartoes_por_partida": "cartões / partida"},
    color_discrete_sequence=["#d62728"],
)

col_v2a.plotly_chart(fig_v2a, width="stretch")

v2_pontos = (
    df_filtrado.groupby("posicao_macro")["pontos_disciplinares"]
    .mean()
    .reindex(posicoes_sel)
    .reset_index()
)

fig_v2b = px.bar(
    v2_pontos,
    x="posicao_macro",
    y="pontos_disciplinares",
    title="Pontos disciplinares (média)",
    labels={"posicao_macro": "Posição", "pontos_disciplinares": "pontos disciplinares"},
    color_discrete_sequence=["#9467bd"],
)

col_v2b.plotly_chart(fig_v2b, width="stretch")


# =====================================
# V3 — Brasileiros x Estrangeiros (Q3)
# =====================================

st.subheader("V3 · Brasileiros x Estrangeiros")

st.caption(
    "Q3) Jogadores estrangeiros disputam mais partidas e apresentam maior "
    "produção ofensiva do que os brasileiros?"
)

col_v3a, col_v3b = st.columns(2)

v3_partidas = (
    df_filtrado.groupby("grupo_nacionalidade")["partidas"]
    .mean()
    .reset_index()
)

fig_v3a = px.bar(
    v3_partidas,
    x="grupo_nacionalidade",
    y="partidas",
    title="Partidas por jogador (média)",
    labels={"grupo_nacionalidade": "", "partidas": "partidas"},
    color="grupo_nacionalidade",
    color_discrete_map={"Brasileiro": "#2ca02c", "Estrangeiro": "#17becf"},
)
fig_v3a.update_layout(showlegend=False)

col_v3a.plotly_chart(fig_v3a, width="stretch")

v3_ofensivo = (
    df_filtrado.groupby("grupo_nacionalidade")[["gols_por_partida", "assistencias_por_partida"]]
    .mean()
    .reset_index()
    .melt(id_vars="grupo_nacionalidade", var_name="métrica", value_name="média por partida")
)

v3_ofensivo["métrica"] = v3_ofensivo["métrica"].map(
    {"gols_por_partida": "Gols por partida", "assistencias_por_partida": "Assistências por partida"}
)

fig_v3b = px.bar(
    v3_ofensivo,
    x="grupo_nacionalidade",
    y="média por partida",
    color="métrica",
    barmode="group",
    title="Produção ofensiva por partida (média)",
    labels={"grupo_nacionalidade": ""},
)

col_v3b.plotly_chart(fig_v3b, width="stretch")


# =====================================
# V4 — Evolução da presença de estrangeiros (Q4)
# =====================================

st.subheader("V4 · Evolução da presença de estrangeiros por temporada")

st.caption(
    "Q4) A presença de jogadores estrangeiros mudou ao longo das temporadas?"
)

v4_total = df_filtrado.groupby("temporada")["jogador"].nunique()

v4_estrangeiros = (
    df_filtrado[df_filtrado["grupo_nacionalidade"] == "Estrangeiro"]
    .groupby("temporada")["jogador"]
    .nunique()
)

v4_dados = pd.DataFrame(
    {"total_jogadores": v4_total, "estrangeiros": v4_estrangeiros}
).fillna(0)

v4_dados["percentual_estrangeiros"] = (
    v4_dados["estrangeiros"] / v4_dados["total_jogadores"] * 100
).round(2)

v4_dados = v4_dados.reset_index()

fig_v4 = px.line(
    v4_dados,
    x="temporada",
    y="percentual_estrangeiros",
    markers=True,
    title="% de jogadores estrangeiros por temporada",
    labels={"temporada": "Temporada", "percentual_estrangeiros": "% estrangeiros"},
)
fig_v4.update_xaxes(dtick=1)
fig_v4.update_yaxes(ticksuffix="%")

st.plotly_chart(fig_v4, width="stretch")


# =====================================
# V5 — Dispersão colorida por cluster (K-Means)
# =====================================

st.subheader("V5 · Perfis encontrados pelo K-Means")

st.caption(
    "Os jogadores se dividem em perfis distintos quando olhamos só para "
    "desempenho ofensivo e disciplina?"
)

opcoes_eixo = {
    "Gols por partida": "gols_por_partida",
    "Assistências por partida": "assistencias_por_partida",
    "Cartões por partida": "cartoes_por_partida",
    "Partidas": "partidas",
}

col_eixo_x, col_eixo_y = st.columns(2)

eixo_x_label = col_eixo_x.selectbox("Eixo X", options=list(opcoes_eixo.keys()), index=0)

eixo_y_label = col_eixo_y.selectbox("Eixo Y", options=list(opcoes_eixo.keys()), index=2)

fig_v5 = px.scatter(
    df_filtrado,
    x=opcoes_eixo[eixo_x_label],
    y=opcoes_eixo[eixo_y_label],
    color="cluster_nome",
    hover_data=["jogador", "posicao_macro", "clube", "temporada"],
    title=f"{eixo_x_label} x {eixo_y_label}, colorido pelo cluster",
    labels={opcoes_eixo[eixo_x_label]: eixo_x_label, opcoes_eixo[eixo_y_label]: eixo_y_label},
    color_discrete_map={
        NOME_CLUSTER[0]: "#4c78a8",
        NOME_CLUSTER[1]: "#e45756",
    },
    category_orders={"cluster_nome": [NOME_CLUSTER[0], NOME_CLUSTER[1]]},
    opacity=0.65,
)

st.plotly_chart(fig_v5, width="stretch")


# =====================================
# V6 — Ranking de clubes (contexto)
# =====================================

st.subheader("V6 · Ranking de clubes")

st.caption("Quais clubes se destacam na métrica escolhida?")

opcoes_metrica_clube = {
    "Gols por partida (média)": "gols_por_partida",
    "Assistências por partida (média)": "assistencias_por_partida",
    "Cartões por partida (média)": "cartoes_por_partida",
    "Pontos disciplinares (média)": "pontos_disciplinares",
}

metrica_label = st.selectbox("Métrica do ranking", options=list(opcoes_metrica_clube.keys()))

metrica_coluna = opcoes_metrica_clube[metrica_label]

v6_dados = (
    df_filtrado.groupby("clube")[metrica_coluna]
    .mean()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

v6_dados["rotulo"] = [
    f"{posicao}º  {clube}"
    for posicao, clube in enumerate(v6_dados["clube"], start=1)
]

v6_dados["valor_texto"] = v6_dados[metrica_coluna].map(lambda v: f"{v:.3f}")

fig_v6 = px.bar(
    v6_dados,
    x=metrica_coluna,
    y="rotulo",
    orientation="h",
    text="valor_texto",
    title=f"Top 15 clubes por {metrica_label.lower()}",
    labels={metrica_coluna: metrica_label, "rotulo": ""},
    color_discrete_sequence=["#59a14f"],
)
fig_v6.update_yaxes(autorange="reversed")
fig_v6.update_traces(textposition="outside", cliponaxis=False)
fig_v6.update_xaxes(range=[0, v6_dados[metrica_coluna].max() * 1.15])

st.plotly_chart(fig_v6, width="stretch")


# =====================================
# Dados filtrados (apoio à exploração)
# =====================================

with st.expander("Ver dados filtrados"):

    st.dataframe(df_filtrado, width="stretch")

    st.download_button(
        "Baixar CSV filtrado",
        data=df_filtrado.to_csv(index=False).encode("utf-8-sig"),
        file_name="serie_a_filtrado.csv",
        mime="text/csv",
    )