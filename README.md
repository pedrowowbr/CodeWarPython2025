# 🎬 API de Filmes 

Este projeto foi desenvolvido como parte do **desafio Code War 2025**, com o objetivo de aplicar conceitos avançados de backend, integração com APIs públicas (TMDb), manipulação de banco de dados, ETL e visualização de dados com Streamlit.

---

## 📌 Objetivo

Criar uma API RESTful com dados extraídos da API pública do The Movie Database (TMDb), armazenados em banco local e exibidos em um dashboard com métricas visuais e interativas.

---

## 🛠️ Funcionalidades 

✅ Endpoints da API (FastAPI)

- **GET /filmes** – Listar todos os filmes
- **GET /filmes/{id}** – Obter um filme por ID
- **POST /filmes** – Criar um novo filme manualmente
- **PUT /filmes/{id}** – Atualizar informações de um filme
- **DELETE /filmes/{id}** – Remover um filme
- **POST /etl/tmdb** - Executar ETL da API TMDb

---

## 🔁 Extração e Tratamento de Dados (ETL)

- Extração de dados em tempo real da API TMDb
- Filtro por gêneros e popularidade
- Armazenamento estruturado em SQLite usando SQLAlchemy ORM

---

## 🎥 Banco de Dados (SQLite via SQLAlchemy)

O banco de dados `database.db` contém:

- **Filme** – Título, data de lançamento, nota, imagem, descrição, popularidade, e gênero(s)

---

## 📊 Dashboard Interativo com Streamlit

O painel exibe:

- 🎞️ Lista de filmes com imagem e descrição
- 📊 Filtro por gênero
- 📈 Gráficos de popularidade e avaliações
- 🔍 Pesquisa dinâmica por título

---

## ⚙️ Tecnologias Utilizadas

- **FastAPI** – Para construção da API
- **SQLAlchemy** – ORM para manipulação do banco
- **Pydantic** – Validação e estruturação de dados
- **Poetry** – Gerenciador de dependências
- **TMDb API** – Fonte dos dados
- **Streamlit** – Para construção do dashboard

---

## 🔐 Variáveis de Ambiente (.env)

```env
DATABASE_URL=sqlite:///./database.db
TMDB_API_KEY=sua_api_key_aqui
```
---

## 🚀 Como Rodar Localmente

- Instale dependências
```bash
poetry install
```

- Execute a API
```bash
poetry run uvicorn src.code_war.app:app --reload
```

- Execute o Dashboard
```bash
poetry run streamlit run src/code_war/dashboard.py
```
---

## 🐋 Executando via Docker

```bash
docker build -t meu-dashboard-tmdb.
docker run -p 8501:8501 meu-dashboard-tmdb.
