FROM python:3.8.13-slim

# Defina o diretório de trabalho
ENV DBT_HOME=/home/dbtuser
WORKDIR $DBT_HOME

# Instale dependências essenciais
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Instale dbt diretamente no sistema (sem venv)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir dbt-core==1.7.7 dbt-bigquery==1.7.7  

# Crie pasta de configuração do dbt
RUN mkdir -p $DBT_HOME/.dbt

# Copie o projeto para dentro da imagem
COPY . $DBT_HOME/dbt-project
COPY ./.dbt/profiles.yml $DBT_HOME/.dbt/profiles.yml

# Defina o diretório padrão de execução
WORKDIR $DBT_HOME/dbt-project
