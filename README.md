# Mineração de Dados - Campeonato Brasileiro Série A

Projeto desenvolvido para a disciplina de Mineração de Dados (Fatec).

## Objetivo

Analisar o desempenho ofensivo e o perfil disciplinar de jogadores do Campeonato Brasileiro Série A (temporadas 2023 a 2025), seguindo o processo de KDD (Knowledge Discovery in Databases):

1. **Entrega 1:** coleta dos dados por Web Scraping (Transfermarkt), ETL e preparação da base.
2. **Entrega 2:** dashboard interativo em Streamlit e agrupamento de jogadores com a técnica de aprendizado não supervisionado K-Means.

---

## Dashboard (acesso rápido)

**Link público:** [https://mineracao-dados-serie-a.streamlit.app/](https://mineracao-dados-serie-a.streamlit.app/)

Não é preciso instalar nada. Basta abrir o link no navegador.

- Se o app estiver inativo, o Streamlit Community Cloud mostra um aviso de que ele "dormiu". Clique no botão para reativá-lo e aguarde alguns segundos.
- Use a **barra lateral** para filtrar por temporada, posição e clube. Esses filtros valem para todos os gráficos.
- Os gráficos V5 (eixos) e V6 (métrica) têm seletores próprios.
- No fim da página, a seção **"Ver dados filtrados"** mostra a tabela e permite baixar o CSV.

---

## Perguntas de Pesquisa

**Q1)** Quais posições apresentam maior contribuição ofensiva, medida por gols e assistências, ao longo das temporadas?

**Q2)** Como o perfil disciplinar, medido em cartões por partida, varia entre as posições?

**Q3)** Jogadores estrangeiros disputam mais partidas e apresentam maior produção ofensiva do que os brasileiros?

**Q4)** A presença de jogadores estrangeiros mudou ao longo das temporadas?

**Q5)** Os jogadores se dividem em perfis distintos quando olhamos só para desempenho ofensivo e disciplina? (respondida pelo K-Means)

### Visualizações do dashboard

| Gráfico | Conteúdo | Pergunta |
|---|---|---|
| V1 | Gols e assistências por partida, por posição | Q1 |
| V2 | Cartões por partida e pontos disciplinares, por posição | Q2 |
| V3 | Brasileiros x estrangeiros (partidas, gols e assistências) | Q3 |
| V4 | % de jogadores estrangeiros por temporada | Q4 |
| V5 | Dispersão dos jogadores colorida pelo cluster do K-Means | Q5 |
| V6 | Ranking dos 15 principais clubes na métrica escolhida | Apoio |

---

## Fonte dos Dados

