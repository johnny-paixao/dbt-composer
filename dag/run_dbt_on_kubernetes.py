# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A DAG that runs and tests a Dockerized dbt project on Kubernetes.
Developed for Composer version 1.17.0. Airflow version 2.1.2
"""

import datetime
import json
import os



from airflow import models
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable


from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator




# The environment variables from Cloud Composer
env = Variable.get("run_environment")
project = os.getenv("GCP_PROJECT")

# Airflow default arguments
default_args = {
    'depends_on_past': False,
    'start_date': datetime.datetime(2024, 1, 1),    
    # Make sure to set the catchup to False in this basic example
    # This will prevents multiple dbt runs from the past dates
    'catchup':False,
    'retries': 0
}

# Select and use the correct Docker image from the private Google Cloud Repository (GCR)
IMAGE = 'gcr.io/{project}/dbt-builder-basic:latest'.format(
    project=project
)

# A Secret is an object that contains a small amount of sensitive data such as
# a password, a token, or a key. Such information might otherwise be put in a
# Pod specification or in an image; putting it in a Secret object allows for
# more control over how it is used, and reduces the risk of accidental
# exposure.


# dbt default variables
# These variables will be passed into the dbt run
# Any variables defined here, can be used inside dbt

default_dbt_vars = {
        "project_id": project,
        # Example on using Cloud Composer's variable to be passed to dbt
        "bigquery_location": Variable.get("bigquery_location")
    }

# dbt default arguments
# These arguments will be used for running the dbt command

default_dbt_args = {
    # Setting the dbt variables
    "--vars": default_dbt_vars,
    # Define which target to load
    "--target": env,
    # Which directory to look in for the profiles.yml file.
    "--profiles-dir": ".dbt"
}

# Converting the default_dbt_args into python list
# The python list will be used for the dbt command
# Example output ["--vars","{project_id: project}","--target","remote"]

dbt_cli_args = []
for key, value in default_dbt_args.items():
    dbt_cli_args.append(key)

    if isinstance(value, (list, dict)):
        value = json.dumps(value)
    dbt_cli_args.append(value)

# Define the DAG
with models.DAG(
    dag_id='run_dbt_on_kubernetes',
    schedule_interval="0 0 * * *",
    default_args=default_args,
    catchup=False
) as dag:

    dbt_run = KubernetesPodOperator(
        task_id='dbt_run',
        name='dbt-run',
        namespace='dbt-tasks',
        service_account_name='dbt-ksa',
        image_pull_policy='Always',
        arguments=["run"] + dbt_cli_args,
        get_logs=True,
        log_events_on_failure=True,
        is_delete_operator_pod=True,
        image=IMAGE
    )

    dbt_test = KubernetesPodOperator(
        task_id='dbt_test',
        name='dbt-test',
        namespace='dbt-tasks',
        service_account_name='dbt-ksa',
        image_pull_policy='Always',
        arguments=["test"] + dbt_cli_args + ["--store-failures"],
        get_logs=True,
        log_events_on_failure=True,
        is_delete_operator_pod=True,
        image=IMAGE

    )

    dbt_run >> dbt_test


dag.doc_md = __doc__
