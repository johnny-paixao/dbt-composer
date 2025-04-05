FROM python:3.8-slim

ARG DBT_HOME=/home/dbtuser

# Install only required system dependencies
RUN apt-get update -y && \
  apt-get install --no-install-recommends -y \
  git libpq-dev gcc && \
  rm -rf /var/lib/apt/lists/*

# Create user and working directory
RUN useradd -ms /bin/bash -u 999 dbtuser
USER dbtuser
WORKDIR ${DBT_HOME}

# Install dbt directly
RUN pip install --no-cache-dir dbt-core==1.0.4 dbt-bigquery==1.0.0

# Copy project and profile
COPY --chown=dbtuser:dbtuser . ${DBT_HOME}/dbt-project
COPY --chown=dbtuser:dbtuser ./.dbt/profiles.yml ${DBT_HOME}/.dbt/profiles.yml

ENV PATH="${HOME}/.local/bin:$PATH"