- Site: [Transfermarkt](https://www.transfermarkt.com)
- Competição: Campeonato Brasileiro Série A
- Temporadas analisadas: 2023, 2024 e 2025

---

## Estrutura do Projeto

```text
mineracao-dados-serie-a/
│
├── data/
│   ├── ofensivo.csv
│   ├── disciplinar.csv
│   ├── dataset_final.csv
│   ├── dataset_final_limpo.csv
│   ├── dataset_ml.csv
│   ├── dataset_clusters.csv
│   ├── clustering_perfil_clusters.csv
│   ├── clustering_cluster_x_posicao.csv
│   └── serie_a.db
│
├── doc/
│   ├── diagrama_pipeline.png
│   └── clustering_cotovelo_silhouette.png
│
├── scripts/
│   ├── montar_dataset.py
│   ├── limpar_dados.py
│   ├── responder_perguntas.py
│   ├── preparar_ml.py
│   └── clustering.py
│
├── src/
│   ├── coletar_disciplinar.py
│   ├── coletar_ofensivo.py
│   ├── config.py
│   ├── database.py
│   ├── parser_disciplinar.py
│   ├── parser_ofensivo.py
│   └── scraper.py
│
├── main.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## Tecnologias Utilizadas

- Python 3.13+
- Requests e BeautifulSoup4 (web scraping)
- Pandas e NumPy
- SQLite
- Scikit-learn (K-Means)
- Matplotlib
- Streamlit e Plotly (dashboard)

---

## Como executar localmente

Os arquivos de dados já estão no repositório. Para **abrir o dashboard**, não é necessário refazer o scraping nem o clustering.

### 1. Clonar o repositório

```bash
git clone https://github.com/rayannenunes/mineracao-dados-serie-a.git
```

### 2. Entrar na pasta do projeto

```bash
cd mineracao-dados-serie-a
```

### 3. Criar o ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar o ambiente virtual

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / MacOS

```bash
source venv/bin/activate
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Rodar o dashboard

Na raiz do projeto (a mesma pasta do arquivo `streamlit_app.py`):

```bash
streamlit run streamlit_app.py
```

### 7. Acessar no navegador

O Streamlit abre o navegador automaticamente. Se isso não acontecer, acesse:

```text
http://localhost:8501
```

Para encerrar, volte ao terminal e pressione `Ctrl + C`.

### Problemas comuns

- **`streamlit` não é reconhecido:** confirme que o ambiente virtual está ativado (passo 4) e que as dependências foram instaladas (passo 5).
- **Erro do NumPy mencionando `X86_V2`:** a CPU não é compatível com a versão mais nova do NumPy. Instale versões anteriores: `pip install numpy==2.2.6 pandas==2.2.3`.
- **Porta 8501 ocupada:** use outra porta, por exemplo `streamlit run streamlit_app.py --server.port 8502`.

---

## Reexecutar as etapas do projeto (opcional)

### Pipeline completo (coleta, integração, limpeza e banco)

```bash
python main.py
```

O processo executa automaticamente:

1. Coleta dos dados ofensivos
2. Coleta dos dados disciplinares
3. Integração das bases
4. Limpeza dos dados
5. Atualização do banco SQLite
6. Resposta das perguntas de pesquisa

A coleta acessa o Transfermarkt e exige conexão com a internet. Ela sobrescreve os arquivos de `data/`.

### Aprendizado de máquina (K-Means)

Execute na raiz do projeto, nesta ordem:

```bash
python scripts/preparar_ml.py
python scripts/clustering.py
```

- `preparar_ml.py` cria `posicao_macro`, as taxas por partida e as variáveis padronizadas (`data/dataset_ml.csv`).
- `clustering.py` testa k de 2 a 8, escolhe o k pelo maior silhouette, gera a coluna `cluster` (`data/dataset_clusters.csv`), as tabelas de perfil e o gráfico `doc/clustering_cotovelo_silhouette.png`.

O dashboard lê o arquivo `data/dataset_clusters.csv`.

---

## Pipeline do Projeto

```text
                  TRANSFERMARKT
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
  Coleta Ofensiva                 Coleta Disciplinar
(coletar_ofensivo.py)         (coletar_disciplinar.py)
        │                                 │
        ▼                                 ▼
    ofensivo.csv                  disciplinar.csv
        │                                 │
        └────────────────┬────────────────┘
                         │
                         ▼
               montar_dataset.py
                         │
                         ▼
                 dataset_final.csv
                         │
                         ▼
                  limpar_dados.py
                         │
                         ▼
             dataset_final_limpo.csv
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
        database.py              preparar_ml.py
            │                         │
            ▼                         ▼
        serie_a.db               dataset_ml.csv
                                      │
                                      ▼
                               clustering.py (K-Means)
                                      │
                                      ▼
                             dataset_clusters.csv
                                      │
                                      ▼
                             streamlit_app.py (dashboard)
```

---

## Bases Geradas

### Base Ofensiva (`ofensivo.csv`)

1.189 registros. Contém: jogador, posição, clube, nacionalidade, partidas, gols, assistências, participação em gols, temporada e URL de origem.

### Base Disciplinar (`disciplinar.csv`)

1.554 registros. Contém: jogador, posição, clube, nacionalidade, partidas, suspensões por amarelo, cartões amarelos, segundo amarelo, cartões vermelhos, expulsões, pontos disciplinares, cartões por partida, temporada e URL de origem.

### Base Integrada (`dataset_final.csv`)

Resultado da integração das bases ofensiva e disciplinar por **junção interna** (chaves: jogador, clube e temporada). Só permanecem os registros que existem nas duas bases, por isso o total (981) é menor que o de cada base de origem. Registros sem correspondência são descartados, por exemplo jogadores que passaram por mais de um clube na mesma temporada e aparecem como `MULTIPLOS_CLUBES` na base ofensiva.

### Base Final Limpa (`dataset_final_limpo.csv`)

Resultado da limpeza. Contém os atributos:

```text
jogador
posicao
clube
nacionalidade
temporada

partidas

gols
assistencias
participacao_gols

suspensoes_amarelo
cartoes_amarelos
segundo_amarelo
cartoes_vermelhos
expulsoes
pontos_disciplinares
cartoes_por_partida
```

### Bases do aprendizado de máquina

- `dataset_ml.csv`: base final com `posicao_macro` (Goleiro, Defesa, Meio-campo, Ataque), taxas por partida e variáveis padronizadas (colunas `_z`).
- `dataset_clusters.csv`: `dataset_ml.csv` com a coluna `cluster` (resultado do K-Means).
- `clustering_perfil_clusters.csv` e `clustering_cluster_x_posicao.csv`: perfil médio de cada cluster e cruzamento com a posição.

---

## Banco de Dados

O projeto também gera:

```text
data/serie_a.db
```

Tabela:

```text
dataset_final_limpo
```

---

## Limpeza dos Dados

As seguintes etapas são aplicadas:

- Conversão de atributos numéricos
- Tratamento de valores ausentes disciplinares (preenchidos com 0)
- Remoção de registros duplicados (nenhum foi encontrado)
- Identificação de valores nulos
- Estatísticas descritivas
- Identificação de valores extremos

---

## Técnica de Aprendizado de Máquina: K-Means

- **Tipo:** aprendizado não supervisionado (agrupamento).
- **Variáveis:** partidas, gols por partida, assistências por partida e cartões por partida, padronizadas com `StandardScaler`.
- **Parâmetros:** `n_init=10`, `random_state=42`, k testado de 2 a 8.
- **Escolha de k:** maior silhouette (k = 2, silhouette de 0,294). O silhouette indica separação fraca entre os grupos, então os perfis devem ser lidos como tendências.
- **Resultado:** Cluster 0 (232 registros), perfil mais ofensivo; Cluster 1 (749 registros), perfil de baixa produção ofensiva e mais cartões.

---

## Resultados da Preparação

Base final:

- 981 registros
- 16 atributos
- 585 jogadores únicos
- 27 clubes
- 27 nacionalidades
- 3 temporadas (2023–2025)

---

## Autores

### Rayanne Nunes

GitHub:

[https://github.com/RayanneNunes](https://github.com/RayanneNunes)

### João Paulo Mussarelli Carossine

GitHub:

[https://github.com/joaopcarossine](https://github.com/joaopcarossine)