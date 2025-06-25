# ⚔️ Code War 2025 – API com Python + Análise de Dados

## 📌 Descrição

Este projeto foi desenvolvido como parte do desafio **Code War 2025 – Edição Python + Análise de Dados**. O objetivo é construir uma **API RESTful do zero** utilizando **FastAPI**, integrando com banco de dados **SQLite**, realizando um **processo ETL** a partir de uma **API pública**, e exibindo os dados em um **dashboard interativo**.

A proposta é aplicar boas práticas de programação, organização de repositório, logs, testes e, opcionalmente, conteinerização com Docker.

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI**  
- **SQLite + SQLAlchemy**
- **Pydantic**
- **Uvicorn**
- **Requests**
- **Pandas**
- **Streamlit / Plotly**
- **Pytest** (testes)
- **Docker / Docker Compose** (bônus)

## 🔄 Funcionalidades da API

- `GET /entidade` – Lista todos os registros (JSON e XML)
- `GET /entidade/{id}` – Busca item por ID
- `POST /entidade` – Cria novo item
- `PUT /entidade/{id}` – Atualiza item existente
- `DELETE /entidade/{id}` – Exclui item (soft delete)
- Datas de inclusão, edição e exclusão registradas automaticamente
- Logs das requisições
- Validação de erros (status 200, 400, etc.)

## 📥 ETL com API Pública

- API utilizada: https://ghibliapi.vercel.app/
- Extração de dados externos
- Transformação com Pandas
- Inserção automatizada via API

## 📊 Dashboard

- Análise exploratória dos dados
- Visualização interativa com Plotly
- Gráficos de distribuição, comparação e insights

## 🧪 Testes

- Testes unitários com `pytest`
- Validação de endpoints principais
- Simulação de falhas (respostas esperadas)

## 🐳 Docker (BÔNUS)

- Arquivo `Dockerfile` configurado
- `docker-compose.yml` (se necessário)
- Imagem disponível para uso e compartilhamento
- Documentação do processo de build e execução

## 👨‍💻 Autor

Desenvolvido por Pedro Eduardo Braga
