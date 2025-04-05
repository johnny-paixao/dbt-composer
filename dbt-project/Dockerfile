FROM python:3.8.13

ARG DBT_HOME=/home/dbtuser

# Install required system packages
RUN apt-get update -y && \
  apt-get install --no-install-recommends -y -q \
  git libpq-dev python-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create user and working directory
RUN groupadd -g 999 dbtuser && useradd -r -u 999 -g dbtuser dbtuser
WORKDIR ${DBT_HOME}
RUN chown -R dbtuser:dbtuser ${DBT_HOME}
USER dbtuser

# Create dbt profiles folder
RUN mkdir ${DBT_HOME}/.dbt

# Install dbt in virtualenv
RUN pip install -U pip
ENV VIRTUAL_ENV=${DBT_HOME}/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dbt version used in your project
RUN pip install dbt-core==1.0.4 dbt-bigquery==1.0.0

# Copy your real project structure
COPY --chown=dbtuser:dbtuser ./dbt-project ${DBT_HOME}/dbt-project
COPY --chown=dbtuser:dbtuser ./dbt-project/.dbt/profiles.yml ${DBT_HOME}/.dbt/

# Entrypoint for dbt commands
ENTRYPOINT ["dbt"]
