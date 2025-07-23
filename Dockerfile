# Usa uma imagem Python leve
FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false 

# Define diretório de trabalho
WORKDIR /app
COPY . .

# Instala o Poetry
RUN pip install poetry

# Desativa ambientes virtuais e instala dependências
RUN poetry config installer.max-workers 10 
RUN poetry install --no-interaction --no-ansi

# Instala o Streamlit
RUN pip install streamlit

# Expõe a porta do Streamlit
EXPOSE 8501

# Comando para iniciar o Streamlit
CMD ["streamlit", "run", "src/code_war/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]