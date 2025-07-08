# ⚔️ Code War 2025 – API de Filmes Ghibli com FastAPI

## 📌 Descrição

Este projeto foi desenvolvido como parte do desafio **Code War 2025 – Edição Python + Análise de Dados**. O objetivo é construir uma **API RESTful do zero** utilizando **FastAPI**, com integração a um banco de dados **SQLite**, validações robustas, **registro de logs**, testes automatizados e um processo **ETL** a partir da **API pública do Studio Ghibli**.

A proposta envolve boas práticas de desenvolvimento, versionamento com Git, logs detalhados, testes automatizados com Pytest e, opcionalmente, conteinerização com Docker.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI**
- **SQLite + SQLAlchemy**
- **Pydantic**
- **Uvicorn**
- **Requests**
- **Pandas**
- **Logging (nativo do Python)**
- **Streamlit / Plotly** (dashboard)
- **Pytest** (testes)
- **Docker / Docker Compose** (bônus)

---

## 🔄 Funcionalidades da API

- `GET /filmes/` – Lista todos os filmes (resposta em JSON ou XML)
- `GET /filmes/{id}` – Busca filme por ID
- `POST /filmes/` – Cria novo filme
- `PUT /filmes/{id}` – Atualiza um filme
- `DELETE /filmes/{id}` – Deleta um filme (soft delete)

### Extras:
- ✅ Datas de inclusão, edição e exclusão geradas automaticamente
- ✅ Validação de entrada com tratamento de erro `400`
- ✅ Logs registrados em tempo real para cada operação

---

## 🧪 Testes Automatizados

- Desenvolvidos com `pytest` e `TestClient` do FastAPI
- Testes de:
  - Criação (`POST`)
  - Leitura (`GET`)
  - Atualização (`PUT`)
  - Exclusão (`DELETE`)
  - Validações de erros e status HTTP
- Rodam com banco de dados `:memory:` (isolado por teste)
- Simulam inserção e retorno com schemas reais

---

## 📝 Registro de Logs

- Implementação completa de `logging` no backend
- Logs gerados para cada endpoint (`INFO`, `ERROR`)
- Mensagens padronizadas com timestamp e rota acessada
- Exemplo de log gerado:

▶️ Como rodar localmente

# Instalar dependências
pip install -r requirements.txt

# Executar a API localmente
uvicorn code_war.app:app --reload

# Rodar testes
pytest

👨‍💻 Autor

Desenvolvido por Pedro Eduardo Braga
