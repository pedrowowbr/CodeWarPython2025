import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from code_war.database import Settings
import plotly.express as px

# Configurações da página
st.set_page_config(page_title="Dashboard TMDb", layout="wide")
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w200"
BACKDROP_BASE_URL = "https://image.tmdb.org/t/p/w300"

# Barra lateral de navegação
st.sidebar.title("🎬 Navegação")
pagina = st.sidebar.radio("Ir para:", ["🏠 Home", "📊 Gráficos"])

# Conexão com o banco SQLite
engine = create_engine(Settings().DATABASE_URL, connect_args={"check_same_thread": False})
with engine.connect() as conn:
    df = pd.read_sql("SELECT * FROM filmes", conn)

df = df[df["adulto"] == 0]

# Conversões necessárias
df["media_votos"] = pd.to_numeric(df["media_votos"], errors="coerce")
df["popularidade"] = pd.to_numeric(df["popularidade"], errors="coerce")
df["quantidade_votos"] = pd.to_numeric(df["quantidade_votos"], errors="coerce")
df["data_lancamento"] = pd.to_datetime(df["data_lancamento"], errors="coerce")
df["ano_lancamento"] = df["data_lancamento"].dt.year

# ---------------------- FILTROS ----------------------
st.sidebar.header("🔎 Filtros")

busca_nome = st.sidebar.text_input("🔍 Buscar por nome do filme", "")
idiomas = sorted(df["idioma_original"].dropna().unique().tolist())
idioma = st.sidebar.selectbox("🗣️ Idioma Original", options=["Todos"] + idiomas)

anos = sorted(df["ano_lancamento"].dropna().unique().astype(int))
ano_min, ano_max = st.sidebar.select_slider("📅 Intervalo de Anos", options=anos, value=(min(anos), max(anos)))
nota_min = st.sidebar.slider("⭐ Nota Média Mínima", 0.0, 10.0, 5.0, 0.5)

todos_generos = sorted(set(g for sublist in df["generos"].dropna().str.split(",") for g in sublist))
generos_selecionados = st.sidebar.multiselect("🎭 Gêneros", options=todos_generos)

# Aplica filtros
if busca_nome:
    df = df[df["titulo"].str.contains(busca_nome, case=False, na=False)]
if idioma != "Todos":
    df = df[df["idioma_original"] == idioma]
df = df[(df["ano_lancamento"] >= ano_min) & (df["ano_lancamento"] <= ano_max)]
df = df[df["media_votos"] >= nota_min]
if generos_selecionados:
    df = df[df["generos"].apply(lambda x: any(g in x.split(",") for g in generos_selecionados) if pd.notnull(x) else False)]

# ---------------------- HOME: GALERIA ----------------------
if pagina == "🏠 Home":
    st.title("🎞️ Galeria de Filmes")
    st.subheader(f"{len(df)} encontrados")

    if df.empty:
        st.warning("Nenhum filme encontrado com os filtros selecionados.")
    else:
        cols = st.columns(3)  # 3 cards por linha
        for idx, row in enumerate(df.itertuples()):
            col = cols[idx % 3]
            with col:
                with st.container():
                    st.markdown(
                        f"""
        <div style="display: flex; flex-direction: row; align-items: flex-start; gap: 10px;
                    padding: 10px; border: 1px solid #ccc; border-radius: 10px;
                    background-color: #f9f9f9; margin-bottom: 12px;">
            <img src="{POSTER_BASE_URL}{row.poster}" alt="{row.titulo}"
                 style="width: 120px; height: auto; border-radius: 8px;" />
            <div style="flex: 1;">
                <h5 style="margin: 0 0 5px 0; font-size: 16px;">🎬 {row.titulo}</h5>
                <p style="margin: 0; font-size: 13px;">
                    📅 {row.ano_lancamento if row.ano_lancamento else "Ano desconhecido"}<br>
                    🌍 Idioma: {row.idioma_original.upper()}<br>
                    ⭐ Nota: {row.media_votos:.1f} / 10<br>
                    📝 <b>Descrição:</b> {row.generos[:200] + '...' if row.generos and len(row.generos) > 200 else row.generos}
                </p>
            </div>
        </div>
        """,
                        unsafe_allow_html=True
                    )

# ---------------------- PÁGINA GRÁFICOS ----------------------
elif pagina == "📊 Gráficos":
    st.title("📊 Relação entre Avaliação e Popularidade")

    col1, col2 = st.columns(2)
    with col1:
        tamanho_based = st.selectbox("Tamanho dos pontos representa:", ["Quantidade de votos", "Ano de lançamento"], key="size_option")

    with col2:
        cor_based = st.selectbox("Cor dos pontos representa:", ["Idioma original", "Gênero principal", "Ano de lançamento"], key="color_option")

    size_column = "quantidade_votos" if tamanho_based == "Quantidade de votos" else "ano_lancamento"
    if cor_based == "Idioma original":
        color_column = "idioma_original"
    elif cor_based == "Gênero principal":
        df["genero_principal"] = df["generos"].str.split(",").str[0]
        color_column = "genero_principal"
    else:
        color_column = "ano_lancamento"

    fig = px.scatter(
        df,
        x="popularidade",
        y="media_votos",
        size=size_column,
        color=color_column,
        hover_name="titulo",
        hover_data={
            "ano_lancamento": True,
            "generos": True,
            "quantidade_votos": True,
            "popularidade": ":.2f",
            "media_votos": ":.1f"
        },
        labels={
            "popularidade": "Popularidade (TMDB)",
            "media_votos": "Nota Média (0-10)",
            size_column: tamanho_based,
            color_column: cor_based
        },
        title=f"Relação: Popularidade × Nota Média<br><sub>Tamanho: {tamanho_based} | Cor: {cor_based}</sub>",
        template="plotly_dark",
        height=600
    )

    fig.update_traces(marker=dict(line=dict(width=0.3, color='DarkSlateGrey')), opacity=0.8)
    fig.update_layout(hoverlabel=dict(bgcolor="white", font_size=12))

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📆 Filmes por Ano")
    df_filmes_ano = df.groupby("ano_lancamento").size().reset_index(name="qtd_filmes")
    fig2 = px.bar(df_filmes_ano, x="ano_lancamento", y="qtd_filmes", labels={"ano_lancamento": "Ano", "qtd_filmes": "Quantidade"}, title="Filmes Lançados por Ano", template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📈 Tendência de Qualidade por Ano")
    df_ano_media = df.groupby('ano_lancamento')['media_votos'].mean().rolling(3).mean().reset_index()
    fig_tendencia = px.line(df_ano_media, x='ano_lancamento', y='media_votos', title='Média Móvel (3 anos) das Avaliações', labels={'media_votos': 'Nota Média', 'ano_lancamento': 'Ano'})
    fig_tendencia.add_hline(y=df['media_votos'].mean(), line_dash="dash")
    st.plotly_chart(fig_tendencia, use_container_width=True)
