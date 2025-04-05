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


from datetime import datetime, timedelta
import os
import json

from airflow import DAG
from airflow.models import Variable
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

project = os.getenv("GCP_PROJECT")
env = Variable.get("run_environment")

default_args = {
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
    'catchup': False
}

# Convert dbt arguments
dbt_vars = {
    "project_id": project,
    "bigquery_location": Variable.get("bigquery_location")
}

dbt_args = [
    "--vars", json.dumps(dbt_vars),
    "--target", env,
    "--profiles-dir", ".dbt"
]

with DAG(
    dag_id='run_dbt_on_kubernetes',
    default_args=default_args,
    schedule_interval="0 0 * * *",
    tags=["dbt", "kubernetes"]
) as dag:

    dbt_run = KubernetesPodOperator(
        task_id="dbt_run",
        namespace="dbt-tasks",
        service_account_name="dbt-ksa",
        image=f"gcr.io/{project}/dbt-builder-basic:latest",
        image_pull_policy="Always",
        cmds=["dbt", "run"] + dbt_args,
        get_logs=True,
        is_delete_operator_pod=True
    )

    dbt_test = KubernetesPodOperator(
        task_id="dbt_test",
        namespace="dbt-tasks",
        service_account_name="dbt-ksa",
        image=f"gcr.io/{project}/dbt-builder-basic:latest",
        image_pull_policy="Always",
        cmds=["dbt", "test"] + dbt_args + ["--store-failures"],
        get_logs=True,
        is_delete_operator_pod=True
    )

    dbt_run >> dbt_test



dag.doc_md = __doc__
