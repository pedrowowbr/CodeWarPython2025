# Usa uma imagem Python leve
FROM python:3.12-slim

# Desativa ambientes virtuais do Poetry
ENV POETRY_VIRTUALENVS_CREATE=false

# Define diretório de trabalho
WORKDIR /app

# Copia todos os arquivos do projeto
COPY . .

# Instala o Poetry
RUN pip install poetry

# Instala dependências do projeto
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

# Instala FastAPI e Uvicorn
RUN pip install fastapi uvicorn

# Expõe a porta padrão da FastAPI
EXPOSE 8000

# Comando para rodar a FastAPI com Uvicorn
CMD ["uvicorn", "src.code_war.app:app", "--host", "0.0.0.0", "--port", "8000"]