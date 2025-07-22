import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, select
from code_war.models import Filme
from code_war.database import Base, get_session, Settings

st.set_page_config(page_title="Dashboard Ghibli", layout="wide")

# Título do dashboard
st.title("🎬 Dashboard - Filmes do Studio Ghibli")

# Conexão com o banco
engine = create_engine(Settings().DATABASE_URL, connect_args={
                       "check_same_thread": False})

# Lê os dados com Pandas + SQLAlchemy
with engine.connect() as conn:
    df = pd.read_sql(select(Filme), conn)

# Filtros
diretor = st.selectbox("Filtrar por diretor", options=[
                       "Todos"] + sorted(df["diretor"].unique().tolist()))
produtor = st.selectbox("Filtrar por produtor", options=[
                        "Todos"] + sorted(df["produtor"].unique().tolist()))

# Aplica filtros
if diretor != "Todos":
    df = df[df["diretor"] == diretor]
if produtor != "Todos":
    df = df[df["produtor"] == produtor]

# Exibe tabela
st.subheader("📋 Tabela de Filmes")
st.dataframe(df)

# Gráfico de pontuação
st.subheader("🍅 Pontuação no Rotten Tomatoes")
df["pontuacao_rotten_tomatoes"] = pd.to_numeric(
    df["pontuacao_rotten_tomatoes"], errors='coerce')

st.bar_chart(df.set_index("titulo")["pontuacao_rotten_tomatoes"])
